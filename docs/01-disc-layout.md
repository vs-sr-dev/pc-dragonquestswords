# The disc

European release, **RDQPGD**, "DRAGON QUEST SWORDS", disc 0, revision 0.
The image used is a Redump-verified RVZ (zstd level 19, 128 KiB blocks),
converted to ISO with Dolphin's `DolphinTool convert` (1 min), then read by
`wiikit.disc` (53 s). Checked against the owner's retail disc (PAL, the
cover and label match).

| Partition | Offset | Title | Size | Notes |
|---|---|---|---|---|
| UPDATE | 0x50000 | 0001000000555050 | 183 MB | system update, ignored |
| DATA | 0xF800000 | 0001000052445150 | 4425 MB | the game |

The TMD asks for **IOS 21** (Victorious: IOS 56).

## sys/

| File | Size |
|---|---|
| `main.dol` | 3 435 904 |
| `apploader.img` | 214 492 |
| `fst.bin` | 106 156 |
| `boot.bin`, `bi2.bin` | |

There is no ELF, no map file, no `.rel`, `.rso` or `.sel` anywhere: the
executable is the whole game (`03-executable.md`).

## files/ — 3 751 files, 2.83 GB

| Path | Files | Size | What |
|---|---|---|---|
| `str/` | 16 `.thp` | 1.3 GB | eight movies, each twice: `…n.thp` (4:3) and `…w.thp` (16:9) |
| `sound/0001.brsar` | 1 | 162 MB | NW4R sound archive: effects, music sequences, banks |
| `sound/strm/` | 1 094 `.brstm` | 257 MB | NW4R streams: voices per scene (`e_2_08_*`, `e_bt_02_*`, `SE_EV*`), special-move shouts (`senkourekkazuki04_32`, `syakunetsu04_32`, `zettai03_32`), music (`ME_*`) |
| `fpack/` | 1 163 `.fpk` | ~730 MB | the game's packs, language-neutral |
| `_us/ _gb/ _fr/ _de/ _es/ _it/` | 246 `.fpk` each | ~47 MB each | localised packs, same tree in each |
| `opening.bnr` | 1 | | the channel banner |

`fpack/` by folder: `chr` 314 (characters, the sword models), `enemy` 248,
`hard_enemy` 206 (the post-game's harder variants, 212 MB), `stg` 179
(stages), `tex` 72, `story` 54, `eft` 50 (effects, the shield), `camera` 12,
`game` 13 (`T0`…`T18`), `mini` 12 (mini-games), `cmn` 3. The localised
trees hold `cmn eft enemy game hard_enemy mini stg story tex`, the parts
with text or text-bearing textures.

## FPK

A flat pack. Big-endian:

    0x00  u32   ?                 (0xC8AE, 0x9720: not the file size; a checksum or id)
    0x04  u32   count
    0x08  u32   0x10              header size
    0x0C  u32   ?                 (varies; the total unpacked size?)
    0x10  entries[count], 0x30 bytes each:
          char  name[0x20]        full path, e.g. "stg/cmn/2003.brres", "mini/mini_debug_slash.seq"
          u32   offset
          u32   packed size
          u32   unpacked size
          u32   ?                 (0, or 0x31xx…: a flag or hash; to check)

The data is compressed with a byte-oriented LZ: a flag byte, then literals
and back-references (`fe 62 72 65 73 fe ff 00 30 …` unpacks to `bres…`).
Not yet decoded; the recompiled game unpacks it itself, so the port does not
need it, but asset inspection and modding do.

What the packs hold, from their names: NW4R `.brres` (models, textures,
animations: standard, readable by existing tools), `.seq` (the game's
script bytecode, run by `seq_cmd*.c`), `.dat` tables (`game/special_info.dat`,
`mini/slash_pattern0.dat`, `mini/stab_pattern.dat`).

## Movies

`str/` scene numbers match the script's chapter numbering (`0_00`, `0_06`,
`5_07`, `7_05` ×2, `7_06`, `7_10`, `8_11`). The executable names twelve
pairs; four are not on the disc (`04-curiosities.md`). Both aspect ratios
exist for every movie: the game chooses by the console's setting, so a
SYSCONF at 16:9 (as Victorious writes) gives widescreen movies too.
