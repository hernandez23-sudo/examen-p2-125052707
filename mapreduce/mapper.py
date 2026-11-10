#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id,"):
        continue
    try:
        parts = line.split(",")
        if len(parts) != 8:
            continue
        producto = parts[4]
        cantidad = int(parts[5])
        precio = float(parts[6])
        ingreso = cantidad * precio
        print(f"{producto}\t{ingreso}")
    except (ValueError, IndexError):
        continue