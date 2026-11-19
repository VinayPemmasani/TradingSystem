# Authoring an explainer video

Every video is a folder `/mnt/project-files/videos/explainers/<slug>/` with:

| File | What |
| --- | --- |
| `video.json` | `{"brand": "TOPIC · TRADING LAB"}`, shown at the top right |
| `script.json` | `[{"id","title","text", "hold"?}]`, one entry per scene. `text` is the narration *and* the captions. Each sentence becomes one caption, so keep sentences under about 22 words. `title` is the chapter pill. `hold` (seconds) adds silence after the narration. The first scene is the title card and shows no pill. |
| `pron.json` | `[[regex, spoken], ...]` applied to the spoken text only, e.g. `["\\bTCP\\b","T C P"]`, `["\\b64\\b","sixty four"]`, `["µs","microseconds"]`, `["ns\\b","nanoseconds"]`. Spell out symbols, units, version numbers and acronyms that the voice mangles. |
| `scenes.html` | one `<div class="scene" id="s-<id>">` per script entry. Children are absolutely positioned on a 1920x1080 canvas, so give each `left/top` (and `width`). |
| `scenes.js` | optional: `SCENES['<id>'] = { setup(H) {...}, draw(u, cue, H, scene) {...} }` for animation the attributes can't express. `u` is seconds into the scene; `cue(k)` is the start of caption k. `draw` must be stateless (compute everything from `u`). |
| `style.css` | optional extra CSS |

Leave the bottom 130 px clear for captions and the top 90 px clear for the chapter pill and brand.

## Timing elements to the narration

Everything is cued to caption (sentence) indexes in that scene, so visuals line up with the voice:

- `data-cue="2"`: fades in when sentence 2 (0-based) starts. `data-d="0.6"` delays it. `data-cue="2.5"` means halfway through sentence 2.
- `data-anim="up|fade|left|scale|none"` sets the entry motion (`up` is the default). Use `fade` on anything that needs its own CSS `transform`.
- `data-out="4"` fades it out at sentence 4, and `data-out="end"` at the end of the scene.
- `data-hl="3" data-hlend="5"` adds the amber glow (`.hl`) from sentence 3 to sentence 5. `data-dim="3"` dims it.
- `<path class="draw" data-cue=.. data-dur="1">` draws an SVG stroke in. Put paths in `<svg class="full">`, which spans the canvas in page coordinates. Arrowheads: `marker-end="url(#ah-teal)"` (also `ah`, `ah-amber`, `ah-green`, `ah-red`, `ah-violet`).
- `<div class="pkt" data-path="pathId" data-cue=.. data-dur="1.2" data-loop="1" data-phase="0.5" style="background:var(--amber)">` is a dot travelling along an SVG path. Path ids must be unique across the whole video.
- `<span class="count" data-cue=.. data-from="0" data-to="1500" data-dec="0" data-post=" ns">` counts up.
- `<span class="type" data-cue=.. data-dur="2">text</span>` types the text in.
- `<div class="grow" data-cue=.. data-w="640" data-dur="1">` grows its width from 0 (bar charts, latency budgets).

## Style kit (already in the stage)

Colours are CSS variables: `--teal --green --amber --red --violet --blue --pink --muted --panel --line`. Text colour utilities are `.c-teal`, `.c-amber`, and so on.

| Class | Use |
| --- | --- |
| `.eyebrow` + `.h1` + `.sub` | title card |
| `.h2` | scene headline (top about 110 px) |
| `.h3`, `.body`, `.lbl` | text sizes |
| `.box` (+ `.teal/.amber/...` border colour) with `.t` title and `.s` mono subtitle | components |
| `.code` | code block with `white-space:pre`. Tokens: `.k` keyword, `.c` comment, `.r` number/literal, `.g` string, `.v` type, `.x` red. Wrap lines in `<span class="line" data-hl="3">` to highlight a line during a sentence. |
| `.bytes` | a flex row of byte-field cells. Set each child's `width` and `background` inline, with label text inside. |
| `table.t` | a table |
| `.pill`, `.tag` | small labels |
| `.bar` | absolute bar |

Make it look designed: one idea per scene, big type, lots of space, and colour that means something (keep a colour per actor across scenes). Every scene should show something moving or building up with the narration, not a static slide. Diagrams beat bullet text.

## Commands

```
E=/mnt/project-files/videos/explainers/engine
python3 $E/tts.py <slug>              # voice all scenes (about 1 s per sentence); add scene ids to redo only those
python3 $E/build_data.py <slug>       # timing -> /tmp/claude-0/vx/<slug>/data.json
node $E/render.js <slug> contact      # one frame at the end of every sentence -> /tmp/claude-0/vx/<slug>/prev/
node $E/render.js <slug> preview 12.5 40 # specific times (seconds, whole video)
python3 $E/sheet.py <slug>            # 3x3 contact sheets of the prev frames; Read them to check
```

Delete `/tmp/claude-0/vx/<slug>/prev/*` before a new contact pass. Look at every sheet and fix the following:

- overlap
- text running off the canvas or under the captions
- elements appearing before the narration mentions them
- empty scenes
- `PAGE ERROR` lines

Rerun `build_data.py` after any change to `script.json` and its TTS. Do not run the full render (`make.sh`): the coordinator renders all the videos one at a time.

## Accuracy

These videos teach engineers, so every number, field offset, byte layout and protocol rule must be right. Check against primary sources: the lab repo at `/home/claude/ts-push` (its `docs/specs/`, code and docs), RFCs, the Apache Kafka protocol docs, and vendor docs. Where a number depends on hardware, say "typical" or give the lab's measured value with its context. Don't invent benchmark results.
