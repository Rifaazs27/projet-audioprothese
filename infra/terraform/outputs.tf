output "resource_group" {
  value = azurerm_resource_group.main.name
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "acr_name" {
  value = azurerm_container_registry.main.name
}

output "acr_login_server" {
  value = azurerm_container_registry.main.login_server
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

# Chaîne de connexion complète consommée par l'application. Sensible :
# récupérée par la CI via `terraform output -raw` puis injectée dans un
# Secret Kubernetes par Helm.
output "database_url" {
  value     = "postgresql+psycopg://${var.postgres_admin_login}:${random_password.postgres.result}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.app.name}?sslmode=require"
  sensitive = true
}
