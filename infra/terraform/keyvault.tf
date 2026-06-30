# Azure Key Vault — gestion centralisée des secrets (équivalent managé de
# Vault, sans coût d'hébergement). Le cluster AKS y accède via le CSI driver
# Secrets Store / Workload Identity (voir docs/securite-devsecops.md).

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = "kv-${var.project}-${local.suffix}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  enable_rbac_authorization  = true
  tags                       = var.tags
}

# L'opérateur Terraform a le droit d'écrire les secrets.
resource "azurerm_role_assignment" "kv_admin" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# Chaîne de connexion complète à la base, consommée par l'application.
resource "azurerm_key_vault_secret" "database_url" {
  name  = "database-url"
  value = "postgresql+psycopg://${var.postgres_admin_login}:${random_password.postgres.result}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.app.name}?sslmode=require"

  key_vault_id = azurerm_key_vault.main.id
  depends_on   = [azurerm_role_assignment.kv_admin]
}

# Le kubelet AKS peut lire les secrets (AcrPull-like pour Key Vault).
resource "azurerm_role_assignment" "aks_kv_reader" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}
