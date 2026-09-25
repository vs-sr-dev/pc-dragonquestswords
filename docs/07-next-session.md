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
5. **Dolphin, still open** (`05-open-questions.md` 1-3): do the numpad
   swings land by direction, diagonals, thrust, the wheel, the mouse flick
   with the left button held; must A be held during a swing?
6. The native self-test on the stripped DOL: `sprintf`, `PSMTX*`, `memcpy`
   through names from `names.tsv`.
