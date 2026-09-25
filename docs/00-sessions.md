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

## Session 2 — the code map, and the game boots

Goal: phase 1, the code map of a stripped executable; the first Dolphin
answers on input. It went further: phases 2 and 3, and first light.

Results:

* **Dolphin**: a per-game controller profile (DQS-Swords, loaded only for
  RDQPGD) with swings on the numpad, thrust on 5, F and the wheel, and
  swings from mouse flicks with the left button or Shift held. First
  answers (`08-input.md`): the shield is as expected; **A does not swing,
  it sets the centre** the next swings are directed from. The press of the
  mouse scheme is A.
* **RVZ in wiikit** (`wiikit.rvz`): Dolphin's RVZ and WIA read directly,
  junk regenerated. Every raw region equals DolphinTool's ISO; the whole
  DATA partition extracts from the RVZ to the same 3 759 files, in 57 s.
  The ISO is no longer needed.
* **Function discovery for stripped executables** (`wiikit.recomp.discover`),
  measured on Victorious's DOL against its ELF: 20 612 of 20 619 starts
  found, and no unit cut through a function. The signals were measured
  first: after a terminator, a prologue or a `bl` target is a start 100% of
  the time, a far `b` target 99.3%, a data pointer 70%. Dragon Quest Swords
  has no padding and no alignment between functions (Victorious has both),
  so reachability does the rest: unreached code no branch crosses is a
  function. Switch tables are sized from the code.
* **Names** (`tools/names.py`): hand names with their evidence
  (`tools/names-manual.tsv`) before debug strings (a function that loads
  "WPADInit()" is WPADInit; 36 names) before signatures (1 467). The
  strings corrected the signatures where look-alike functions share one
  (WPAD's callback setters). KPAD, which prints nothing, was named by
  aligning its object's function order with Victorious's: sizes match one
  for one. 26 of the runtime's 47 hooks resolve; the rest are not reached.
* **The stripped DOL recompiles, compiles and links** (phase 2): 8 744
  units, 332 switch tables, no branch to an unknown target; 91 files of
  C++, 53 s with clang, no errors.
* **It boots** (phase 3), after four fixes, three of them in wiikit:
  `RealMode` named; a static constructor behind a tail call found (the
  discovery rule for data pointers); and a PAL boot: the region from the
  disc, VI preset as the IPL leaves it (DCR in PAL, the display
  interrupts). `OSInit` reports "Revolution OS, Kernel built Apr 24 2007",
  the static constructors run, VI, GX, AX, DSP start, five threads, the
  main loop runs.
* **It draws** (phase 4, first light): the Wii Strap screen in English and
  natively 16:9, the Square Enix logo, both right. Then the title screen, a
  3D stage (`stg/038`, the sword model, `tex/title`, the overture playing
  on a silent AX), shows as flat dark blue at about 10 fps: 77 000 GX draws
  a frame, each one an OpenGL draw in the renderer.
* **Dolphin, the rest of the input questions** (`08-input.md`): a slash
  is a direction only, cut the whole length through the centre A set, at
  any speed, diagonals included; A is a press, not held; mouse flicks with
  the left button held slash. The stab is fickle: Swing Forward stabbed a
  couple of times with the aim perfectly still, a Z shake never. The
  hypothesis for session 3: the IR distance falling with the aim held.
* Found on the way: this SDK's `KPADStatus` is 0x84 bytes (the runtime
  assumes Victorious's 0xF0), the game reads 16 samples a frame; the game
  uses the `_gb` packs for English.
* wiikit: `rvz`, `recomp/discover`, `WIIKIT_DISCLOG`, the PAL boot. Every
  change checked on Victorious: its generated C++ unchanged, self-test 15
  of 15, boot to its main loop.
