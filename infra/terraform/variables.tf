variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "service_name" {
  description = "Logical service name, used for resource naming."
  type        = string
  default     = "healthcheck"
}
