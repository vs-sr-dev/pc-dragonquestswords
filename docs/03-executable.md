# The executable

`main.dol`, 3.4 MB, entry `0x80006124`, BSS `0x80344700`+`0x14BAC0`.

| Section | Range | Size |
|---|---|---|
| T0 | 80004000–800064E0 | 9 KB (`__start`, init, runtime asm) |
| T1 | 80006840–802DB860 | 2.83 MB |
| D0–D7 | 800064E0…804901A0 | ~0.4 MB data, ~1.3 MB BSS |

**Stripped**: no symbols, no map. Against Victorious (20 619 named
functions in a shipped ELF) this is the one real change of problem.

## What is linked

From the version strings (`<< RVL_SDK - X release build: … >>`):

| Library | Build | Notes |
|---|---|---|
| RVL SDK OS, DVD | Apr 24 2007 | |
| EXI, SI, VI, GX, AI, DSP, SC, NAND, THP | Nov 30 2006 | an early SDK: Victorious's is 2010 |
| AX | Dec 18 2006 | the early AX: its micro-code and command list differ from Victorious's (`06-attack-plan.md`, risks) |
| WPAD, KPAD | May 17 2007 | Bluetooth stack (BTE, WUD) linked in full |
| HBM | Oct 22 2007 | the Home Button menu, `home/homebtn_*.arc` |
| NW4R G3D, EF | Jun 7 2007 | models, scenes, particles |
| NW4R SND | (no version string) | `Sound3DListener.h`, `0001.brsar` |
| MSL C, Runtime, TRK | CodeWarrior | |

No third-party middleware: no Bink, Wwise, Scaleform, CRI. Everything above
the SDK and NW4R is the game's own code, in C and C++ (source names from
assertions: `glib_*.cpp`, the 3D layer over NW4R, with depth of field,
glare, HDR, shadow maps, reflection maps and "DOW"; `tcg_*.c`, the 2D and
text system; `n2d_main.c`; `eft_*.c`, effects with their own script
commands; `seq_cmd*.c`, the script interpreter; `game_message.c`;
`slib_file.c`; `clinklist.cpp`).

## Size and shape of the code

`tools/census.py`:

* **744 768 words** of text (Victorious: 1.66 million), 168 distinct
  operations; only **14 non-zero words** fail to decode (data inside text),
  so wiikit's decoder covers this compiler's output as it did Victorious's.
* **Paired singles 1.48%** (Victorious 0.86%): 8 292 `psq_*`, of which
  8 123 use GQR0 (plain float pairs: NW4R math, PSMTX). **169 quantised**,
  on GQRs 2, 3, 5, 6, 7: the cost Victorious found in quantised loads is
  small here.
* **6 576 distinct `bl` targets** (43 492 calls), 5 585 `stwu r1`
  prologues, 2 581 `bcctr`. Adding the entry after every `blr` gives **9 901
  candidate functions**: about half Victorious's count.
* The locked cache is used (`LCEnable`, `LCStoreBlocks`, `LCQueueWait`,
  `DCZeroRange`), as the THP decoder does.

## Naming without symbols

`tools/sigmatch.py` hashes each candidate function with Dolphin's
signature checksum (opcodes and registers kept, immediates and targets
masked) and looks it up in Dolphin's `Sys/totaldb.dsy` (10 549 SDK and
library signatures) and in Victorious's symbolised ELF.

* All sizes: 3 147 matches. With a floor of 32 bytes: **1 813 names**
  (1 701 from Dolphin's database, 112 more from Victorious).
* By library: BTE 591, HBM 169, GX 123, OS 101, DVD 75, MSL 56, NAND 39,
  WUD 38, SC 29, MTX 27, WPAD 27, VI 26, IPC 26, TRK 25, EXI 22, FS 20…
* Every function Victorious's runtime hooks by name that was looked up is
  found: `OSLoadContext` 801DDD18, `OSCreateThread` 801E4B3C, `GXInit`
  801F0AB0, `DVDOpen` 801F89A4, `AXInit` 801FFC14, `PSMTXConcat` 801EEE08.
  (A `KPADInit` at 801E6208, from the pass without a size floor, sits in the
  OS code far from the rest of KPAD: a collision, not a name.)
* **Noise**: 62 hits name JSystem's J3D (not in this game). They are
  generic C++ destructors and constructors, one name at a dozen addresses.
  Rule for the real tool: a name matching more than one address is
  ambiguous and dropped; small functions need a call-graph check (callers
  and callees consistent with the name).
* The hits cluster in **801C0000–802D0000**: the SDK, NW4R and MSL. The game's
  own code is below, **80006840–~801C0000, about 1.8 MB**, and will stay
  nameless except where the port needs a name (input, the gesture
  recogniser, the frame loop), given by hand as in any RE project.
* Not found by signature (versions differ): `KPADRead`, `WPADRead`,
  `VIInit`, `__start` (at the entry, known). Session 2 named them other
  ways (below).

## Discovery and names (session 2)

`python -m wiikit.recomp build/extract/sys/main.dol --symbols build/names.tsv`
finds 8 744 units (`wiikit/recomp/discover.py`), sizes 332 switch tables
from the code (3 unresolved) and leaves no branch to an unknown target.
No padding and no alignment separate functions here (starts are spread
evenly mod 16; Victorious aligns most to 16 with zero padding), so
reachability does most of the work.

`tools/names.py` writes `build/names.tsv` from three sources, most trusted
first: `tools/names-manual.tsv` (each name with its evidence), debug
strings (36 names: WPAD, WUD, DVD, OS print their own names), signatures
(1 467). Where they disagree the string wins: WPAD's three callback
setters have one signature between them.

KPAD prints nothing. Its functions follow its object's order, which is
Victorious's order with the newer functions missing, and sizes that match
one for one (`select_2obj_first` 488, `select_2obj_continue` 552,
`clamp_stick_circle` 296...): `KPADRead` 802260A4, `KPADInit` 802267BC,
`KPADReset` 80226B18. The game calls `KPADRead(chan, buf, 16)` at 800167E8.
This SDK's `KPADStatus` is **0x84 bytes** (Victorious's 0xF0); the fields
the runtime writes, up to 0x5F, are at the same offsets.

## Landmarks

* **The game's input module**, about 80014E00–80017400: it calls
  `KPADSetPosParam` for four channels, `WPADControlMotor`,
  `WPADGetRadioSensitivity`, `WPADSetExtensionCallback`. Another
  `KPADSetPosParam` caller at 80106A4C, `WPADControlMotor` callers at
  80107ADC–80107DF8 (rumble on hits, probably).
* Strings name the swing data: `mini/slash_pattern0.dat`,
  `mini/stab_pattern.dat`, `mini/mini_debug_slash.seq`,
  `mini/mini_debug_stab.seq`, `game/special_info.dat`, `eft/shield/%04d`.
