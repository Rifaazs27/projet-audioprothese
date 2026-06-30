# Mot de passe administrateur généré aléatoirement (jamais en clair dans Git).
resource "random_password" "postgres" {
  length           = 24
  special          = true
  override_special = "!#%*-_"
}

# PostgreSQL Flexible Server en accès public + pare-feu "services Azure".
# Choix MVP : évite la complexité d'un réseau privé (VNet déléguée, DNS privé)
# tout en restant joignable uniquement depuis Azure et avec TLS obligatoire.
resource "azurerm_postgresql_flexible_server" "main" {
  name                = "psql-${local.name}-${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  version             = "16"

  administrator_login    = var.postgres_admin_login
  administrator_password = random_password.postgres.result

  sku_name   = var.postgres_sku
  storage_mb = var.postgres_storage_mb

  public_network_access_enabled = true

  # FinOps : pas de haute disponibilité (zone unique) pour le MVP.
  zone = "1"

  # Sauvegardes : 7 jours (PRA/PCA). Pas de géo-redondance (coût).
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  tags = var.tags
}

resource "azurerm_postgresql_flexible_server_database" "app" {
  name      = "audioprothese"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "fr_FR.utf8"
}

# Autorise les ressources internes à Azure (dont les nœuds AKS) à se
# connecter. La plage 0.0.0.0/0.0.0.0 est la règle spéciale "Allow Azure
# services" : aucune connexion depuis l'Internet public n'est admise.
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
