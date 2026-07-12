# Azure Container Registry — stockage des images Docker.
# SKU Basic : le moins cher, suffisant pour le MVP.
resource "azurerm_container_registry" "main" {
  name                = "acr${var.project}${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = var.tags
}

# Autorise le cluster AKS à tirer les images (AcrPull) sans secret stocké.
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                            = azurerm_container_registry.main.id
  role_definition_name             = "AcrPull"
  principal_id                     = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
  skip_service_principal_aad_check = true
}
