#!/usr/bin/env python3
"""Run all HW05 JMeter scenarios (cross-platform)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
JM = Path(r"e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\tools\apache-jmeter-5.6.3\bin\jmeter.bat")
RESET = Path(r"e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\scripts\reset-eshop-api.ps1")
SID, DATE = "23127153", "20260830"
SCENARIOS = [("Load", "load"), ("Stress", "stress"), ("Spike", "spike"), ("Endurance", "endurance")]


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(RESET), "-Port", "3010"])
    run([sys.executable, str(BASE / "scripts" / "generate_jmx.py")])

    for name, folder in SCENARIOS:
        out_dir = BASE / "results" / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        jtl = out_dir / f"{SID}_{name}_{DATE}.jtl"
        html = out_dir / "html-report"
        if jtl.exists():
            jtl.unlink()
        if html.exists():
            import shutil
            shutil.rmtree(html)
        plan = BASE / "test-plans" / f"{SID}_{name}_{DATE}.jmx"
        print(f"=== {name} ===")
        run([
            str(JM), "-n", "-t", str(plan), "-l", str(jtl),
            "-e", "-o", str(html),
            "-Jjmeter.save.saveservice.output_format=csv",
        ])

    run([sys.executable, str(BASE / "scripts" / "summarize_jtl.py")])
    print("All scenarios complete.")


if __name__ == "__main__":
    main()
