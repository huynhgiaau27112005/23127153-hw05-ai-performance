#!/usr/bin/env python3
"""Run Stress, Spike, Endurance only (Load already completed)."""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
JM = Path(r"e:\DISK D\NOTES FOR CLASS\NAM 3\HOC KY III\TESTING\HOMEWORKS\tools\apache-jmeter-5.6.3\bin\jmeter.bat")
SID, DATE = "23127153", "20260830"
SCENARIOS = [("Stress", "stress"), ("Spike", "spike"), ("Endurance", "endurance")]


def run(cmd: list[str], timeout: int | None = None) -> None:
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, timeout=timeout)


def remove_path(p: Path, retries: int = 10) -> None:
    for attempt in range(retries):
        try:
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                shutil.rmtree(p)
            return
        except PermissionError:
            if attempt == retries - 1:
                backup = p.with_suffix(p.suffix + ".bak")
                if p.is_file() and not backup.exists():
                    p.rename(backup)
                    return
                raise
            time.sleep(3)


def main() -> None:
    for name, folder in SCENARIOS:
        out = BASE / "results" / folder
        out.mkdir(parents=True, exist_ok=True)
        jtl = out / f"{SID}_{name}_{DATE}.jtl"
        html = out / "html-report"
        for p in (jtl, html):
            if p.exists():
                remove_path(p)
        plan = BASE / "test-plans" / f"{SID}_{name}_{DATE}.jmx"
        timeout = 900 if name == "Endurance" else 600
        print(f"=== {name} (timeout {timeout}s) ===", flush=True)
        run([
            str(JM), "-n", "-t", str(plan), "-l", str(jtl),
            "-e", "-o", str(html),
            "-Jjmeter.save.saveservice.output_format=csv",
        ], timeout=timeout)

    run([sys.executable, str(BASE / "scripts" / "summarize_jtl.py")])
    print("Remaining scenarios complete.", flush=True)


if __name__ == "__main__":
    main()
