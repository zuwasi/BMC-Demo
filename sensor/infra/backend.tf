terraform {
  backend "s3" {
    bucket = "bmc-demo-tfstate-569428679488"
    key    = "sensor/dev/terraform.tfstate"
    region = "eu-west-1"
  }
}
