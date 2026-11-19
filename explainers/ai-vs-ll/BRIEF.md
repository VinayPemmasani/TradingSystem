# AI-bloat vs low-latency C++: 16 patterns, one 3-minute video each

User's ask: Stroustrup (now at Susquehanna, eFinancialCareers 6 Aug 2026) says AI-generated C++ can be bloated for the
low-latency scene. Research current HFT low-latency principles and show side-by-side code with walkthroughs of how and
why that is true, 10-20 practical latency-critical patterns, and a 3-minute video for each.

## Framing (be fair and accurate)
- LEFT = "the general-purpose version": the idiomatic, correct, safe code an assistant typically writes when the prompt
  states no latency budget (std containers, heap, exceptions, virtuals, iostream, mutex, seq_cst...). Never claim a
  specific model produced it; call it "typical AI-style / general-purpose" code. It must be correct and reasonable,
  not a strawman.
- RIGHT = "the hot-path version" an HFT engineer writes. Must be correct, compile cleanly with -Wall -Wextra, and be
  tested for the same output as LEFT.
- Every video ends with the honest nuance: the bloat comes from missing constraints (latency budget, no allocation,
  bounded sizes, single writer), so stating those constraints, then measuring, is the fix; and when the general version
  IS fine (cold path, startup, tooling).
- Numbers: measure both versions on this box (g++ -O2 -std=c++20; pin with taskset; use `chrt -f 10` for two-thread
  tests). The box is a shared 4-vCPU cloud VM, so label on screen "measured on a shared 4-vCPU cloud VM" and show
  p50 and p99 (or ns/op with min-max of runs). Never invent numbers. Ratios matter more than absolutes.
- Also report something about bloat itself where it fits: instructions per op (perf may be unavailable; then use
  objdump line counts of the hot function or binary .text size via `size`), allocations per op (count via a
  replaced operator new), bytes per element.

## Sources to cite (verify what you use)
- Read /mnt/project-files/videos/explainers/ai-vs-ll/RESEARCH.md once it exists (a research agent is writing it).
- David Gross (Optiver), "When Nanoseconds Matter", CppCon 2024 keynote; Carl Cook (Optiver), "When a Microsecond Is
  an Eternity", CppCon 2017; cppreference; Intel/AMD optimization manuals; the lab repo /home/claude/ts-push
  (libs/core has SpscRing etc.; read-only, do not commit).

## Files per pattern (slug ai-NN-name)
1. Code: /tmp/claude-0/vx/<slug>/code/ with ai.hpp (left), fast.hpp (right), bench.cpp, test, README of how measured.
   Keep each side's snippet that goes on screen to <= 16 lines x 52 cols so two fit side by side at 22-24px mono.
2. Video sources: /mnt/project-files/videos/explainers/<slug>/ per /mnt/project-files/videos/explainers/engine/GUIDE.md
   (read it, plus engine/stage.html and engine.js; look at an existing video like cpp-no-alloc or cpp-false-sharing
   for the house style). Target 170-195 s total. Suggested arc (6-7 scenes): title -> the task + the general version
   on the left -> what it costs at the machine level (animated diagram: heap nodes, cache lines, pipeline, syscalls...)
   -> the hot-path version on the right, side by side, lines highlighted as the narration explains them -> measured
   numbers (bars / counts) -> nuance + one-line rule. Keep colours consistent across all 16: LEFT/general = red-ish
   (--red), RIGHT/hot-path = teal (--teal), costs = amber.
   Brand in video.json: "AI CODE VS HOT PATH · TRADING LAB".
   Title card eyebrow: "PATTERN NN / 16".
3. Run tts.py, build_data.py, render contact frames, sheet.py, read every sheet, fix issues. Don't run make.sh.
   When a video passes its checks, append its slug as its own line to /tmp/claude-0/vx/queue.txt
   (`echo <slug> >> /tmp/claude-0/vx/queue.txt`); the coordinator's render queue picks it up.
4. Write-up: /mnt/project-files/videos/explainers/ai-vs-ll/patterns/<slug>.md with: title; one-line rule; the two
   snippets (full, as fenced cpp); a 4-8 bullet walkthrough of why the left is slower (machine-level causes);
   measured table (metric, general, hot path, ratio) with method line; when the general version is fine; sources (links).

## Shared-folder rules
/mnt/project-files is a network mount shared with other sessions: write only your own slugs' folders/files; re-read a
shared file just before changing it and keep edits small (queue.txt: append only). Don't install packages unless
already present; test a tool on something small before planning around it. Keep scratch outside /mnt/project-files.
The box is shared and loaded: run benchmarks pinned, one at a time, and don't run more than one TTS job at once.

## Corrections from research (read RESEARCH.md)
- The eFinancialCareers piece is dated 2 June 2026 and does not mention Susquehanna; Stroustrup joined Susquehanna as
  Technical Fellow on 6 Aug 2026 (Business Wire). Don't put "6 Aug" on the article. Don't quote "bloated" as his words.
- Google study (arXiv 2608.06640): observational, no latency measured; about 5% CPU and 8% heap memory, and AI code
  had more copy/allocation findings (1.39x). Cite it only that way.
- Exceptions: zero cost when not thrown (Carl Cook); the cost is the throw path (~1.5 µs in his talk).
