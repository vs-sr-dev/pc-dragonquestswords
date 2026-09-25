"""Instruction census of an executable without symbols.

`wiikit.ppc --mix` walks sized function symbols, so on a stripped DOL it has
nothing to count. This walks the text sections word by word instead: the
operation mix, paired singles and their GQRs, undecoded words, and a first
count of call targets and stack-frame prologues. Meant to become the
symbol-less path of `wiikit.ppc --mix`.
"""
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # wiikit/

from wiikit.dol import Image
from wiikit.ppc import branch_target, decode


def main():
    img = Image(sys.argv[1])
    ops = collections.Counter()
    gqr = collections.Counter()
    undecoded = []
    calls = collections.Counter()
    prologues = 0
    total = 0
    text = [(s.vaddr, s.vaddr + len(s.data)) for s in img.text_segments()]
    for s in img.text_segments():
        for i in range(0, len(s.data) - 3, 4):
            a = s.vaddr + i
            w = struct.unpack_from(">I", s.data, i)[0]
            ins = decode(w)
            total += 1
            if ins.op == ".long":
                if w:
                    undecoded.append((a, w))
                continue
            ops[ins.op] += 1
            if ins.op.startswith("psq"):
                gqr[ins.f.get("I")] += 1
            elif ins.op == "b" and ins.f["LK"]:
                t = branch_target(ins, a)
                if any(lo <= t < hi for lo, hi in text):
                    calls[t] += 1
            elif ins.op == "stwu" and ins.f["D"] == 1 and ins.f["A"] == 1:
                prologues += 1
    ps = sum(n for o, n in ops.items() if o.startswith(("ps_", "psq_", "dcbz_l")))
    print(f"{total} words, {len(ops)} operations, {len(undecoded)} non-zero words undecoded")
    print(f"paired-single {ps} ({100 * ps / total:.2f}%); psq_* by GQR: {dict(sorted(gqr.items()))}")
    print(f"{len(calls)} distinct bl targets ({sum(calls.values())} calls), "
          f"{prologues} stwu r1 prologues, {ops['bcctr']} bcctr")
    for o, n in ops.most_common(30):
        print(f"  {o:12} {n}")
    for a, w in undecoded[:20]:
        print(f"  undecoded {a:08X} {w:08X}")


if __name__ == "__main__":
    main()
