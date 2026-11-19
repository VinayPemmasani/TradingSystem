# Generates script.json, scenes.html, scenes.js, style.css, pron.json, video.json
# for cpp-live-optimize. All numbers come from code/results*.txt and code/mt_main.out.
import json, sys, html, os
sys.path.insert(0, '/tmp/claude-0/vx/cpp-branches-layout')
from cg import hl_cpp, hl_asm
OUT = '/mnt/project-files/videos/explainers/cpp-live-optimize'
N = json.load(open('/tmp/claude-0/vx/cpp-live-optimize/nums.json'))

# ---------------------------------------------------------------- numbers
ST = N['single']          # name -> [p50, p99, p999]
MT = N['mt']              # name -> [p50, p99, p99_lo, p99_hi, p50_lo, p50_hi]
def f(x):
    return f'{x:.0f}' if x >= 10 else f'{x:.1f}'
def us(x):
    return f'{x/1000:.1f}'
M50, M99 = MT['mutex'][0], MT['mutex'][1]
R50, P50, L50 = MT['packed'][0], MT['padded'][0], MT['lab'][0]

# ---------------------------------------------------------------- script
S = []
def sc(i, title, text, hold=0):
    S.append({'id': i, 'title': title, 'text': text, **({'hold': hold} if hold else {})})

sc('title', 'Live optimization',
   "An interviewer hands you a market data handler and says: make it fast. "
   "Let's do it live, one step at a time. "
   "Every change is measured on this box, and every version must print the same output.")
sc('snippet', 'The snippet',
   "Here is the snippet. "
   "Each message is a quote or a trade for one stock. "
   "It finds the symbol's state in a std::map keyed by string. "
   "Trades are appended to a history vector. "
   "Then it computes a VWAP over the last 32 trades, and returns buy, sell or hold.")
sc('measure', 'How we measure',
   "First, the measurement. "
   "We replay two million synthetic messages and time every call with rdtsc. "
   "We keep the median and the 99th percentile per message, never averages. "
   "The timer itself costs about 27 nanoseconds, and that is inside every number. "
   "A test checks that every version returns exactly the same signals.")
sc('baseline', 'Baseline',
   "This is a shared four vCPU cloud VM, so the thread is pinned and runs under a real time scheduler. "
   f"The naive handler takes {f(ST['v0'][0])} nanoseconds at the median, and {f(ST['v0'][1])} at p99. "
   "Five suspects are already visible. "
   "A string keyed map, a string copy, a growing vector, a 32 step loop, and two divides.")
# part 1
sc('ds-map', 'Data structures',
   "Start with the map. "
   "A std::map is a red black tree, so a lookup chases a pointer at every level, around nine levels for 500 symbols. "
   "Each level compares strings, and each hop can miss the cache. "
   "But the feed already gives us an integer. "
   "Every ITCH message carries a two byte stock locate code, so index a flat array with it.")
sc('ds-layout', 'Hot fields',
   "Then lay the state out for the cache. "
   "Everything we touch per message fits in one 64 byte line, aligned so it never straddles two. "
   "The symbol name is cold, so it moves to its own array. "
   f"The median drops from {f(ST['v0'][0])} to {f(ST['v1'][0])} nanoseconds. "
   f"No locate code on your feed? An open addressing table on the eight symbol bytes measured {f(ST['v1h'][0])}.")
sc('pipeline', 'CPU pipelining',
   "Next, the pipeline. "
   "Every instruction is fetched, decoded, executed, and retired in program order. "
   "An out of order core keeps many instructions in flight, and executes any whose inputs are ready. "
   "So independent work overlaps. "
   "But an instruction that needs the previous result has to wait for it. "
   "A dependency chain runs at the speed of its latency.")
sc('chain', 'Dependency chains',
   "Our VWAP loop is one chain: every add waits for the add before it. "
   "The textbook fix is four accumulators, four short chains running side by side. "
   "The values are whole numbers stored in doubles, so the sum stays exact. "
   f"In isolation it helps a little: {N['ilp'][0]} nanoseconds becomes {N['ilp'][1]}. "
   f"Inside the handler, the median barely moved: {f(ST['v1'][0])} to {f(ST['v2a'][0])}. "
   "So the add chain was not the limit; each element also needs two converts and a load from a 48 byte record.")
