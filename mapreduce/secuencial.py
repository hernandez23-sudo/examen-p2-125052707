#!/usr/bin/env python3
import csv
from collections import defaultdict

totales = defaultdict(float)
with open("/data/input/ventas_125052707.csv") as f:
    r = csv.DictReader(f)
    for row in r:
        try:
            totales[row["producto"]] += int(row["cantidad"]) * float(row["precio_unitario"])
        except (ValueError, KeyError):
            continue

for prod, total in sorted(totales.items(), key=lambda x: -x[1])[:10]:
    print(f"{prod}\t{total:.2f}")