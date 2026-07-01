"""Tests for the sensor service.

Local mode (default): compile sensor.c and run it, asserting the sample count.
Post-deploy mode: if SENSOR_ENDPOINT is set, call the deployed API and assert
the reported count.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

EXPECTED = 30
ENDPOINT = os.environ.get("SENSOR_ENDPOINT")
ROOT = Path(__file__).resolve().parent.parent


def _local_count():
    src = ROOT / "sensor.c"
    exe = ROOT / ("sensor.exe" if sys.platform == "win32" else "sensor.out")
    subprocess.run(["gcc", str(src), "-o", str(exe)], check=True)
    out = subprocess.run([str(exe)], capture_output=True, text=True, check=True).stdout
    return len([ln for ln in out.splitlines() if ln.strip()])


def _deployed_payload():
    import urllib.request

    with urllib.request.urlopen(ENDPOINT) as resp:
        return resp.getcode(), json.loads(resp.read().decode())


def test_sample_count():
    if ENDPOINT:
        status, data = _deployed_payload()
        assert status == 200
        assert data["count"] == EXPECTED, f"expected {EXPECTED}, got {data['count']}"
        assert data["ok"] is True
    else:
        count = _local_count()
        assert count == EXPECTED, f"expected {EXPECTED}, got {count}"
