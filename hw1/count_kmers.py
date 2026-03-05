#!/usr/bin/env python3

import argparse
import json
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--fa', required=True)
args = parser.parse_args()

# Чтение FASTA
seqs = {}
with open(args.fa) as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            name = line[1:].split()[0]
            seqs[name] = ''
        else:
            seqs[name] += line.upper()

# Подсчёт k-меров
result = {}
for name, seq in seqs.items():
    kmers = [seq[i:i+4] for i in range(len(seq)-3)]
    result[name] = dict(Counter(kmers))

with open('cnts.json', 'w') as f:
    f.write('{\n')
    for i, (name, kmers) in enumerate(result.items()):
        kmers_str = json.dumps(kmers, ensure_ascii=False)
        f.write(f'    "{name}": {kmers_str}')
        if i < len(result) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write('}\n')
