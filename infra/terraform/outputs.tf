output "healthcheck_endpoint" {
  description = "Public URL of the deployed health-check endpoint."
  value       = "${aws_apigatewayv2_api.http.api_endpoint}/healthcheck"
}

output "lambda_function_name" {
  description = "Name of the deployed Lambda function."
  value       = aws_lambda_function.healthcheck.function_name
}
