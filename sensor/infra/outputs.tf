output "ecr_repository_url" {
  description = "ECR repository URL for the sensor image."
  value       = aws_ecr_repository.sensor.repository_url
}

output "sensor_endpoint" {
  description = "Public URL of the deployed sensor endpoint (empty until image_tag is set)."
  value       = var.image_tag == "" ? "" : "${aws_apigatewayv2_api.http[0].api_endpoint}/sensor"
}
