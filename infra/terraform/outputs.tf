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

# Chaîne psql (libpq) pour pg_dump/psql côté on-prem (Ansible).
output "database_dsn_psql" {
  value     = "postgresql://${var.postgres_admin_login}:${random_password.postgres.result}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.app.name}?sslmode=require"
  sensitive = true
}

# --- Sorties on-prem / MinIO (consommées par Ansible et la CI) ---
output "onprem_enabled" {
  value = var.enable_onprem
}

output "onprem_public_ip" {
  value = var.enable_onprem ? azurerm_public_ip.onprem[0].ip_address : ""
}

output "onprem_admin_user" {
  value = var.onprem_admin_user
}

output "onprem_ssh_private_key" {
  value     = var.enable_onprem ? tls_private_key.onprem[0].private_key_pem : ""
  sensitive = true
}

output "minio_root_user" {
  value = var.minio_root_user
}

output "minio_root_password" {
  value     = var.enable_onprem ? random_password.minio[0].result : ""
  sensitive = true
}

output "minio_kms_key" {
  # Format attendu par MinIO : "<nom-clé>:<clé base64>"
  value     = var.enable_onprem ? "audio-key-1:${random_id.minio_kms[0].b64_std}" : ""
  sensitive = true
}

output "minio_endpoint" {
  value = var.enable_onprem ? "http://${azurerm_public_ip.onprem[0].ip_address}:9000" : ""
}
