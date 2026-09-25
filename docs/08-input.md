# Input: the Remote in this game, and the mouse

Victorious needed a pointer, two buttons and a shake. Dragon Quest Swords is
the opposite case: the sword *is* the Remote. This is the port's design
problem, and the place where it can be better or worse than the original.

## What the game asks of the Remote

From play knowledge; every line to be confirmed in the code and in Dolphin
(`05-open-questions.md`).

| Action | On the Wii | Notes |
|---|---|---|
| Aim | the pointer (IR) | always on in battle; the cursor is where a stab lands |
| **Slash** | swing the Remote | the swing's direction sets the cut's angle on screen (horizontal, vertical, diagonals); the game draws the arc |
| **Stab** (thrust) | push the Remote forward | lands at the cursor: the "depth" move, for weak points and some enemies |
| **Shield** | hold B | the cursor becomes the shield and follows the pointer; blocks what it covers |
| **A** | sets the centre | *seen in Dolphin, session 2*: A does not swing; it sets the point the next swings are directed from. The shield (hold B, the pointer moves it) behaves as expected |
| Special moves | a gauge, then a swing | `game/special_info.dat`; the shouts are streams (`zettai`, `syakunetsu`…) |
| Walk the rails, forks | d-pad / pointer | on rails: stop, turn back, choose a branch |
| Menus, town, shops | pointer + A, B back | as in Victorious |
| Mini-games | slash and stab patterns, darts, a lottery | `mini/slash_pattern0.dat`, `mini/stab_pattern.dat`, `mini_debug_darts.seq`, `mini_fukubiki.seq` |

The names in the executable already separate the two sword gestures:
`slash` and `stab` have their own pattern files and their own debug
scripts. A slash is a direction, a stab is a point. That split is what the
mouse scheme has to give.

## The model: Silver

Silver (PC, 1999) fights with the mouse: hold a modifier, then **click
without moving for a jab**, **hold the left button and drag** left, right,
forward or back for a swipe, lunge or backslash; the right button is the
shield (hold) or a dodge (tap). (`../PC-Silver-RE`: the scheme from the
manual; its thresholds were never reverse-engineered.)

It maps onto this game almost term for term, and better than on Silver,
because here the cursor is already on screen:

## The proposed scheme

| Mouse | Game | Why |
|---|---|---|
| move | the pointer | one to one, as in Victorious; the game's cursor, drawn by the game |
| **left button: press, drag, release** | **A at the press** (the game's own centre), then a **slash** along the drag | the game already anchors swings at a point set by A: the press *is* A, the drag is the swing. The scheme and the game agree term for term |
| **left button: click without dragging** | **stab** at the cursor | Silver's jab; a point is what a stab needs |
| right button, held | B: the shield, moved by the mouse | the game's own behaviour, unchanged |
| wheel forward (option) | stab | the "depth" axis, for players who want click-and-drag for slashes only |
| Space | A alone (confirm in menus; re-centre without swinging) | |
| W A S D, arrows | d-pad (rails, forks) | |
| Esc | the port's pause box, as in Victorious | |

Details to settle by playing, each a setting:

* **Fire on threshold, not on release.** A slash fires the moment the drag
  passes a distance (say 40 px at 1080p, scaled to the window) within a
  time (say 250 ms), with the direction measured then. Waiting for the
  release adds the player's own hesitation to the latency.
* **Does the cursor move during a drag?** On the Wii the pointer moves with
  the swing. With a mouse, a frozen cursor during the drag (the drag is the
  gesture, the aim stays) keeps aim and gesture from fighting. Both, as an
  option; the frozen cursor as the likely default.
* **Diagonals and angles**: the drag gives any angle. The game may quantise
  to 4 or 8; the recogniser decides (below).
* **Strength**: if the game grades a swing's speed, drag speed maps to it.
* Left-handed: swap the buttons, as Silver did.

A gamepad fits the same model later: the right stick flicked is a slash
(Skyward Sword HD's button-only mode on Switch is the precedent), a trigger
is the stab, the left stick the pointer.

## Two ways to deliver a swing

**1. Synthesise the Remote's motion (wiikit, game-agnostic).** The port
already fills `KPADStatus` from the mouse. For a swing it can also fill the
accelerometer: gravity plus a short pulse along the gesture's direction, in
the Remote's frame (speed up, then brake, some 100–150 ms, peaks of a few
g), into `acc`, `acc_value`, `acc_speed` and the raw WPAD samples. This is
what Dolphin's emulated Remote does with its *Swing* (up, down, left, right,
forward, backward) and *Shake* inputs, and it is game-agnostic: every Wii
game with waggle could use it. It needs no knowledge of the recogniser, but
costs the pulse's duration in latency and may miss what the recogniser
wants for diagonals.

**2. Deliver the gesture where the game recognises it (this port's
layer).** Read the recogniser: from the input module (80014E00–80017400)
to the code that turns acceleration into "slash at angle θ, strength s" or
"stab", then inject that result directly from the mouse gesture. Exact
angles, no pulse latency, no guessing. Costs reverse engineering in
nameless code.

**The plan uses both, in that order.** 1 first, because it is cheap, it
belongs in wiikit, and **Dolphin tells us on day one whether it works**:
bind Dolphin's emulated Swing and Thrust to keys, play the first battle.
If the game accepts them, the synthetic route is proven before a line of
port code. Then 2, when the recogniser is found, for precision and latency.
The recogniser's thresholds, read in 2, also tune 1.

## Why not a pure reimplementation of the controls

A port could bypass all of this by rewriting the battle input in C++. It
would drift from the game's own rules (guard timing, weak points, specials)
in ways that only show late. Driving the game's own recogniser, or its
output, keeps the game's rules as they are.
