# pc-dragonquestswords

Toward a native PC port of **Dragon Quest Swords: The Masked Queen and the
Tower of Mirrors** (Wii, Square Enix / Genius Sonority, 2007), the
first-person, on-rails sword-fighting RPG. It was a Wii exclusive and never
re-released. The goal is the game running natively on PC, with the Wii
Remote's pointer, shield and sword swings replaced by the mouse.

The route is static recompilation: the game's own PowerPC code, translated
to C++ and built for the PC, running on a replacement for the Wii's
hardware and system software. Nothing is emulated at the instruction
level, and nothing of the game is rewritten.

This repository documents the disc, its formats and its code, and holds the
port's own tools and layer. It is the second port built on
**[wiikit](https://github.com/vs-sr-dev/wiikit)**, the game-agnostic Wii
toolkit that grew with [pc-victorious](https://github.com/vs-sr-dev/pc-victorious)
and is now its own repository, taken here as a submodule at `wiikit/`
(clone with `--recursive`, or `git submodule update --init`). Where this
game needs something every Wii game would need (a stripped executable, RVZ
images, a PAL boot, the locked cache, motion input), it goes into wiikit,
not here.

## Where it stands

After three sessions the game **boots, draws, sounds and plays its
opening**: the intro, the title, a new save, the movies, the town and the
tutorial's first battles, at 16:9 and at the game's own rate, with its
music in time and the Remote speaker's sounds mixed in. Slashes work with
the mouse. **It is not yet playable through**: the tutorial stops at the
Master Stroke (raise the Remote, bring it down), which the port cannot give
yet, and the stab is not found. Some models show faint lines on their
faces, heavy scenes stutter the first time they appear, and fog is not
drawn. See [Status](#status) and
[docs/07-next-session.md](docs/07-next-session.md).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the European release, RDQPGD (English, French, German, Spanish, Italian);
the addresses in `tools/` and `docs/` are that executable's.

## Layout

    docs/     disc, format and code analysis, the plan, the session log
    tools/    Dragon Quest Swords-specific tools, the port's layer (dqs.cpp)
    wiikit/   game-agnostic Wii toolkit (submodule: github.com/vs-sr-dev/wiikit)
    build/    (not in git) the disc, everything derived from it, the build

## Tools

The Python tools need only Python 3.8+ and no dependencies (pycryptodome,
if installed, speeds up disc decryption; RVZ needs Python 3.14 for zstd).
Building the recompiled code needs CMake, Ninja, a C++20 compiler (clang
from MSYS2 is what is used here) and SDL3; running it needs OpenGL 4.5.
Run from the repository root.

```sh
# the disc, straight from the RVZ (or .iso, .wbfs)
python -m wiikit.disc GAME.rvz --info
python -m wiikit.disc GAME.rvz --extract build/extract

# the executable: stripped, so its names are found, not read
python -m wiikit.dol build/extract/sys/main.dol --info
python tools/census.py build/extract/sys/main.dol
python tools/sigmatch.py build/extract/sys/main.dol \
    --dsy <Dolphin>/Sys/totaldb.dsy --out build/sig_guess.tsv
python tools/names.py build/extract/sys/main.dol      # -> build/names.tsv
```

`sigmatch.py` takes signatures from Dolphin's database and, with
`--elf`, from any symbolised executable (Victorious's
`Oscar_wii_final_versioned.elf` names 112 more). Dolphin's alone is
enough: the names the runtime hooks that only Victorious's ELF had are in
`tools/names-manual.tsv`, with their evidence.

```sh
# recompile, build: the port's layer comes in through WIIKIT_EXTRA
python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
    --symbols build/names.tsv
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1 \
    -DWIIKIT_EXTRA=$PWD/tools/dqs.cmake
ninja -C build/recomp-build

# boot the game: the NAND (saves, SYSCONF) in build/nand; the boot ROM's
# fonts and the DSP ROM's resampling table in build/fonts (font_western.bin,
# font_japanese.bin, dsp_coef.bin: Dolphin's Sys/GC has free ones)
build/recomp-build/wiiboot build/extract --symbols build/names.tsv
build/recomp-build/wiiboot build/extract --window 1920x1080
build/recomp-build/wiiboot build/extract --no-video --quit-after 30   # no window

# where the time goes, and a frame's GX commands and EFB (see wiikit)
WIIKIT_PERF=1 build/recomp-build/wiiboot build/extract 2> run.err
WIIKIT_GXTRACE=1880 build/recomp-build/wiiboot build/extract          # or F12
```

### Playing

The mouse over the picture is the Remote's pointer. The keys are in
`build/keys.txt`, written with wiikit's defaults on the first run. For this
game, change its `Shake` line and add the two `Raise` lines:

    Shake = Space, Mouse Middle, Drag Left
    Raise = Left Shift
    Raise Alt = Left Ctrl

| Mouse, keys | Game |
|---|---|
| move | the pointer |
| left button, press | A: sets the centre a slash is directed from; confirms in menus |
| left button held, **drag fast** | a slash along the drag (slow movement never slashes) |
| right button, held | B: the shield, moved by the mouse |
| W A S D, arrows | the d-pad: stop, turn back, choose a branch on the rails |
| Tab, Q, 1, 2 | +, -, 1, 2 |
| Space, middle button | a shake: a slash along the pointer's movement |
| Left Shift, Left Ctrl | the Remote raised (for the Master Stroke: not yet recognised) |
| Esc, F11 / Alt+Enter, F12 | pause box, fullscreen, trace a frame's GX commands |

The port does not yet write these defaults itself (`07-next-session.md`).

## Status

Session 3: **the game in 3D, in time with its music, and played.** Every
model had been drawn through zero matrices: NW4R computes its view
matrices in the locked cache and stores them back by DMA, which the
runtime now does. The intro and the title then matched Dolphin, natively
16:9. From 10 fps to the game's own rate, up to 60 at EuRGB60: the vertex
buffer is a ring mapped once. The sound had four faults, found one under
the other (the hardware lock held across a hand-over, interrupts not taken
while waiting, 50 Hz chosen because the boot said PAL, draw-done answered
too early); the music is now clean and in time with the camera cuts. With
a save created, the user played the town and the tutorial's battles:
slashes come from mouse drags (the game takes a slash's direction from the
pointer's movement, the acceleration only triggers it), the Remote's
speaker is mixed in, the THP movies play. Not yet: the Master Stroke, the
stab, lines on some faces, a stutter at heavy scenes' first appearance,
fog.

Session 2: **the game boots and draws.** The stripped executable is mapped
(8 744 functions found by discovery, names from hand, debug strings and
signatures), recompiled to C++ that compiles and links, and booted: from
`__start` through the SDK's `OSInit`, the static constructors, VI, GX and
AX to the main loop. The Wii Strap screen (natively 16:9) and the Square
Enix logo draw right; the 3D title screen drew flat blue at 10 fps. In
Dolphin, A turns out to set the centre swings are directed from: the press
of the mouse scheme. The disc is read straight from the RVZ.

Session 1: **analysis and plan.** The disc is read and mapped (3 751 files:
FPK packs of NW4R resources and scripts, BRSAR/BRSTM sound, THP movies in
4:3 and 16:9 pairs). The executable is stripped, but small: 745 000 words
of code, about 9 900 functions, a 2007 RVL SDK with NW4R G3D, EF and SND,
no REL modules and no third-party middleware. 1 813 library functions are
named by signature on a first try, among them every one the runtime hooks.
The route is the same as Victorious (static recompilation, the SDK replaced
at the hardware), with three new problems: a stripped executable, a richer
3D renderer, and sword swings from a mouse. See
[docs/06-attack-plan.md](docs/06-attack-plan.md).

## Documentation

    00-sessions.md            progress log
    01-disc-layout.md         what is on the disc
    03-executable.md          the stripped DOL: what is linked, where, how it is named
    04-curiosities.md         what the disc reveals
    05-open-questions.md      what is still unknown
    06-attack-plan.md         feasibility and the porting route
    07-next-session.md        the plan for the next session
    08-input.md               the Remote in this game, and the mouse scheme
    10-wiikit.md              how this port uses and grows wiikit

## Licence

MIT. This covers the documentation and tools in this repository only. It
says nothing about Dragon Quest Swords, which remains the property of its
rights holders.