sc('divide', 'Delete the chain',
   "The real fix is to delete the chain. "
   "Keep running sums: add the new trade, and subtract the one that falls out of the window. "
   "Now the divides. "
   "The compiled code is divide, subtract, divide, each one waiting on the last. "
   "A double divide takes about 13 to 15 cycles of latency on recent Intel cores. "
   f"So cross multiply instead, in integers: in isolation, {N['div'][0]} nanoseconds becomes {N['div'][1]}. "
   f"The handler drops to {f(ST['v2'][0])}.")
sc('predict', 'Branch prediction',
   "Now branches. "
   "The core guesses every branch direction and keeps fetching down the guessed path. "
   "A wrong guess throws that work away, typically 15 to 20 cycles on current x86 cores. "
   "Validation fails about one percent of the time, so it predicts well. "
   "But bid or ask is a coin flip, and the signal itself is close to random.")
sc('branchless', 'Branchless',
   "So turn those branches into data. "
   "Bid and ask become a two element array, indexed by the side. "
   "The signal becomes two comparisons subtracted: plus one, zero, or minus one. "
   "Then check with g++ -S. "
   "Before, the side and the buy signal were conditional jumps. "
   "After, they are sete and setg instructions, and an indexed store. "
   f"The median drops from {f(ST['v2'][0])} to {f(ST['v3'][0])} nanoseconds.")
sc('hidden', 'Hidden allocations',
   "Now memory. "
   "Replace operator new with a counter, and count every allocation in a run. "
   f"The naive version allocates {N['allocs'][0]:,} times: 500 map nodes, and 6,000 vector buffers as the histories grow. "
   "Each time a vector fills, it allocates a buffer twice as big, moves every trade across, and frees the old one. "
   "You never see it at the median. You see it in the tail. "
   "The eight character symbols fit the string's small buffer, so those copies never call malloc.")
sc('prealloc', 'Preallocate',
   "The fix is a fixed window: 32 slots inside each symbol's state, overwriting the oldest. "
   "No vector, no strings, no malloc. "
   "All 512 states are allocated once, at startup. "
   "Allocations per run drop to zero. "
   f"The median stays at {f(ST['v4'][0])}, but p99 falls from {f(ST['v3'][1])} to {f(ST['v4'][1])} nanoseconds. "
   f"And p99.9 falls from {ST['v3'][2]/1000:.1f} microseconds to {f(ST['v4'][2])} nanoseconds.")
sc('part1', 'Single thread',
   "That is part one. "
   f"Same program, same output: {f(ST['v0'][0])} down to {f(ST['v4'][0])} nanoseconds at the median, and {f(ST['v0'][1])} down to {f(ST['v4'][1])} at p99. "
   f"Take away the {f(ST['timer'][0])} nanosecond timer, and the work itself is about {f(ST['v4'][0]-ST['timer'][0])} nanoseconds per message.")
# part 2
sc('split', 'Two threads',
   "Now the interviewer adds: decoding runs on its own thread. "
   "So split the program. "
   "A feed thread stamps each message with rdtsc and hands it over. "
   "A strategy thread runs the handler from part one. "
   "Latency now runs from the stamp to the signal. "
   "One message arrives every microsecond, and each thread is pinned to its own core.")
sc('mutex', 'Mutex queue',
   "The obvious handoff is a mutex, a queue, and a condition variable. "
   "The strategy thread sleeps until it is notified. "
   "Waking a sleeping thread goes through the kernel. "
   f"On this busy box the median is now {M50/1000:.0f} microseconds, and p99 is {M99/1000:.0f} microseconds. "
   f"Our {f(ST['v4'][0]-ST['timer'][0])} nanoseconds of work disappear inside it.")
sc('flag', 'A plain bool',
   "So someone suggests a plain bool flag. "
   "Write the message, then set ready to true. "
   "That is a data race, which is undefined behaviour. "
   "Here is what g++ -O2 really emits. "
   "In publish, the flag store moved above the message stores. "
   "In consume, the spin loop is gone.")
sc('reorder', 'Weak ordering',
   "Two layers may reorder memory. "
   "The compiler may move any access that a single thread could not notice. "
   "The CPU parks stores in a store buffer and lets later loads run ahead. "
   "x86 uses total store order: only a later load may pass an earlier store. "
   "ARM is weakly ordered: almost any two accesses to different addresses may be reordered.")
