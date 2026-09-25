# pc-dragonquestswords

Toward a native PC port of **Dragon Quest Swords: The Masked Queen and the
Tower of Mirrors** (Wii, Square Enix / Genius Sonority, 2007), the
first-person, on-rails sword-fighting RPG. It was a Wii exclusive and never
re-released. The goal is the game running natively on PC, with the Wii
Remote's pointer, shield and sword swings replaced by the mouse.

This repository documents the disc, its formats and its code, and grows the
tooling for the port. It is the second port built on
**[wiikit](https://github.com/vs-sr-dev/wiikit)**, the game-agnostic Wii
toolkit that grew with [pc-victorious](https://github.com/vs-sr-dev/pc-victorious)
and is now its own repository, taken here as a submodule at `wiikit/`
(clone with `--recursive`, or `git submodule update --init`). Where this
game needs something every Wii game would need (a stripped executable, RVZ
images, motion input), it goes into wiikit, not here.

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the European release, RDQPGD (English, French, German, Spanish, Italian).

## Layout

    docs/     disc, format and code analysis, the plan
    tools/    exploratory and Dragon Quest Swords-specific tools
    wiikit/   game-agnostic Wii toolkit (submodule: github.com/vs-sr-dev/wiikit)

## Tools

Python 3.8+, no dependencies (pycryptodome, if installed, speeds up disc
decryption). Run from the repository root.

```sh
# the disc, straight from the RVZ (or .iso, .wbfs)
python -m wiikit.disc GAME.rvz --info
python -m wiikit.disc GAME.rvz --extract build/extract

# the executable
python -m wiikit.dol build/extract/sys/main.dol --info
python tools/census.py build/extract/sys/main.dol
python tools/sigmatch.py build/extract/sys/main.dol \
    --dsy <Dolphin>/Sys/totaldb.dsy \
    --elf <pc-victorious>/build/extract/files/Oscar_wii_final_versioned.elf \
    --out build/sig_guess.tsv
python tools/names.py build/extract/sys/main.dol      # -> build/names.tsv

# recompile, build, boot (clang, Ninja, SDL3 as for Victorious)
python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp --symbols build/names.tsv
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1
ninja -C build/recomp-build
build/recomp-build/wiiboot build/extract          # fonts and dsp_coef.bin in build/fonts
```

## Status

Session 2: **the game boots and draws.** The stripped executable is mapped
(8 744 functions found by discovery, names from hand, debug strings and
signatures), recompiled to C++ that compiles and links, and booted: from
`__start` through the SDK's `OSInit`, the static constructors, VI, GX and
AX to the main loop. The Wii Strap screen (natively 16:9) and the Square
Enix logo draw right; the 3D title screen draws flat blue at 10 fps, next.
In Dolphin, A turns out to set the centre swings are directed from: the
press of the mouse scheme. The disc is read straight from the RVZ.

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
