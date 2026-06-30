locals {
  name   = "${var.project}-${var.environment}"
  suffix = random_string.suffix.result
}

# Suffixe aléatoire pour les ressources à nom globalement unique (ACR, etc.).
resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${local.name}"
  location = var.location
  tags     = var.tags
}
