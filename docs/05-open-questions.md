# Open questions

## Input

1. **The recogniser.** Where does acceleration become "slash at angle θ"
   or "stab"? Does it read KPAD's `acc`/`acc_speed`, or raw WPAD samples at
   200 Hz? How many directions does it distinguish? Does swing speed
   matter?
2. **Does Dolphin's emulated Swing work in this game?** For slashes, yes
   (session 2): mouse flicks (Shift or the left button held) and the
   numpad's eight directions, diagonals included. **The stab does not
   come**: Swing Forward (numpad 5, the wheel) slashes, and so does a shake
   on the Z axis alone (T). Neither of Dolphin's emulated motions makes the
   acceleration the game takes for a push: the recogniser's own test for a
   stab is the answer (question 1), and the first target of the input phase.
   **Hypothesis** (from the game's own description, and how fickle the stab
   was on the Wii): a stab is the Remote *approaching the sensor bar while
   pointing at the same spot*, seen by the IR camera: the two dots spread,
   KPAD's `dist` falls (`dist_vec`, `dist_speed` at 0x4C, 0x50), `pos`
   stays; the least change of aim makes it a slash. Dolphin's swings move
   the aim; the runtime's KPADRead holds `dist` at 2 m, so no stab can come
   from either yet. In the port the stab would be: pointer held, `dist`
   shortened over a few frames.
   *Last test of session 2*: with the mouse perfectly still, Swing Forward
   (F) **did stab, a couple of times**, on no condition the player could
   tell; the Z shake (T) never did. A forward movement is needed (the shake
   goes forth and back), and the stab is rare because the emulated swing
   rarely leaves the aim still: consistent with the hypothesis, not a proof.
3. ~~What A does in battle~~: it sets the centre the swing is directed
   from; a press and a movement, A need not be held (Dolphin, session 2).
   Still open: how is a special move entered?
7b. **The pointer in Dolphin sits above and left of the Windows cursor**
   (same speed, an offset): Dolphin's IR calibration against the game's
   pointer box (`KPADSetPosParam`). An emulator matter; the port maps the
   mouse to the game's pointer one to one, as Victorious does, and checks
   it on the title's menus.
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

10. **Frame rate**: variable, up to 60 at 60 Hz (EuRGB60): the intro runs
    60 in light scenes, 25-35 in heavy ones in the port; the game counts
    time in retraces (session 3). What Dolphin holds in heavy scenes is
    still to see.
11. How the game picks the language on PAL (SYSCONF, or its own save).
    With SYSCONF English it reads `_gb` (session 2).
12. Which `glib` effects are in use in normal play (DOF, glare, HDR,
    shadow, reflection, "DOW"), and what each asks of GX.

## Resolved

* ~~The title screen draws flat blue~~ (13): the locked cache's DMA was
  not emulated, and G3D's view matrices stayed zero (session 3).
* ~~77 000 draws a frame~~ (14): a frame of the intro is 8 000-16 000
  draws of G3D display lists; they cost 90 ms because every vertex upload
  made the GPU wait. A mapped ring fixed it (session 3).
* ~~The early AX~~: the 2007 SDK's AX already has the 2009 command lists
  and parameter blocks (session 3).
