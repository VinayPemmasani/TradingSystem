# Packet life in 3D

One order's journey through the lab, end to end, as a 3D scene: the exchange's market
data packet, the firm's feed handler and book, the strategy and risk checks, the OUCH
order over SoupBinTCP, simex accepting it, a FIX firm selling into it, the match, and
the fills fanning out to both firms, the public feed and the drop copy.

Every message is the real one the lab's own code builds: `tools/order-trace` runs the
codecs, `BookBuilder`, market maker, risk, OMS and matching engine, and prints each wire
message as bytes and fields, plus the p50/p99 cost of each step on the machine it ran
on. A packet is drawn as a strip of boxes, one per field, sized by the field's bytes, so a
172-byte MoldUDP64 packet is visibly longer than a 31-byte ITCH Order Executed.

There are two versions of the same scene:

| | |
|---|---|
| `index.html` | three.js (r160 from jsDelivr), any modern browser |
| `opengl/` | native C++20, OpenGL 3.3 core with GLFW, Windows, Linux, WSL2 and macOS |

Both read `trace.json` (order-trace output) and `scene.json` (where the stations sit and
which path each message takes) and play the same timeline. Change one, keep the other
in step: the timing constants are at the top of each.

## Browser

```sh
python3 viz/packet-life/build_page.py --out packet-life.html   # data inlined
# open packet-life.html, or serve the folder:
cd viz/packet-life && python3 -m http.server 8000             # then http://localhost:8000
```

Space plays and pauses, the arrow keys step stages, F follows the packet, click the bar to
seek, drag to orbit. The panel shows the stage, its measured timings, and each message's
bytes coloured by field.

## Native OpenGL

Needs CMake 3.20+, a C++20 compiler and OpenGL 3.3. GLFW 3.4 and `stb_easy_font.h` are
downloaded at configure time (pinned by SHA-256) unless GLFW is already installed.

```sh
cmake -S viz/packet-life/opengl -B build/packet-life -DCMAKE_BUILD_TYPE=Release
cmake --build build/packet-life --config Release
build/packet-life/packet-life-gl              # Windows: build\packet-life\Release\packet-life-gl.exe
```

- **Linux**: install the X11 headers GLFW needs once:
  `sudo apt install libx11-dev libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev libgl-dev`.
- **WSL2**: same packages; the window opens through WSLg on Windows 11. If it reports no
  OpenGL 3.3, run with `LIBGL_ALWAYS_SOFTWARE=1`.
- **Windows**: Visual Studio 2022 with "Desktop development with C++", then the commands
  above from a Developer PowerShell.
- **macOS**: Xcode command line tools; the viewer asks for a 3.3 core forward-compatible
  context, which macOS provides.

Keys: Space play/pause, Left/Right stage, F follow, +/- speed, L light or dark, Esc quit.
Mouse: drag to orbit, right-drag to pan, scroll to zoom, click the bar to seek.

`--t 40 --screenshot shot.png --size 1500x900` renders one frame to a PNG and exits, which
also works headless under `Xvfb` with `LIBGL_ALWAYS_SOFTWARE=1`.

## New data

`trace.json` here came from `order-trace` on a shared cloud box, so its timings are that
machine's. To use your own:

```sh
cmake --build --preset release --target order-trace
./build/release/tools/order-trace/order-trace > viz/packet-life/trace.json
```

If order-trace gains or reorders stages or messages, update the legs in `scene.json`;
`build_page.py` checks that every leg points at a stage and message that exist.
