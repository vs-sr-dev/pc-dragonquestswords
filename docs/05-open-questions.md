# Open questions

## Input

1. **The recogniser.** Where does acceleration become "slash at angle θ"
   or "stab"? Does it read KPAD's `acc`/`acc_speed`, or raw WPAD samples at
   200 Hz? How many directions does it distinguish? Does swing speed
   matter?
2. **Does Dolphin's emulated Swing/Thrust work in this game?** If so, how
   well on diagonals: the cheapest experiment of the project.
3. **What A does in battle** (special moves only, or a focus or lock-on too),
   and how a special move is entered.
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

10. **Frame rate**: 30 or 60 fps, fixed or variable?
11. How the game picks the language on PAL (SYSCONF, or its own save),
    and whether `_us` or `_gb` is used for English.
12. Which `glib` effects are in use in normal play (DOF, glare, HDR,
    shadow, reflection, "DOW"), and what each asks of GX.

## Resolved
