# TODO — session 4

Phase 5, input, now that the game draws, sounds and keeps time
(`00-sessions.md`, session 3). Graphics and speed behind it.

1. **The Master Stroke** (the tutorial asks to raise the Remote and bring
   it down fast; the user's save is there). `Raise Alt` (Left Ctrl,
   acc.z -1) first; if neither sign works, read how the game tells
   "raised": KPAD's `acc`, `horizon`, the pointer leaving the top of the
   screen (`dpd_valid_fg`, `pos.y`), from the input module
   (80014E00-80017400) and KPADRead's caller (800167E8).
2. **The stab**: Dolphin answered everything but the stab (slashes by
   direction only, diagonals, A a press; `08-input.md`). No emulated motion
   stabs, so read the recogniser: from `KPADRead`'s caller (800167E8) to
   where acceleration becomes a slash or a stab, and what it tests for the
   stab: first, whether it reads `dist`/`dist_speed` (KPADStatus 0x48-0x50),
   as the hypothesis says. If so, the stab in the port is the pointer held
   and `dist` shortened, with no motion to synthesise.
3. **The slash from the mouse** works (session 3: `Drag Left`, the
   direction from the pointer as the game takes it). Tune the threshold
   with the user; make it a key-file setting.
4. **The stutter when a heavy scene first appears**: count the programs
   linked then (`WIIKIT_PERF`, the renderer's program count); if it is
   shader compilation, a program cache on disk, or compiling ahead.
5. **The lines on faces**: light or dark lines on some models' faces,
   not always (the hero in the intro too). EFB dump of such a frame,
   against Dolphin's.
6. **Fog** (type 2 at the title, and likely outdoors): wiikit's shader
   generator; Dolphin's frame side by side.
7. The native self-test on the stripped DOL: `sprintf`, `PSMTX*`, `memcpy`
   through names from `names.tsv` (Victorious's `tools/selftest.cpp`).

The port's keys (build/keys.txt, not in the repository): `Shake = Space,
Mouse Middle, Drag Left`, `Raise = Left Shift`, `Raise Alt = Left Ctrl`;
the port should write these defaults itself (its layer, or wiikit's
default key text gaining Drag Left).

wiikit `309832b` (another port's needs: the Classic in WPAD's own samples;
draws in a row merged into one GL call; the disc's files sized from the FST
instead of opened at boot; `WIIKIT_PROFILE=render`) leaves the generated
C++ unchanged; the game boots to its Adventure Logs as before, and no
longer opens every file of the disc at start (an old build sat past its
time limit there while the antivirus scanned them).

wiikit `b9db60f` (`--input keyboard` fixed: windows.h's `INPUT_KEYBOARD`
shadowed it) changes nothing here; the game boots to its menus as before.

wiikit `5a004bf` (another port's need: the Classic Controller, SDL
gamepads, the connect callbacks called for Classic games) leaves the
generated C++ unchanged; the game boots to the adventure-log menu as
before, and now rumbles a plugged-in pad through `WPADControlMotor`
(`WPADIsMotorEnabled` says yes). Its connect callback stays uncalled: it
starts WPAD's own sampling, which crashed on a WPAD never started. A pad
could later drive the Remote here (buttons; a stick as the pointer).

wiikit `cb99bf8` (RG8 and GB8 EFB copies had their two channels swapped;
another port's colour grading found it) draws this game as before; if the
glib post effects (depth of field, glare) ever copy RG8/GB8, they now read
right.

wiikit `a66e681` (another port's needs: display lists and vertex buffers in
MEM2, `mtspr WPAR` emptying the gather pipe, IOS replies delivered after the
call returns, F12 GX trace, `WIIKIT_ICALLS`, an opt-in relative mouse)
changes the generated C++ at the one `mtspr WPAR` (801DAF1C); the game boots
to the adventure-log menu as before. The relative mouse could serve the
sword swings (motion without the pointer leaving the window).

wiikit `a07e7ab` (another port's need: `KPADInitEx` and `KPADReadEx`
hooked) changes nothing here: this 2007 SDK has neither, the generated C++
is unchanged, and the game boots to the adventure-log menu as before.

Housekeeping (2026-09-26, a session of publication only): wiikit is
pushed up to `6fc2304`, whose README now names this port. This repository
is prepared for GitHub: the README says where the port stands and how to
play; with Dolphin's signature database alone (no Victorious ELF) the
same 26 hooks resolve, and that build boots to the Adventure Logs. Four
old commits here pinned wiikit SHAs from before its messages were
reworded (`1a857e5`, `1168fd6`, `2216cd4`, `2733ba3`); they were
repointed to their published twins (the same code) before the first
push, and the repository published at
[vs-sr-dev/pc-dragonquestswords](https://github.com/vs-sr-dev/pc-dragonquestswords).
pc-victorious's unpushed commits were repointed the same way and pushed.

wiikit `688d1bf` (its README names another port, Conduit 2, published
the same day) is documentation only: the submodule moved, nothing to
check.

wiikit `0c71853` (its README names the fourth port, Arc Rise Fantasia,
published the same day) is documentation only: the submodule moved,
nothing to check.

wiikit `d403beb` (GameCube discs and the GameCube's hardware, for a new
GameCube port: the disc drive, ARAM, the controllers on SI, its clocks)
leaves the Wii's paths as they were: checked, this game to its Adventure
Logs with the script above, the same screens as the build before it, side
by side.

wiikit `761b9a7` (the GameCube's AX micro-code, for the GameCube port; the
port's Classic filter also on the GameCube's controllers; WIIKIT_AUDIODUMP's
header written as it goes) leaves the Wii's paths as they were: checked,
this game to its Adventure Logs with the script above, the same screens as
the build before it, side by side, and its sound dumped: the same loudness.

wiikit `0d235b5` (its README names the fifth port, Mega Man X: Command
Mission, published the same day) is documentation only: the submodule
moved, nothing to check.

wiikit `a5e96e5` (RSO modules recompiled with the executable, for the sixth
port, Monster Hunter Tri; WPAD's data format and pointing camera,
`/dev/usb/hid`, the CPU's EFB reads, the AI clock waiting for the DSP's
interrupt) and `9674d07` (its README names that port): checked, this game
to its Adventure Logs with the script above, the same screens as the build
before it, side by side.
