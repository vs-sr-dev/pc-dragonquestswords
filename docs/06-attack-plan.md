# Feasibility and the porting route

## Verdict

**Feasible, by the same route as Victorious**: static recompilation of the
whole executable to C++, with the Wii SDK replaced at the hardware by
wiikit's runtime. Harder than Victorious in three places, easier in three.

| Harder | Why | Answer |
|---|---|---|
| **A stripped executable** | Victorious's recompiler takes function bounds from symbols and switch-table sizes from data symbols; hooks are by name | function discovery and switch bounds from the code; library names by signature (1 813 on a first try, every hook target among them) |
| **Motion input** | the sword is the Remote: slashes by direction, stabs by depth | a mouse scheme after Silver's (`08-input.md`); swings delivered first as synthetic motion, then at the game's recogniser |
| **A richer 3D renderer** | NW4R G3D, and the game's `glib` with depth of field, glare, HDR, shadow maps, reflection maps: fog, Z-texture copies, more EFB copies than Victorious ever used | the FIFO renderer grows the missing GX features, each reported on first use; Dolphin as the oracle |

| Easier | Why |
|---|---|
| Half the code | 745 000 words, ~9 900 functions (Victorious: 1.66 M, 20 653) |
| No middleware | no Bink, Wwise, Scaleform: the SDK and NW4R only, both of which Dolphin and existing decompilations know well |
| Plain code | C and C++ from one compiler; no REL/RSO; 169 quantised paired-single accesses |

Also new, smaller: an **early SDK** (2006–07; IOS 21) whose AX differs from
Victorious's 2010 one; **THP movies**, decoded by the SDK on the CPU with
the locked cache; **RVZ** images.

## Where to cut

Unchanged from Victorious (`../pc-victorious/docs/06-attack-plan.md`): the
CPU recompiled; graphics at the GX FIFO; audio at the AX micro-code; input
at WPAD/KPAD; files, saves and title at IOS's IPC registers; the OS
scheduler recompiled with only `OSLoadContext` replaced; VI presenting the
XFB; Home Button, Bluetooth and low-level WPAD stubbed.

What changes is how the recompiler and the hooks find their targets:

* **Units**: from discovery, not symbols. Entry points: `__start`, every
  `bl` target, every address a data word points to inside text (vtables,
  callback and command tables: the script interpreter's are the big ones),
  and every word after an unconditional end whose flow no branch reaches
  over. Boundaries: the next entry. Tail calls: an unconditional `b` to an
  entry. To a fixed point, as today.
* **Switch tables**: `lwzx`/`mtctr`/`bctr` with the base from `lis`/`addi`,
  sized from the bounds check before it (`cmplwi rX, N` / `bgt`), not from
  a data symbol.
* **Indirect calls**: every `bctrl` goes through the dispatch table, as
  today; a target not in the table is logged with its caller, and becomes
  an entry on the next recompile. The runtime keeps a list.
* **Names**: a `symbols.tsv` built from signatures (Dolphin's database,
  symbolised ELFs; later the decompilations' symbol lists), plus names given
  by hand. The hook lists stay by name; the recompiler resolves them
  through `symbols.tsv`.
* **Cross-check**: Ghidra with the Gekko SLEIGH language (as The Last Story
  found, the stock PowerPC language drops functions with paired singles)
  for an independent function list; disagreements are read by hand.

## Phases

| # | Phase | Checkable milestone |
|---|---|---|
| 0 | **Analysis** ✅ | disc, executable, libraries, input question, route (session 1) |
| 1 | **Code map** ✅ (session 2; 21 hooks unnamed, none reached so far) | every text word classed (code of a unit, padding, data); `symbols.tsv` with the SDK, NW4R and MSL named; every hook target resolved; switch tables bounded; agreement with Ghidra's function list explained |
| 2 | **Recompiler: coverage** ✅ compiles and links (session 2); the self-test still to port | all units compile and link; the native self-test (the game's `sprintf`, 64-bit division, libm, `qsort`, `PSMTX*`, `memcpy`) passes through addresses from `symbols.tsv` |
| 3 | **Runtime: boot** ✅ to the main loop (session 2) | `__start` to the game's main loop: `OSReport`'s SDK banner, the FPK reads through DVD, the strap screen's frames of GX commands. New: the early AX micro-code, IOS 21, the locked cache's DMA |
| 4 | **Graphics** | the strap and logos, the opening THP (`0_00_2*.thp`), the title, the town, the first battle; fog, Z textures, the `glib` post effects |
| 5 | **Input** | pointer, buttons, shield (as Victorious); then swings: Dolphin experiment, synthetic motion in wiikit, the recogniser found, the gesture delivered there. Target: **the first dungeon, fought with the mouse** |
| 6 | **Audio** | NW4R SND on AX: effects, sequences, voices from BRSTM streams, the movies' sound |
| 7 | **PC finish** | 16:9 (the game has it: `…w.thp`, a SYSCONF at 16:9), internal resolution, key file, the five languages (SYSCONF), saves, the pause box |

Phases 4–6 interleave once the first frame is up, as they did in
Victorious. Victorious took seven sessions for its six phases; this port
should be counted in **ten to twelve**, the difference being phase 1 and
the swing.

## Known risks

* **Hidden entry points.** A function reached only through a pointer that
  discovery missed runs into the "not in dispatch table" path. Mitigation:
  the runtime log turns each into an entry; a data-word scan up front keeps
  them few.
* **Signature false positives.** A wrong name on a hooked function breaks
  boot in confusing ways. Mitigation: hooks only on names matched uniquely,
  over 32 bytes, and confirmed by call-graph (callers and callees agree);
  the hook list checked by hand once.
* **The early AX.** The command list and parameter block of a 2006 AX
  differ from the 2010 one in `ax.cpp`; Dolphin's HLE handles both (its
  "old AXWii") and is the reference. Silence, not a crash, is the symptom.
* **Swing recognition.** Synthetic motion may be rejected or misread for
  diagonals. Mitigation: the Dolphin experiment first; the recogniser read
  in the code second.
* **Renderer breadth.** Depth of field, glare and shadow maps mean Z copies,
  more EFB formats, maybe bounding box and TEV corners Victorious never hit.
  Dolphin frame dumps side by side, one effect at a time.
* **THP on the locked cache.** The SDK's decoder uses `LCQueue` DMA between
  memory and the locked cache; the runtime maps the cache but must also do
  the DMA. Alternative: hook the frame decode and use a host JPEG decoder.
* **Frame rate and timing**: unknown yet whether the game runs at 30 or
  60 fps; battle timing (guards, combos) is frame-based and must hold.
* **Single-precision rounding**, as in Victorious: battle maths could
  notice. Differential runs against Dolphin.

## What is never distributed

Documentation, tools, and wiikit's recompiler and runtime. Generated C++,
game data and anything extracted stay local, produced from one's own disc.
