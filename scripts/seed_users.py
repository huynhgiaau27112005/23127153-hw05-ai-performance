#!/usr/bin/env python3
"""Register CSV perf users against local EShop API on port 3001."""
import csv
import json
import urllib.error
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:3010"
CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "users.csv"


def post(path: str, body: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-Student-Id": "23127153"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def main() -> None:
    rows = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            email = row["email"]
            password = row["password"]
            code, body = post(
                "/api/register",
                {
                    "name": f"Perf {email.split('@')[0]}",
                    "email": email,
                    "password": password,
                    "role": "user",
                },
            )
            if code in (200, 201):
                print(f"OK register {email}")
            elif "exists" in body.lower() or code == 400:
                print(f"SKIP exists {email}")
            else:
                print(f"WARN {email} -> {code} {body[:120]}")


if __name__ == "__main__":
    main()
