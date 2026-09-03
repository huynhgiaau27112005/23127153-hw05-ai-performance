#!/usr/bin/env python3
"""Generate HTML dashboards from existing JTL and run Endurance if missing."""
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


def html_from_jtl(jtl: Path, html: Path) -> None:
    if not jtl.exists() or jtl.stat().st_size < 100:
        print(f"Skip HTML (no JTL): {jtl}")
        return
    if html.exists():
        import shutil
        shutil.rmtree(html)
    run([str(JM), "-g", str(jtl), "-o", str(html)])


def main() -> None:
    for name, folder in SCENARIOS:
        out = BASE / "results" / folder
        jtl = out / f"{SID}_{name}_{DATE}.jtl"
        html = out / "html-report"
        html_from_jtl(jtl, html)

    endurance_jtl = BASE / "results" / "endurance" / f"{SID}_Endurance_{DATE}.jtl"
    if not endurance_jtl.exists() or endurance_jtl.stat().st_size < 100:
        print("=== Running Endurance (600s) ===")
        run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(RESET), "-Port", "3010"])
        out = BASE / "results" / "endurance"
        out.mkdir(parents=True, exist_ok=True)
        if endurance_jtl.exists():
            endurance_jtl.unlink()
        html = out / "html-report"
        if html.exists():
            import shutil
            shutil.rmtree(html)
        plan = BASE / "test-plans" / f"{SID}_Endurance_{DATE}.jmx"
        run([
            str(JM), "-n", "-t", str(plan), "-l", str(endurance_jtl),
            "-e", "-o", str(html),
            "-Jjmeter.save.saveservice.output_format=csv",
        ])

    run([sys.executable, str(BASE / "scripts" / "summarize_jtl.py")])
    print("Finish complete.")


if __name__ == "__main__":
    main()
