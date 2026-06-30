# Mot de passe administrateur généré aléatoirement et stocké dans Key Vault.
resource "random_password" "postgres" {
  length           = 24
  special          = true
  override_special = "!#%*-_"
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-${local.name}-${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  version             = "16"

  administrator_login    = var.postgres_admin_login
  administrator_password = random_password.postgres.result

  sku_name   = var.postgres_sku
  storage_mb = var.postgres_storage_mb

  # Accès privé via le sous-réseau délégué (pas d'IP publique).
  delegated_subnet_id = azurerm_subnet.postgres.id
  private_dns_zone_id = azurerm_private_dns_zone.postgres.id

  # FinOps : pas de haute disponibilité (zone unique) pour le MVP.
  zone = "1"

  # Sauvegardes : 7 jours (PRA/PCA). Désactivé géo-redondant pour le coût.
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  tags = var.tags

  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgres]
}

resource "azurerm_postgresql_flexible_server_database" "app" {
  name      = "audioprothese"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "fr_FR.utf8"
}
