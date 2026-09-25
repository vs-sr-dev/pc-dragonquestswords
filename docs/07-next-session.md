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

wiikit `2216cd4` (RG8 and GB8 EFB copies had their two channels swapped;
another port's colour grading found it) draws this game as before; if the
glib post effects (depth of field, glare) ever copy RG8/GB8, they now read
right.

wiikit `2733ba3` (another port's needs: display lists and vertex buffers in
MEM2, `mtspr WPAR` emptying the gather pipe, IOS replies delivered after the
call returns, F12 GX trace, `WIIKIT_ICALLS`, an opt-in relative mouse)
changes the generated C++ at the one `mtspr WPAR` (801DAF1C); the game boots
to the adventure-log menu as before. The relative mouse could serve the
sword swings (motion without the pointer leaving the window).

wiikit `1168fd6` (another port's need: `KPADInitEx` and `KPADReadEx`
hooked) changes nothing here: this 2007 SDK has neither, the generated C++
is unchanged, and the game boots to the adventure-log menu as before.

Housekeeping: wiikit `93cfa20` (global SPRs, Remote speaker, drag and
raise keys, disc log) is committed locally, not pushed (up to `5b66083`
is on GitHub); pc-victorious `3f58adc`..`c4c0292` are local. wiikit is
public and must not name this port; push when the user says so, after
the path audit.
