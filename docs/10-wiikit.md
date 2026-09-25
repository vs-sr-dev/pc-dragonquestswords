# This port and wiikit

wiikit grew inside pc-victorious and, since this port began, is its own
repository ([vs-sr-dev/wiikit](https://github.com/vs-sr-dev/wiikit)), taken
here as a submodule at `wiikit/`. This port is its second user, and the
first with a stripped executable. Most of what session 1 found missing is game-agnostic and
belongs in wiikit, not here.

## What this port uses as it is

`wiikit.disc` (read the PAL disc at the first try: 3 751 files), `dol`,
`ppc` (14 undecoded non-zero words in 745 000), `gxtex`, `tpl`, `u8`, `dsp`;
and, later, the recompiler's emitter and the whole runtime: OS, IOS, GX
renderer, AX, WPAD/KPAD, SYSCONF, `wiiboot`.

## What it will add to wiikit

| Addition | Layer | Why it is not game knowledge |
|---|---|---|
| RVZ (and WIA) reading in `disc` | 1–2 | Dolphin's own format, and how most dumps are kept today. Python 3.14 has zstd in the standard library; LZMA and bzip2 were already there; the junk-data generator is documented |
| `ppc --mix` without symbols | 3 | `tools/census.py` |
| `sig`: signatures from Dolphin's `.dsy`, from any symbolised ELF, from decompilations' symbol lists; uniqueness and call-graph checks | 3 | `tools/sigmatch.py` |
| function discovery for stripped executables | 4 | entry points from calls, data pointers, flow; units without symbols |
| switch tables bounded by their compare | 4 | |
| hook lists resolved through a `symbols.tsv` | 4 | any stripped game |
| ~~the early AX micro-code~~ not needed: this 2007 SDK's AX has the later lists and PBs (session 3) | 5 | |
| locked-cache DMA ✅ `fbdff55` (G3D's view matrices; session 3) | 5 | the THP decoder, and any game using `LC*` |
| synthetic Remote motion (swing, thrust, shake) from mouse gestures | 5 | any Wii game with waggle |
| fog, Z textures, more EFB copy formats | 5 | any 3D game |
| BRSAR/BRSTM, THP readers | 2 | NW4R and SDK formats |

Also added in session 3, found on the way: a frame's GX commands, EFB
stages and draws as files (`WIIKIT_GXTRACE`, `WIIKIT_EFBDUMP`,
`WIIKIT_DRAWLOG`), AX voices per frame (`WIIKIT_AXTRACE`); the vertex ring
mapped and XF in a uniform block; `KPADStatus`'s size per SDK; audio
without gaps under load (the record handed over outside the hardware lock,
interrupts taken while waiting for the renderer, the AI waiting for its
mix); VI timing from its registers and the EuRGB60 boot; draw-done raised
when the renderer reaches it.

FPK, `.seq`, the recogniser's hook and the mouse scheme's tuning stay here.

## Where wiikit lives

Decided in session 1 (way C). Two projects now write to it; the three ways
weighed:

| Way | For | Against |
|---|---|---|
| A. Keep it in pc-victorious; this port imports it by path and commits there | nothing to set up | changes for another game land in Victorious's history; a change for Dragon Quest Swords can break Victorious unnoticed; a third port makes it worse |
| B. Copy it here | independent | two copies that drift: exactly what to avoid |
| **C. Its own repository, a submodule in each port** | one copy, its own history and tests, each port pinned to a known version and moved on deliberately; publishable on its own, like ps2kit | one setup step now |

**Done: C.** `git subtree split --prefix=wiikit` in pc-victorious carried
its seven commits over, the tree identical at the split; the new
repository's README took over Victorious's `docs/10-wiikit.md` (layers,
checks, gaps), which is now a pointer; the profiler's resolver, being
game-agnostic, moved in as `python -m wiikit.profile`. Both ports take it
as a submodule at `wiikit/`, so `python -m wiikit…` works from each root,
and `tools/*.py` put the root on their path. Victorious was checked on the
submodule: the whole build rebuilt, the self-test 15 of 15, the boot to
`CGame::run`. wiikit is published at
[vs-sr-dev/wiikit](https://github.com/vs-sr-dev/wiikit), and pc-victorious's
`main` takes it from there: a fresh `git clone --recursive` of Victorious
checks out and runs it.

Rules that carry over: pure Python for layers 1–4, C++20 + SDL3 for the
runtime; every claim checked on a real disc; game knowledge stays out. One
added: **every change is checked on both games** before it goes in (Victorious
still boots and plays; this port still gets as far as it did).
