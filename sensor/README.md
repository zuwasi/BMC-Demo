# Sensor Demo — bug-fix loop on AWS (container Lambda)

Repeatable demo of Amp's value: a deployed service has a bug, a Jira ticket is
filed, Amp debugs and fixes it locally, Jenkins builds a container image, pushes
to ECR, deploys to AWS Lambda, and the live result flips from wrong to right.

## The bug

`sensor.c` should emit **30** sample lines but a hard-coded `limit = 20` caps it
at **20**. The fix uses `MAX_NUMBER_OF_SAMPLES` (30).

```
Run on AWS -> count=20  (bug)          Fix limit -> count=30  (correct)
```

## How it runs on AWS

The C binary is compiled on Amazon Linux 2023 and packaged behind the AWS Lambda
Python runtime as a **container image** (see `Dockerfile`). `app.py` runs the
binary, counts the sample lines, and returns JSON:

```json
{ "service": "sensor", "count": 30, "expected": 30, "ok": true, "output": "..." }
```

Terraform provisions ECR + the container Lambda + an HTTP API Gateway route
`GET /sensor`.

## Layout

```
sensor/
  sensor.c                 C program (the bug lives here)
  app.py                   Lambda handler: run binary, count lines
  Dockerfile               compile C (AL2023) + package on Lambda base
  infra/                   ECR + Lambda(image) + API Gateway + IAM
  tests/test_sensor.py     local (compile+run) and post-deploy (HTTP) checks
  jenkins/Jenkinsfile      build image -> push ECR -> terraform deploy -> test
```

## Demo loop (per run, new Jira ticket)

1. Show the deployed endpoint returning `count=20`.
2. Create a Jira ticket and assign it.
3. Use Amp to debug locally, fix `sensor.c`, run tests (count=30).
4. Commit on a `fix/<ticket>` branch and push.
5. Jenkins `sensor-build` compiles, tests, pushes the image, deploys.
6. The endpoint now returns `count=30`. Close the ticket.
