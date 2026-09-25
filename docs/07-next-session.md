# TODO — session 4

Phase 5, input, now that the game draws, sounds and keeps time
(`00-sessions.md`, session 3). Graphics and speed behind it.

1. **To the first battle.** The new game from the save "ABC": the mouse
   on the menus and the town (the pointer one to one, as in Victorious),
   then the first fight. Every screen checked against Dolphin with the
   capture script; what differs becomes a GX item below.
2. **The stab**: Dolphin answered everything but the stab (slashes by
   direction only, diagonals, A a press; `08-input.md`). No emulated motion
   stabs, so read the recogniser: from `KPADRead`'s caller (800167E8) to
   where acceleration becomes a slash or a stab, and what it tests for the
   stab: first, whether it reads `dist`/`dist_speed` (KPADStatus 0x48-0x50),
   as the hypothesis says. If so, the stab in the port is the pointer held
   and `dist` shortened, with no motion to synthesise.
3. **The slash from the mouse**: synthetic motion in wiikit (a pulse along
   the drag, `08-input.md`), or the recogniser's own result once found.
4. **The stutter when a heavy scene first appears**: count the programs
   linked then (`WIIKIT_PERF`, the renderer's program count); if it is
   shader compilation, a program cache on disk, or compiling ahead.
5. **Fog** (type 2 at the title, and likely outdoors): wiikit's shader
   generator; Dolphin's frame side by side.
6. The native self-test on the stripped DOL: `sprintf`, `PSMTX*`, `memcpy`
   through names from `names.tsv` (Victorious's `tools/selftest.cpp`).

Housekeeping: wiikit `fbdff55`..`5b66083` and pc-victorious `3f58adc`..
`fc2f401` are committed locally, not pushed. wiikit is public and must not
name this port (the commit messages say "a stripped PAL game"); push when
the user says so, after the path audit.
