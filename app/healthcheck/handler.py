"""AWS Lambda handler for the health-check service (SCRUM-1).

Returns HTTP 200 with a JSON body describing the service, environment,
region, and a current ISO-8601 timestamp. Invoked behind API Gateway.
"""

import json
import os
from datetime import datetime, timezone


def build_response() -> dict:
    """Build the health-check payload from the runtime environment."""
    return {
        "service": "healthcheck",
        "environment": os.environ.get("ENVIRONMENT", "dev"),
        "region": os.environ.get("AWS_REGION", "eu-west-1"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def lambda_handler(event, context):
    """API Gateway (Lambda proxy) entry point."""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(build_response()),
    }
