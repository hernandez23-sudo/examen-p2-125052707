#!/usr/bin/env python3
import sys
from collections import defaultdict

totales = defaultdict(float)
for line in sys.stdin:
    try:
        prod, val = line.strip().split("\t")
        totales[prod] += float(val)
    except ValueError:
        continue

top = sorted(totales.items(), key=lambda x: -x[1])[:10]
for prod, total in top:
    print(f"{prod}\t{total:.2f}")