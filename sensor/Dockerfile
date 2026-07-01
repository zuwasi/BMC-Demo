# Stage 1: compile the C sensor on Amazon Linux 2023 (Lambda-compatible)
FROM amazonlinux:2023 AS build
RUN dnf install -y gcc && dnf clean all
COPY sensor.c /tmp/sensor.c
RUN gcc -O2 -Wall /tmp/sensor.c -o /tmp/sensor

# Stage 2: package the binary behind the AWS Lambda Python runtime
FROM public.ecr.aws/lambda/python:3.12
COPY --from=build /tmp/sensor ${LAMBDA_TASK_ROOT}/sensor
COPY app.py ${LAMBDA_TASK_ROOT}/app.py
CMD ["app.handler"]
