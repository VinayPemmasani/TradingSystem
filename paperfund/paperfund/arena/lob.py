"""One exchange, one stock, microsecond clock: a price-time priority limit order book and the
firms that race on it. Simulation only.

The fair value R (in ticks) moves in jumps, as when the futures or another venue moves first.
Some jumps are preceded by a lead signal on another venue's feed; a firm sees it only if it
reads that feed directly. Each firm reacts after its own latency plus jitter, so whoever is
faster cancels a stale quote, picks one off, or reaches the front of the new queue first.
"""

from __future__ import annotations

import heapq
import math
from collections import deque
from dataclasses import dataclass, field

import numpy as np

TICK = 0.01            # dollars per tick
DAY_US = 23_400_000_000  # 6.5 hours in microseconds
MAKER_REBATE = 0.20    # ticks per share (0.20 cents)
TAKER_FEE = 0.30       # ticks per share (0.30 cents)
HEDGE_COST = 0.10      # ticks per share for a sniper to lay off a position elsewhere


@dataclass
class Firm:
    """A firm on the book. kind is 'mm' (quotes both sides), 'sniper' (takes stale quotes) or
    'flow' (sends marketable child orders for a slower fund)."""
    name: str
    kind: str
    latency_us: float
    size: int = 300
    max_inv: int = 3000
    lead_p: float = 0.0         # chance it reads the feed that carries a given lead signal
    guard_us: float = 0.0       # mm: wait this long after a jump before quoting again
    stressed_off: bool = False  # mm: stop quoting on stressed days
    jitter_us: float = 1.0
    parent: int = 0             # pflow: shares to work today (signed)
    # state
    inv: int = 0
    cash: float = 0.0
    view: int = 0
    oids: dict = field(default_factory=dict)


class Book:
    def __init__(self):
        self.side = {1: {}, -1: {}}  # 1 bids, -1 asks: price -> deque[[oid, owner, qty]]
        self.where = {}

    def best(self, s):
        lv = self.side[s]
        if not lv:
            return None
        return max(lv) if s == 1 else min(lv)

    def add(self, oid, owner, s, price, qty):
        self.side[s].setdefault(price, deque()).append([oid, owner, qty])
        self.where[oid] = (s, price)

    def cancel(self, oid):
        loc = self.where.pop(oid, None)
        if loc is None:
            return False
        s, p = loc
        q = self.side[s][p]
        for i, o in enumerate(q):
            if o[0] == oid:
                del q[i]
                break
        if not q:
            del self.side[s][p]
        return True

    def take(self, s, qty, limit):
        """Marketable order on side s (1 buy, -1 sell) up to price limit. Returns fills as
        (maker, maker_oid, price, qty, queue_rank) and the unfilled quantity."""
        opp = self.side[-s]
        fills = []
        while qty > 0 and opp:
            p = min(opp) if s == 1 else max(opp)
            if (s == 1 and p > limit) or (s == -1 and p < limit):
                break
            q = opp[p]
            rank = 0
            while qty > 0 and q:
                o = q[0]
                n = min(qty, o[2])
                fills.append((o[1], o[0], p, n, rank))
                o[2] -= n
                qty -= n
                if o[2] == 0:
                    q.popleft()
                    self.where.pop(o[0], None)
                rank += 1
            if not q:
                del opp[p]
        return fills, qty


@dataclass
class DayParams:
    jumps: int
    big_jump_p: float      # chance a jump is 2+ ticks
    lead_p: float = 0.6    # chance a jump has a lead signal
    sweep_p: float = 0.35  # chance a 2+ tick jump is preceded by an informed sweep
    noise_orders: int = 1500
    flow_orders: dict = field(default_factory=dict)  # firm -> (n child orders, direction)


REGIME_DAY = {
    0: DayParams(jumps=500, big_jump_p=0.15),
    1: DayParams(jumps=800, big_jump_p=0.22),
    2: DayParams(jumps=1600, big_jump_p=0.40),
}


