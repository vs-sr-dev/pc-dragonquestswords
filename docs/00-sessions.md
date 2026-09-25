# Session log

## Session 1 — analysis, feasibility, the plan

Goal: understand the disc and the code, measure what a stripped executable
costs, settle how the sword could be played with a mouse, choose a route.

Results:

* **The disc read** (`01-disc-layout.md`): the Redump RVZ converted with
  DolphinTool, the DATA partition extracted by `wiikit.disc` unchanged (its
  first PAL disc): 3 751 files, 2.83 GB. FPK packs (a simple table and an LZ
  compression, not yet decoded) of NW4R `.brres`, script `.seq` and `.dat`
  tables; NW4R sound (one BRSAR, 1 094 BRSTM streams); eight THP movies,
  each in 4:3 and 16:9. English comes twice, US and UK.
* **The executable measured** (`03-executable.md`): stripped, 3.4 MB,
  745 000 words of code, ~9 900 candidate functions, 1.48% paired singles
  but only 169 quantised accesses, 14 undecodable non-zero words. RVL SDK
  of 2006–07 (IOS 21), NW4R G3D, EF and SND, HBM; no REL modules, no
  third-party middleware. The game's own code is C and C++ (`glib`, `tcg`,
  `eft`, `seq`), about 1.8 MB below 801C0000.
* **Named without symbols**: Dolphin's signature database and Victorious's
  ELF name 1 813 functions of 32 bytes or more, every hook target looked up
  among them (`OSLoadContext`, `OSCreateThread`, `GXInit`, `DVDOpen`,
  `AXInit`, `PSMTXConcat`). Generic destructors give false positives under
  JSystem names: uniqueness and call-graph checks are needed.
* **Input** (`08-input.md`): the game separates slash (a direction) and
  stab (a point) in its own file names. The mouse scheme follows Silver:
  drag for a slash, click for a stab, right button for the shield. Swings
  will be delivered first as synthetic Remote motion (wiikit), proven by a
  Dolphin experiment, then at the game's recogniser.
* **The route** (`06-attack-plan.md`): Victorious's, with a new phase 1
  (the code map of a stripped executable). Seven phases, ten to twelve
  sessions.
* **wiikit** (`10-wiikit.md`): what this port adds to it; and, decided and
  done, its own repository (split from pc-victorious with its history),
  taken as a submodule by both ports. Victorious rebuilt on it, passes its
  self-test 15 of 15 and boots to its main loop.
* Tools: `tools/census.py`, `tools/sigmatch.py`, both headed for wiikit.

Two lessons from other projects applied up front, from The Last Story:
Ghidra needs a Gekko language or it silently drops paired-single
functions; stripped does not mean nameless (RTTI and assertion strings
survive: here `nw4r::g3d::ScnObj`, `glib::Manager<…>` and 87 source file
names).
