# BMC-Demo — Agentic DevOps: AWS Lambda Health-Check Service

End-to-end demo of an autonomous DevOps workflow driven from a Jira ticket
([SCRUM-1](https://liezrowice.atlassian.net/browse/SCRUM-1)): read the task,
change application + infrastructure + pipeline code, validate, commit, push,
and (in a real environment) deploy to AWS via Jenkins and Terraform.

## Workflow

```
Jira SCRUM-1  ->  Amp (code + infra)  ->  Git branch + push  ->  Jenkins  ->  AWS (Lambda + API Gateway)
                                                                                    |
                                                       pytest 200 / JSON validation  <-
```

## Repository layout

```
app/healthcheck/handler.py          Lambda handler: 200 + JSON (service/env/region/timestamp)
infra/terraform/                    Lambda + HTTP API Gateway + least-privilege IAM
  main.tf variables.tf outputs.tf
  environments/dev.tfvars           region=eu-west-1, environment=dev
jenkins/Jenkinsfile                 9-stage CI/CD pipeline
tests/test_healthcheck_endpoint.py  Local + post-deploy validation
jira/SCRUM-1.md                     The source ticket (fetched from Jira)
```

## Local validation

```bash
python -m pytest -q
```

Tests invoke the Lambda handler directly. Against a deployed endpoint, set
`HEALTHCHECK_ENDPOINT` and the same tests run over HTTP.

## Deploy (real environment)

```bash
cd infra/terraform
terraform init
terraform plan  -var-file=environments/dev.tfvars -out=tfplan
terraform apply tfplan
```

The endpoint URL is exposed as the `healthcheck_endpoint` Terraform output.

## Validation contract

The endpoint returns HTTP 200 with:

```json
{
  "service": "healthcheck",
  "environment": "dev",
  "region": "eu-west-1",
  "timestamp": "<ISO timestamp>"
}
```
