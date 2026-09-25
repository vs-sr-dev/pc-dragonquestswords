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

## Session 3 — the game in 3D, in time with its music

Goal (`07-next-session.md` of session 2): the flat blue title, the 77 000
draws, `KPADStatus`, the early AX. It went through graphics, speed, the
first menus and the sound, with Dolphin beside the port and the user
listening.

Results:

* **Dolphin as the reference, from here**: a script starts Dolphin on the
  RVZ and captures its window at given seconds. What the port called "the
  title" is an in-engine intro first (the hero on a tower, the throne
  room), then the logo on white, then "PRESS A+B".
* **Every model was drawn through zero matrices** (`WIIKIT_GXTRACE`,
  `WIIKIT_EFBDUMP`, `WIIKIT_DRAWLOG`, new in wiikit, showed 16 000 draws
  leaving no trace, and XF position and normal matrices of 0). NW4R G3D
  computes view matrices in the locked cache and stores them back with
  `LCStoreBlocks`; the runtime ignored `mtspr DMA_L`. With the DMA
  (wiikit `fbdff55`) the intro and the title match Dolphin, natively 16:9.
* **10 fps to the game's own rate** (wiikit `4a6caf6`): the GPU waited on
  a copy between every two draws (vertices uploaded with `glBufferSubData`
  into a buffer in use). The vertex buffer is a ring mapped once, fenced in
  quarters; XF moved from a storage buffer to a uniform block. Not
  fill-rate: the same at 1x. `WIIKIT_PERF` reports the time presenting.
* **The port's own layer**, `tools/dqs.cpp` (`tools/dqs.cmake`, CMake's
  `WIIKIT_EXTRA`): this SDK's `KPADStatus` is 0x84 (wiikit `10eb63f`,
  `wpad_set_kpad_status_size`). A+B passes the title; with an empty NAND
  the game says so, creates a save (name, handedness) and starts the new
  game's narration ("The world was at peace.").
* **The AX is not the early one**: its command lists and parameter blocks
  are the 2009 layout wiikit already mixes (a PB dump: addresses at 57–62,
  ADPCM at 56, coefficients from 63; list SETUP, ADD_TO_LR, PBS,
  COMPRESSOR, WM, OUTPUT, END). The sound played from session 2 on; it
  crackled and ran out of time with the picture. Four causes, found one
  under the other:
  1. the game's thread handed the GX record to the renderer **holding the
     hardware lock**, and waited there: AI blocks started late (wiikit
     `8dc0d4f`: handed over outside the lock);
  2. waiting there it took **no interrupts**, and the AI dropped every
     block left without a new AX frame: 3 ms gaps. It now takes its
     interrupts while it waits; the AI waits for the mix (up to 50 ms) and
     catches up. The speed correction of the host stream is held to 0.5%
     (2% after a stall): a drained queue had pulled it to −0.8%, heard as
     a lower pitch (`1c5834b`);
  3. **the intro ran 20% fast against the music**: the game chose PAL
     50 Hz (VTR `1085`, HTR0 `4B6A01B0`) because the boot left the TV mode
     at PAL (0x800000CC = 1), while the clock made 59.94 retraces a second.
     The game picks 60 Hz only if `VIGetTvFormat()` is EuRGB60 (8001D01C;
     progressive first, if SYSCONF and the cable allow). The boot now
     writes 5 when SYSCONF's `IPL.E60` is set, as the IPL does, and the
     clock takes the field's length from the VI registers (50 Hz PAL,
     59.94 NTSC and EuRGB60). The game then runs 480 lines at 60 Hz, as in
     Dolphin with PAL60 (`5b66083`);
  4. **the last clicks were in the stream itself**, on AX frame boundaries
     (the stream's position unchanged across them: stale buffer, not lost
     frames). Draw-done was answered at once, so a game ahead of the
     renderer waited inside a FIFO store while the guest OS thought it ran,
     and the thread that reads the stream from the disc starved. PE's
     finish interrupt now comes when the renderer reaches the draw-done
     point: the game sleeps in `GXWaitDrawDone`, as with a real GP. A 60 s
     recording went from 30 clicks to none; the user hears the beats on
     the camera cuts, as in Dolphin.
* **The frame rate is not fixed**: the intro runs up to 60 fps in light
  scenes and 25–35 in heavy ones, on the retrace clock; the game measures
  time in retraces, so the speed is right either way.
* Every wiikit change checked on Victorious: generated C++ unchanged but
  for the one `mtspr DMA_L`, self-test 15 of 15, 30 fps, its audio queue
  at 20 ms, drawn as before. Its submodule follows (`fc2f401`).
* Left: one stutter when a heavy scene first appears (likely shaders
  compiled on first use); fog (type 2) is not drawn.

Later in session 3, with the user playing the port:

* **The game plays**: the town, the tutorial's battle - field - battle
  cycle; audio and video right but for faint light or dark lines on some
  faces (also on the hero in the intro), not always.
* **Swings from the mouse** (wiikit `93cfa20`): the user found that the
  game takes a slash's direction from the pointer's movement and the
  acceleration only as the trigger (Space, a shake, while moving the mouse
  slashed that way). A new key-file source, `Drag Left`, is the left
  button held with the mouse moving faster than 1.5 window heights a
  second (held 120 ms): `Shake = Space, Mouse Middle, Drag Left` gives
  "click to set the focus, drag to slash", with no slash from slow
  movement. Confirmed by the user: slashes "much better".
* **The Remote's speaker** is mixed into the TV's sound (the shield's
  parries were silent): confirmed.
* **The movies play** (`str/0_00_2w.thp`, with Fleurette's voice-over):
  THP's decoder checks HID2's locked-cache enable on its own thread, and
  the runtime kept HID0/1/2/4, WPAR and the DMA pair per guest thread; the
  OS saves only GPRs, FPRs, CR, LR, CTR, XER, GQRs and SRRs, the rest are
  the CPU's (`g_ppc_spr`). Found with `--watch` (the decode thread
  suspending itself after `THPVideoDecode`, 802133E0, failed) and
  `WIIKIT_DISCLOG=all` (ten frames read, then none). Confirmed by the user.
* **Not yet: the Master Stroke** (raise the Remote, swing down). `Raise`
  (Left Shift: acc.z +1, the pointer off the screen) is not recognised;
  `Raise Alt` (Left Ctrl, acc.z -1) is untested.
