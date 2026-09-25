# Open questions

## Input

1. **The recogniser.** Where does acceleration become "slash at angle θ"
   or "stab"? Does it read KPAD's `acc`/`acc_speed`, or raw WPAD samples at
   200 Hz? How many directions does it distinguish? Does swing speed
   matter?
2. **Does Dolphin's emulated Swing/Thrust work in this game?** Partly
   answered (session 2): **yes, from mouse flicks**. Shift held plus a flick
   of the mouse, fed to Dolphin's Swing, slashes in the game. Still open:
   the numpad's fixed directions, diagonals, thrust (5, F, the wheel), and
   the same flick with the left button held (A) instead of Shift.
3. ~~What A does in battle~~: it sets the centre swings are directed
   from (Dolphin, session 2). Still open: must A be held during the
   swing, or does one press set the centre until the next? How is a
   special move entered?
4. **Remote orientation**: does the game use roll (the pointer's angle) or
   tilt anywhere, e.g. for the shield?
5. **Are the debug mini-games reachable** (`mini_debug_slash/stab/darts`)?
   A lab for tuning the mouse.
6. Rumble: `WPADControlMotor` is called from the game; keep it for pads.

## Data

7. The FPK compression (`01-disc-layout.md`) and the header's two unknown
   words.
8. `.seq` bytecode: the interpreter is `seq_cmd*.c`; needed only to
   understand scripts.
9. The four THP pairs named but absent: what plays in their place?

## Code

10. **Frame rate**: 30 or 60 fps, fixed or variable? (The logos run at
    the retrace rate; the title is too slow to tell.)
13. **The title screen draws flat blue**: what does Dolphin show there, and
    which GX feature is missing (fog, Z textures, EFB formats, TEV)?
14. **77 000 draws a frame** at the title: a particle system, or display
    lists replayed per object? Batching in the renderer, as Dolphin does.
11. How the game picks the language on PAL (SYSCONF, or its own save).
    With SYSCONF English it reads `_gb` (session 2).
12. Which `glib` effects are in use in normal play (DOF, glare, HDR,
    shadow, reflection, "DOW"), and what each asks of GX.

## Resolved