def default_firms():
    """The microstructure cast. Latencies are wire-to-wire estimates for each kind of setup."""
    return [
        Firm("apex_hft", "mm", 3.0, size=500, max_inv=5000, lead_p=0.95),
        Firm("sniper_arb", "sniper", 2.0, max_inv=4000, lead_p=0.95),
        Firm("tier2_mm", "mm", 60.0, size=400, max_inv=4000, lead_p=0.3, jitter_us=8),
        Firm("your_md_fund", "mm", 25.0, size=200, max_inv=1500, lead_p=0.9, guard_us=400,
             stressed_off=True, jitter_us=4),
        Firm("mirofish_fund", "mm", 2000.0, size=300, max_inv=3000, lead_p=0.0, jitter_us=300),
    ]


class DaySim:
    def __init__(self, firms, params: DayParams, rng, start=10_000.0, record_jumps=0):
        self.f = {x.name: x for x in firms}
        self.p = params
        self.rng = rng
        self.book = Book()
        self.R = start
        self.t = 0.0
        self.heap = []
        self.seq = 0
        self.oid = 0
        self.last_jump = -1e18
        self.fills = []  # (t, maker, taker, taker_side, price, qty, rank)
        self.rpath_t = [0.0]
        self.rpath_v = [start]
        self.record_until = -1.0
        self.record_jumps = record_jumps
        self.log = []
        self.jump_no = 0
        self.races = []  # per big jump: who reacted when, who got hit

    # -- plumbing
    def push(self, t, kind, *a):
        self.seq += 1
        heapq.heappush(self.heap, (t, self.seq, kind, a))

    def lat(self, firm):
        return firm.latency_us + self.rng.exponential(firm.jitter_us)

    def rec(self, kind, who, detail):
        if self.t <= self.record_until:
            snap = {}
            for s, nm in ((1, "bids"), (-1, "asks")):
                lv = sorted(self.book.side[s], reverse=(s == 1))[:3]
                snap[nm] = [[p, [[o[1], o[2]] for o in self.book.side[s][p]]] for p in lv]
            self.log.append({"t": round(self.t, 2), "kind": kind, "who": who, "detail": detail,
                             "R": self.R, "book": snap})

    # -- quoting
    def quote(self, m: Firm):
        """Re-quote both sides at the current fair value. An order already resting at the right
        price is left alone, so it keeps its place in the queue."""
        off = m.stressed_off and self.p.jumps >= 1600
        guarded = self.t - self.last_jump < m.guard_us
        m.view = self.R
        skew = 1 if abs(m.inv) > m.max_inv // 2 else 0
        want = {}
        if not off and not guarded:
            for s in (1, -1):
                if m.kind == "pflow":
                    left = m.parent - m.inv
                    if s * left <= 0:
                        continue
                elif s * m.inv >= m.max_inv:
                    continue
                wide = skew if s * m.inv > 0 else 0
                want[s] = (math.ceil(self.R) - 1 - wide) if s == 1 else (math.floor(self.R) + 1 + wide)
        for s in (1, -1):
            o = m.oids.get(s)
            if o is not None and o in self.book.where and self.book.where[o][1] == want.get(s):
                want.pop(s)
                continue
            if o is not None:
                m.oids.pop(s)
                self.book.cancel(o)
        if guarded and not off:
            self.push(self.last_jump + m.guard_us + 1, "requote", m.name)
        for s, price in want.items():
            self.oid += 1
            size = m.size if m.kind != "pflow" else min(m.size, abs(m.parent - m.inv))
            self.book.add(self.oid, m.name, s, price, size)
            m.oids[s] = self.oid
        self.rec("quote", m.name, {"view": m.view})

    def pull(self, m: Firm, s):
        o = m.oids.pop(s, None)
        if o is not None and self.book.cancel(o):
            self.rec("pull", m.name, {"side": "bid" if s == 1 else "ask"})

    # -- matching
    def market(self, taker, s, qty, limit):
        fills, left = self.book.take(s, qty, limit)
        t = self.f.get(taker)
        for maker, oid, price, n, rank in fills:
            mk = self.f[maker]
            mk.inv -= s * n
            mk.cash += s * n * price + n * MAKER_REBATE
            if mk.kind == "pflow" and mk.oids.get(-s) == oid:
                self.book.cancel(oid)
                mk.oids.pop(-s, None)
                self.push(self.t + self.lat(mk), "requote", maker)
            elif mk.oids.get(-s) == oid and oid not in self.book.where:
                mk.oids.pop(-s, None)
                self.push(self.t + self.lat(mk), "requote", maker)
            if t is not None:
                t.inv += s * n
                t.cash -= s * n * price + n * TAKER_FEE
            self.fills.append((self.t, maker, taker, s, price, n, rank))
        if fills:
            self.rec("trade", taker, {"side": "buy" if s == 1 else "sell",
                                      "fills": [[f[0], f[2], f[3], f[4]] for f in fills]})
        return fills, left

    # -- events
    def run(self, flow_dir):
        rng, p = self.rng, self.p
        jt = np.sort(rng.uniform(0, DAY_US, p.jumps))
        for i, t in enumerate(jt):
            u = rng.random()
            k = 0.5 if u > p.big_jump_p + 0.3 else (1.0 if u > p.big_jump_p else
                                                     (2.0 if rng.random() < 0.75 else 3.0))
            d = 1 if rng.random() < 0.5 else -1
            self.push(t, "jump", d * k, i)
            if rng.random() < p.lead_p:
                self.push(t - rng.uniform(4, 120), "lead", d, k, i)
            if k >= 1 and rng.random() < p.sweep_p:
                # an informed order that knows the move is coming sweeps the whole queue first
                self.push(t - rng.uniform(50, 2000), "sweep", d, int(rng.integers(1500, 3500)))
        for t in rng.uniform(0, DAY_US, p.noise_orders):
            self.push(t, "noise", 1 if rng.random() < 0.5 else -1, int(rng.choice([100, 200, 300, 500])))
        for name, (n, d) in p.flow_orders.items():
            for t in rng.uniform(0, DAY_US, n):
                self.push(t, "flow", name, d, int(rng.choice([100, 200, 300])))
        for m in self.f.values():
            if m.kind in ("mm", "pflow"):
                self.push(self.lat(m), "requote", m.name)
        while self.heap:
            self.t, _, kind, a = heapq.heappop(self.heap)
            getattr(self, "on_" + kind)(*a)
        return self.close()

    def on_jump(self, dk, i):
        self.R += dk
        self.last_jump = self.t
        self.rpath_t.append(self.t)
        self.rpath_v.append(self.R)
        if i < self.record_jumps:
            self.record_until = self.t + 3000
        self.rec("jump", "market", {"ticks": dk})
        for m in self.f.values():
            if m.kind in ("mm", "pflow"):
                self.push(self.t + self.lat(m), "requote", m.name)
            elif m.kind == "sniper":
                self.push(self.t + self.lat(m), "snipe", m.name)

    def on_lead(self, d, k, i):
        if i < self.record_jumps:
            self.record_until = max(self.record_until, self.t + 3200)
        self.rec("lead", "other venue", {"dir": d, "ticks": k})
        for m in self.f.values():
            if self.rng.random() >= m.lead_p:
                continue
            if m.kind in ("mm", "pflow"):
                self.push(self.t + self.lat(m), "pull_side", m.name, -d)
            elif m.kind == "sniper" and k >= 1:
                self.push(self.t + self.lat(m), "snipe_pred", m.name, d, k)

    def on_requote(self, name):
        self.quote(self.f[name])

    def on_pull_side(self, name, s):
        self.pull(self.f[name], s)

    def _snipe(self, sn: Firm, fair):
        room = sn.max_inv
        for s in (1, -1):
            b = self.book.best(-s)
            edge = TAKER_FEE + 0.2
            if b is not None and s * (fair - b) > edge and s * sn.inv < room:
                lim = math.floor(fair - edge) if s == 1 else math.ceil(fair + edge)
                self.market(sn.name, s, room - s * sn.inv, lim)
        # hedge straight away on another venue / the futures at fair value plus a small cost
        sn.cash += sn.inv * fair - abs(sn.inv) * HEDGE_COST
        sn.inv = 0

    def on_snipe(self, name):
        self._snipe(self.f[name], self.R)

    def on_snipe_pred(self, name, d, k):
        self._snipe(self.f[name], self.R + d * k)

    def on_noise(self, s, q):
        fills, left = self.market("retail", s, q, round(self.R) + s * 4)
        if left:
            self.fills.append((self.t, "background", "retail", s, round(self.R) + s * 3, left, 99))

    def on_sweep(self, s, q):
        fills, left = self.market("informed", s, q, round(self.R) + s * 2)

    def on_flow(self, name, s, q):
        fills, left = self.market(name, s, q, round(self.R) + s * 4)
        if left:
            px = round(self.R) + s * 3
            t = self.f.get(name)
            if t is not None:
                t.inv += s * left
                t.cash -= s * left * px
            self.fills.append((self.t, "background", name, s, px, left, 99))

    def close(self):
        """Mark each firm at the closing fair value; flattening costs half a spread."""
        out = {}
        for m in self.f.values():
            if m.kind == "pflow":
                left = m.parent - m.inv  # finish the parent order in the closing auction
                px = self.R + (1.0 if left > 0 else -1.0)
                m.cash -= left * px
                m.inv = m.parent
            pnl = m.cash + m.inv * self.R - abs(m.inv) * 1.0
            out[m.name] = None if m.kind in ("flow", "pflow") else pnl * TICK
        return out


