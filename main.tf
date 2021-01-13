variable "api_key" {}
variable "tld" {}
variable "parent_subdomain" {}

provider "vultr" {
  api_key = var.api_key
  rate_limit = 3000
  retry_limit = 5
}

data "external" "network" {
  program = ["python3", "network.py"]
}

resource "vultr_dns_record" "dynamic_dns" {
  domain = var.tld
  type = "A"
  name = join(".", [
    data.external.network.result.hostname,
    var.parent_subdomain
  ])
  data = data.external.network.result.public_ip
  ttl = 3600
}

resource "vultr_dns_record" "dynamic_private_dns" {
  domain = var.tld
  type = "A"
  name = join(".", [
    data.external.network.result.hostname,
    var.parent_subdomain,
    "private"
  ])
  data = data.external.network.result.private_ip
  ttl = 3600
}