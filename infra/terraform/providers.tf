terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.10"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # État distant dans un Storage Account Azure. La configuration (nom du
  # compte, conteneur, clé) est fournie par la CI via -backend-config, et le
  # compte est créé automatiquement par le workflow (aucune action manuelle).
  backend "azurerm" {}
}

provider "azurerm" {
  # subscription_id est lu depuis ARM_SUBSCRIPTION_ID (exporté par la CI).
  # L'authentification s'appuie sur la session `az login` de la CI.
  features {
    resource_group {
      # FinOps : permet de tout détruire facilement après la démo.
      prevent_deletion_if_contains_resources = false
    }
  }
}
