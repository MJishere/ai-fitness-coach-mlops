terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket         = "ai-fitness-manoj-tf"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks-ai-fitness-manoj"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}