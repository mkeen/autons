variable "api_key" {}

provider "vultr" {
  api_key = var.api_key
  rate_limit = 3000
  retry_limit = 5
}

data "external" "network" {
  program = ["python3", "network.py"]
}

resource "vultr_dns_record" "dynamic_dns" {
  domain = "mikekeen.com"
  type = "A"
  name = data.external.network.result.hostname
  data = data.external.network.result.public_ip
  ttl = 3600
}