sc('acqrel', 'Acquire and release',
   "The fix is a release store on the flag, and an acquire load on the other side. "
   "When the acquire load reads the value that was released, the store happens before the load. "
   "So every write before the release is visible after the acquire. "
   "On x86 both are plain mov instructions, and the loop stays. "
   "On ARM, clang emits stlrb and ldarb.")
sc('ring', 'Lock-free ring',
   "Generalize the flag into a single producer, single consumer ring. "
   "The producer writes a slot, then stores head with release. "
   "The consumer loads head with acquire, then reads the slot. "
   "No locks, and no kernel. "
   f"The median falls to {f(R50)} nanoseconds. "
   f"Most of that is cache lines crossing cores: about {N['oneway']} nanoseconds each way on this VM.")
sc('mesi', 'Cache lines',
   "Caches move whole 64 byte lines, and to write a line, a core must own it. "
   "Each copy is Modified, Exclusive, Shared, or Invalid. "
   "Our ring packs head, tail, and both stats counters into one line. "
   "So every write by one thread invalidates the other core's copy. "
   f"Two threads bumping counters in one line: {N['fs'][0]} nanoseconds per increment. "
   f"On separate lines: {N['fs'][1]}.")
sc('padfix', 'alignas(64)',
   "So give each index and each counter its own line, with alignas 64. "
   f"The median drops from {f(R50)} to {f(P50)} nanoseconds. "
   "Last, cached indices. "
   "The producer keeps a private copy of tail, and reads the real one only when the ring looks full. "
   f"That is the lab's SpscRing, and it measured {f(L50)}. "
   "At one message a microsecond the ring is almost never full, so here the cache barely matters.")
sc('results', 'Results',
   "Here is every step, measured on this box. "
   f"On one thread, {f(ST['v0'][0])} down to {f(ST['v4'][0])} nanoseconds at the median. "
   "Across threads, the handoff costs far more than all the work. "
   "That is why low latency systems keep the hot path on one pinned thread. "
   "The two thread p99 is noisy here, because a shared VM steals time.")
sc('checklist', 'Talking points',
   "To recap for the interview. "
   "Measure first, per message, with percentiles. "
   "Replace node maps and strings with integer ids and flat arrays. "
   "Shorten dependency chains, and avoid divides. "
   "Make random branches into data, and read the assembly. "
   "Allocate at startup. "
   "Publish with release and acquire. "
   "And give each thread's hot data its own cache line.", hold=1.5)

PRON = [
    [r"std::map", "standard map"], [r"std::string", "standard string"],
    [r"\bp99\.9\b", "P ninety nine point nine"], [r"\bp99\b", "P ninety nine"], [r"\bp50\b", "P fifty"],
    [r"\brdtsc\b", "R D T S C"], [r"\bVWAP\b", "vee wap"], [r"\bvCPU\b", "V C P U"], [r"\bVM\b", "V M"],
    [r"g\+\+ -O2", "G plus plus, O two,"], [r"g\+\+ -S", "G plus plus, dash S"], [r"\bx86\b", "x eighty six"],
    [r"\bITCH\b", "itch"], [r"\bSpscRing\b", "S P S C ring"], [r"\balignas\b", "align as"],
    [r"\bstlrb\b", "S T L R B"], [r"\bldarb\b", "L D A R B"], [r"\bsete\b", "set E"], [r"\bsetg\b", "set G"],
    [r"\bmov\b", "move"], [r"\bARM\b", "arm"], [r"\bCPU\b", "C P U"], [r"\b6,500\b", "six thousand five hundred"],
    [r"\b6,000\b", "six thousand"], [r"\bmalloc\b", "malloc"], [r"\bclang\b", "clang"],
]

json.dump(S, open(f'{OUT}/script.json', 'w'), indent=1)
json.dump(PRON, open(f'{OUT}/pron.json', 'w'), indent=1)
json.dump({'brand': 'C++ LIVE OPTIMIZATION · TRADING LAB'}, open(f'{OUT}/video.json', 'w'))
import re
words = sum(len(s['text'].split()) for s in S)
print('scenes', len(S), 'words', words)
for s in S:
    sents = [x for x in re.split(r'(?<=[.!?])\s+', s['text'].strip()) if x]
    long = [x for x in sents if len(x.split()) > 22]
    if long: print('LONG', s['id'], long)
NS = {s['id']: len([x for x in re.split(r'(?<=[.!?])\s+', s['text'].strip()) if x]) for s in S}

exec(open('/tmp/claude-0/vx/cpp-live-optimize/scenes_gen.py').read())
