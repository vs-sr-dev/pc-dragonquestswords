# TODO — session 3

Phase 4, graphics, with Dolphin next to the port; input and audio behind.

1. **The title screen.** Dolphin's frame of the title next to the port's
   flat blue: which GX feature is missing or wrong (fog, Z-texture copies,
   EFB copy formats, TEV corners). `WIIKIT_TEXDUMP`/`WIIKIT_SHADERDUMP`, and
   Dolphin's FIFO player on one frame of the title if needed.
2. **77 000 draws a frame**: see what they are; batch consecutive draws
   with the same state in the renderer, as Dolphin does (wiikit).
3. **KPADStatus per SDK** (wiikit): the size from the port (0x84 here),
   so KPADRead fills this game's samples exactly; then the mouse on the
   title's menus.
4. **The early AX** (wiikit): the overture already plays on a silent AX;
   the 2006 command list, with Dolphin's old AXWii as the reference.
5. **The stab**: Dolphin answered everything but the stab (slashes by
   direction only, diagonals, A a press; `08-input.md`). No emulated motion
   stabs, so read the recogniser: from `KPADRead`'s caller (800167E8) to
   where acceleration becomes a slash or a stab, and what it tests for the
   stab: first, whether it reads `dist`/`dist_speed` (KPADStatus 0x48-0x50),
   as the hypothesis says. If so, the stab in the port is the pointer held
   and `dist` shortened, with no motion to synthesise.
6. The native self-test on the stripped DOL: `sprintf`, `PSMTX*`, `memcpy`
   through names from `names.tsv`.
