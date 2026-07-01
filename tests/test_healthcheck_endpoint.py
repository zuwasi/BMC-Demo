"""Validation tests for the health-check service (SCRUM-1).

Runs in two modes:

* Post-deployment: if HEALTHCHECK_ENDPOINT is set, the tests call the real
  deployed API Gateway URL over HTTP.
* Local: otherwise they invoke the Lambda handler directly, so the same
  assertions run in CI unit-test stage without any AWS access.
"""

import json
import os

ENDPOINT = os.environ.get("HEALTHCHECK_ENDPOINT")


def _get_payload():
    """Return (status_code, parsed_json) from the deployed endpoint or the
    local Lambda handler."""
    if ENDPOINT:
        import urllib.request

        with urllib.request.urlopen(ENDPOINT) as resp:
            return resp.getcode(), json.loads(resp.read().decode())

    from app.healthcheck.handler import lambda_handler

    result = lambda_handler({}, None)
    return result["statusCode"], json.loads(result["body"])


def test_status_code_is_200():
    status, _ = _get_payload()
    assert status == 200


def test_response_is_valid_json():
    _, data = _get_payload()
    assert isinstance(data, dict)


def test_service_is_healthcheck():
    _, data = _get_payload()
    assert data["service"] == "healthcheck"


def test_environment_is_dev():
    _, data = _get_payload()
    assert data["environment"] == "dev"


def test_region_exists():
    _, data = _get_payload()
    assert data.get("region")


def test_timestamp_exists():
    _, data = _get_payload()
    assert data.get("timestamp")
