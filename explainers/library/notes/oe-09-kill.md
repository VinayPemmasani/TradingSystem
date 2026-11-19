# oe-09-kill: Kill switches

Key facts and sources
- EU RTS 6 (Commission Delegated Regulation (EU) 2017/589) Article 12: an investment firm shall be able to cancel immediately, as an emergency measure, any or all of its unexecuted orders submitted to any or all venues ("kill functionality"); it must be able to identify which algorithm and which trader, desk or client is responsible for each order. Source: [legislation.gov.uk, 2017/589 Art. 12](https://legislation.gov.uk/eur/2017/589/article/12/2020-12-31?view=plain); [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2017/589/oj).
- CME Kill Switch: at Legal Clearing Entity, Execution Firm or SenderComp level; only session messages accepted; Day and Good Till orders cancelled; mass quotes not cancelled. Source: [CME Globex Credit Controls, Kill Switch](https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/Kill-Switch.html).
- CME Cancel on Disconnect: on by default; triggered by involuntary disconnects and missed heartbeats, not by a graceful logout; GTC and GTD excluded. Source: [CME client wiki, Cancel on Disconnect](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457216487/Cancel+on+Disconnect).
- Lab: `Risk::kill()` sets an atomic flag checked first in every check (`firm/risk`); simex cancels all of an account's orders when its connection closes, unless started with `--no-cancel-on-disconnect` (`exchange/simex/gateway.cpp`, `main.cpp`). There is no call to clear the kill flag (`risk.hpp`).

Worked example (illustrative): runaway buying, kill flag at t=0, 120 working orders cancelled.

Unsure / left out: in the lab only tests call `kill()`; no operator control is wired up, so the video says "any thread can set it". No figures on how fast CME cascades cancels beyond "within a second" for blocking (not narrated).
