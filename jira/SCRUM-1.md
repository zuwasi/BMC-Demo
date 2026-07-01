# SCRUM-1:  Add AWS Lambda health-check service

- **Type:** Task
- **Status:** To Do
- **URL:** https://liezrowice.atlassian.net/browse/SCRUM-1

## Description

Add a new AWS Lambda-based health-check service. The service should expose a simple HTTP endpoint through API Gateway. The endpoint should return status 200 and a JSON response containing service name, environment, region, and timestamp. Add Terraform resources, update the Jenkins deployment pipeline, and add an automated test that validates the deployed endpoint.

---
_Fetched live from Jira Cloud via `GET /rest/api/3/issue/SCRUM-1`._
