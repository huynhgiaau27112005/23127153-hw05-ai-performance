#!/usr/bin/env python3
"""Summarize JMeter CSV JTL files for HW05 report tables."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCENARIOS = ["Load", "Stress", "Spike", "Endurance"]
DATE = "20260830"
SID = "23127153"


def summarize(path: Path) -> dict:
    rows = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    if not rows:
        return {"samples": 0, "error_pct": 0, "avg_ms": 0, "p95_ms": 0, "throughput": 0}

    elapsed = [int(r["elapsed"]) for r in rows if r.get("elapsed")]
    errors = sum(1 for r in rows if (r.get("success") or "").lower() == "false")
    ts = [int(r["timeStamp"]) for r in rows if r.get("timeStamp")]
    duration_s = max((max(ts) - min(ts)) / 1000, 1) if ts else 1
    elapsed_sorted = sorted(elapsed)
    p95 = elapsed_sorted[int(len(elapsed_sorted) * 0.95) - 1] if elapsed_sorted else 0

    by_label: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        if r.get("elapsed"):
            by_label[r["label"]].append(int(r["elapsed"]))

    labels = {
        label: {
            "count": len(vals),
            "avg_ms": round(sum(vals) / len(vals), 1),
            "p95_ms": sorted(vals)[int(len(vals) * 0.95) - 1] if vals else 0,
        }
        for label, vals in sorted(by_label.items())
    }

    return {
        "samples": len(rows),
        "errors": errors,
        "error_pct": round(100 * errors / len(rows), 2),
        "avg_ms": round(sum(elapsed) / len(elapsed), 1) if elapsed else 0,
        "p95_ms": p95,
        "throughput_rps": round(len(rows) / duration_s, 2),
        "duration_s": round(duration_s, 1),
        "by_label": labels,
    }


def main() -> None:
    out = {}
    for name in SCENARIOS:
        jtl = BASE / "results" / name.lower() / f"{SID}_{name}_{DATE}.jtl"
        out[name] = summarize(jtl) if jtl.exists() else {"missing": True, "path": str(jtl)}
    print(json.dumps(out, indent=2))
    (BASE / "results" / "summary.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
