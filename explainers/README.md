# Explainer videos

Narrated 1080p explainer videos about the lab, and the tooling that makes them. The videos are not kept in git; render them from these sources.

| Video | Slug | Length |
| --- | --- | --- |
| Aeron IPC between processes | `aeron-ipc` (older single-file stage) | 3:14 |
| REST API calls | `rest-api` | 5:01 |
| Kafka pump and topics | `kafka` | 4:59 |
| HTTP on the wire (HTTP/1.1, HTTP/2, HTTP/3, WebSocket) | `http` | 4:55 |
| FPGA decode for book building | `fpga-book` | 5:00 |
| Signals on top of book and the full book | `signals` | 4:57 |
| Tick to trade, end to end | `tick-to-trade` | 4:39 |
| Cache lines and false sharing | `cpp-false-sharing` | 3:05 |
| Memory ordering: acquire and release | `cpp-memory-order` | 2:56 |
| No allocation on the hot path | `cpp-no-alloc` | 3:12 |
| Branches and data layout | `cpp-branches-layout` | 3:15 |
| Static vs virtual dispatch | `cpp-static-dispatch` | 3:14 |
| Walkthrough: SPSC ring buffer | `cpp-spsc-ring` | 3:08 |
| Walkthrough: order book with O(1) cancel | `cpp-order-book` | 3:02 |
| Walkthrough: fixed-point price parsing | `cpp-price-parse` | 3:14 |
| Walkthrough: sliding-window VWAP | `cpp-vwap` | 3:00 |

## Layout

- `engine/` holds the scene engine and pipeline. Read `engine/GUIDE.md` before writing a video.
  - `stage.html` and `engine.js` are a stateless `render(t)`; visuals are cued to narration sentences with `data-cue` attributes.
  - `tts.py` voices `script.json` with kokoro-onnx (voice `am_michael`).
  - `build_data.py` lays out the scene timing.
  - `render.js` screenshots each frame with Playwright into ffmpeg.
  - `make.sh` does all of the above.
- `videos/<slug>/` holds one video:
  - `script.json` (narration, which is also the captions), `scenes.html`, and optional `scenes.js`, `style.css` and `pron.json`.
  - `gen/`, where present, has the generator that wrote `scenes.html`. It still points at the scratch paths it was written in.
  - `code/` holds the C++ shown on screen, with its tests and benchmarks. Build it by hand, for example `g++ -std=c++20 -O2 -Wall -Wextra -pthread test.cpp`. It is not part of the CMake build.

## Rendering

The engine expects these layouts:
- sources in `/mnt/project-files/videos/explainers/<slug>/`
- work files in `/tmp/claude-0/vx/<slug>/`
- the voice model in `/tmp/claude-0/av/voice/`

The model is `kokoro-v1.0.onnx` and `voices-v1.0.bin`, from the github.com/thewh1teagle/kokoro-onnx releases. Change the paths at the top of each script to render elsewhere.

```
bash engine/make.sh <slug> 3   # 3 render workers -> <slug>.mp4
```

Benchmark numbers in the videos were measured on a shared, heavily loaded 4-vCPU cloud box, and the videos say so. Rerun the `code/` benchmarks on pinned cores for real numbers.
