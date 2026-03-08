#!/usr/bin/env python3

import argparse
import json
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--fa', required=True, help='Входной FASTA файл')
parser.add_argument('--k', type=int, default=4, help='Длина k-мера')
parser.add_argument('--out', default='cnts.json', help='Выходной JSON файл')
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
k = args.k
for name, seq in seqs.items():
    if len(seq) >= k:
        kmers = [seq[i:i+k] for i in range(len(seq)-k+1)]
        result[name] = dict(Counter(kmers))
    else:
        result[name] = {}

with open('out.json', 'w') as f:
    f.write('{\n')
    for i, (name, kmers) in enumerate(result.items()):
        kmers_str = json.dumps(kmers, ensure_ascii=False)
        f.write(f'    "{name}": {kmers_str}')
        if i < len(result) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write('}\n')
