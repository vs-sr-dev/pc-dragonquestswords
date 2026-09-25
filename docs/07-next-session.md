# TODO — session 2

Phase 1, the code map.

0. ~~wiikit's home~~: done in session 1, its own repository
   (github.com/vs-sr-dev/wiikit, public) and a submodule in both ports
   (`10-wiikit.md`).

1. **Dolphin experiment** (half an hour, answers the biggest unknown):
   Dolphin, the emulated Remote with
   Swing (up, down, left, right, forward) on keys, the pointer on the
   mouse. Play to the first battle. Do slashes land by direction, does a
   forward swing stab, do diagonals come through? Record it with Dolphin's
   input recording for later replays.
2. **RVZ in `wiikit.disc`**, so the ISO in `build/` can go.
3. **Function discovery** for stripped executables: entries from calls,
   data pointers into text, flow; units; switch tables bounded by their
   compare. Measured against Ghidra with the Gekko language.
4. **`wiikit.sig`** from `tools/sigmatch.py`, with uniqueness and
   call-graph checks; `build/symbols.tsv`; every name in Victorious's
   `hooks.txt` resolved or explained.
5. If time: phase 2's first step, the whole executable through the
   emitter to C++ that compiles.
