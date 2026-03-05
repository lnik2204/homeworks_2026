#!/usr/bin/env python3

import argparse

p = argparse.ArgumentParser()
p.add_argument('--seq', required=True)
args = p.parse_args()
s = args.seq.upper()

# Reverse complement
comp = {'A':'T','T':'A','G':'C','C':'G'}
rev = ''.join(comp[b] for b in reversed(s))
print(rev)

# GC content
gc = (s.count('G') + s.count('C')) / len(s)
print(f"{gc:.3f}")
