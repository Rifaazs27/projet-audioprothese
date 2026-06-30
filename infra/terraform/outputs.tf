output "resource_group" {
  value = azurerm_resource_group.main.name
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "key_vault_name" {
  value = azurerm_key_vault.main.name
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

# Commande prête à l'emploi pour configurer kubectl.
output "aks_get_credentials_cmd" {
  value = "az aks get-credentials --resource-group ${azurerm_resource_group.main.name} --name ${azurerm_kubernetes_cluster.main.name}"
}

output "database_url_secret_uri" {
  description = "URI du secret Key Vault contenant la chaîne de connexion"
  value       = azurerm_key_vault_secret.database_url.versionless_id
  sensitive   = true
}
