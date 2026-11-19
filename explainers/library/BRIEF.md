# Brief for library videos (3 minutes each)

User's ask (19 Nov 2026): "create such 3 min videos for all the topics in our lab, such as market data protocols,
exchanges, feed handlers, network, signal generation, most common HFT & Hedge fund strategies, order entry, asset
classes, biggest exchanges and why etc. Create up to at least 10s of videos for each topic." The list is CATALOGUE.md.

## How to make each video
- Read /mnt/project-files/videos/explainers/engine/GUIDE.md, engine/stage.html, engine/engine.js first, and look at
  one finished video for house style (e.g. /mnt/project-files/videos/explainers/cpp-no-alloc and signals).
- Folder /mnt/project-files/videos/explainers/<slug>/. Target 165-195 s total, 6-7 scenes: title card -> why it
  matters -> the mechanism as an animated diagram (packets, books, timelines, byte layouts, flows) -> a worked example
  with real numbers -> a lab tie-in where the repo has one -> pitfalls / what pros do -> one-line takeaway.
- Brand (video.json): "<TOPIC NAME> · TRADING LAB" in caps, e.g. "MARKET DATA · TRADING LAB".
  Title card eyebrow: "<TOPIC> · NN / 10".
- Every scene moves with the narration; diagrams over bullet text; consistent colour per actor.
- Pipeline: tts.py, build_data.py, render contact, sheet.py, read every sheet, fix. Don't run make.sh.
  When a video passes, append its slug to /tmp/claude-0/vx/queue.txt (`echo <slug> >> /tmp/claude-0/vx/queue.txt`)
  and set its CATALOGUE.md status to queued (re-read the file just before editing; change only your row).
- Write a 150-300 word companion note /mnt/project-files/videos/explainers/library/notes/<slug>.md: key facts with a
  source link each, and anything you were unsure of.

## Accuracy (these teach engineers and traders)
- Every number, field layout, rule, date and market statistic must come from a primary source you read this session:
  the lab repo /home/claude/ts-push (docs/specs/*.md for ITCH, MoldUDP64, SoupBinTCP, OUCH, FIX 4.4 subset, drop copy;
  libs/ and firm/ code; read-only, never commit), exchange specs and rulebooks, SEC/ESMA/CFTC texts, exchange annual
  reports and investor pages, WFE statistics, BIS triennial survey, academic papers.
- Market statistics change: give the year and source on screen ("2025, WFE"). Prefer rounded figures. If you can't
  verify a number, leave it out. Strategy videos explain mechanics and risks; no performance claims or advice.
- Use WebSearch/WebFetch; Firecrawl tends to time out; curl may be blocked by the proxy.

## Shared box and folder
- /mnt/project-files is a shared network mount: write only your own slug folders and notes, re-read shared files just
  before editing, append-only for queue.txt. Scratch goes in /tmp/claude-0/vx/<slug>/.
- The box is a shared 4-vCPU VM with several agents: run one TTS job at a time, keep contact renders to what you need.
- Don't install packages; test a tool on something small before relying on it.