def markouts(sim: DaySim, horizon_us=1_000_000):
    """Per fill: maker's gain versus fair value horizon_us later (positive = maker did well)."""
    t = np.array(sim.rpath_t)
    v = np.array(sim.rpath_v)
    res = []
    for (ft, maker, taker, s, price, n, rank) in sim.fills:
        j = np.searchsorted(t, ft + horizon_us, side="right") - 1
        res.append((maker, taker, n, rank, -s * (v[j] - price) * n * TICK))
    return res


def niche_firms():
    """A less contested venue (a regional exchange, another country, another asset class) where
    the top two speed firms are not connected. The cast is smaller and slower."""
    return [
        Firm("tier2_mm", "mm", 60.0, size=400, max_inv=4000, lead_p=0.3, jitter_us=8),
        Firm("local_arb", "sniper", 45.0, max_inv=3000, lead_p=0.4, jitter_us=6),
        Firm("your_md_fund", "mm", 25.0, size=300, max_inv=2000, lead_p=0.9, jitter_us=4),
        Firm("mirofish_fund", "mm", 2000.0, size=300, max_inv=3000, lead_p=0.0, jitter_us=300),
    ]


def simulate_day(regime, rng, flow=None, firms=None, record_jumps=0, passive=None, niche=False):
    """flow: {fund: (child orders, direction)} sent as marketable orders.
    passive: {fund: signed shares} worked passively by a 25us lead-aware algo, the rest in the
    closing auction."""
    p = REGIME_DAY[regime]
    if niche:
        p = DayParams(p.jumps // 2, p.big_jump_p, p.lead_p, p.sweep_p, p.noise_orders // 2)
    p = DayParams(p.jumps, p.big_jump_p, p.lead_p, p.sweep_p, p.noise_orders, dict(flow or {}))
    fs = firms or (niche_firms() if niche else default_firms())
    for name in p.flow_orders:
        fs.append(Firm(name, "flow", 3000.0))
    for name, q in (passive or {}).items():
        fs.append(Firm(name, "pflow", 25.0, size=200, lead_p=0.9, jitter_us=4, parent=int(q)))
    sim = DaySim(fs, p, rng, record_jumps=record_jumps)
    pnl = sim.run(None)
    return sim, pnl


def exec_cost(sim: DaySim, name, direction):
    """Cost per share in ticks against fair value at the moment of each fill, for a fund's
    orders that day: spread paid or earned, exchange fees or rebates, the closing-auction
    remainder (1 tick), and the markout one second later for passive fills (adverse selection).
    Returns (cost per share, share of the parent filled before the close)."""
    t = np.array(sim.rpath_t)
    v = np.array(sim.rpath_v)
    tot = n_tot = 0.0
    for (ft, maker, taker, s, price, n, rank) in sim.fills:
        if taker == name:
            fee = TAKER_FEE if maker != "background" else 0.0
            j = np.searchsorted(t, ft, side="right") - 1
            tot += (s * (price - v[j]) + fee) * n
        elif maker == name:
            j = np.searchsorted(t, ft + 1_000_000, side="right") - 1
            tot += (-s * (price - v[j]) - MAKER_REBATE) * n
        else:
            continue
        n_tot += n
    m = sim.f[name]
    filled = n_tot
    if m.kind == "pflow":
        left = abs(m.parent) - filled
        tot += max(left, 0) * 1.0
        n_tot = abs(m.parent)
    return (tot / n_tot if n_tot else 0.0), (filled / n_tot if n_tot else 0.0)
