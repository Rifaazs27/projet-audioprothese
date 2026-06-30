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

  # État distant : à activer après le bootstrap (voir docs/installation.md).
  # Stocke le tfstate dans un compte de stockage Azure pour le travail en équipe.
  # backend "azurerm" {
  #   resource_group_name  = "rg-tfstate-audioprothese"
  #   storage_account_name = "sttfstateaudio"
  #   container_name       = "tfstate"
  #   key                  = "mvp.tfstate"
  # }
}

provider "azurerm" {
  features {
    resource_group {
      # FinOps : permet de tout détruire facilement après la démo.
      prevent_deletion_if_contains_resources = false
    }
  }
}
