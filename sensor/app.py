"""AWS Lambda handler that runs the compiled C sensor binary and reports how
many sample lines it produced. Deployed as a container image."""

import json
import os
import subprocess

EXPECTED_SAMPLES = 30


def handler(event, context):
    binary = os.path.join(os.environ["LAMBDA_TASK_ROOT"], "sensor")
    proc = subprocess.run([binary], capture_output=True, text=True, timeout=10)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    count = len(lines)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "service": "sensor",
                "environment": os.environ.get("ENVIRONMENT", "dev"),
                "count": count,
                "expected": EXPECTED_SAMPLES,
                "ok": count == EXPECTED_SAMPLES,
                "output": proc.stdout,
            }
        ),
    }
