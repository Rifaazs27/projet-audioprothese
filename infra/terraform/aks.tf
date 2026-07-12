# Cluster AKS managé. Le plan de contrôle est gratuit ; seul le pool de
# nœuds est facturé. 1 nœud B2s_v2 pour rester dans le budget Student.
# Réseau par défaut (kubenet, VNet auto-gérée) : léger et sans configuration
# manuelle, adapté à un MVP mono-nœud.
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.project}${var.environment}"
  # SKU Free : pas de SLA payant sur le plan de contrôle (FinOps).
  sku_tier = "Free"

  default_node_pool {
    name            = "system"
    node_count      = var.aks_node_count
    vm_size         = var.aks_node_size
    os_disk_size_gb = 32
  }

  # Identité managée : pas de secret de service principal à gérer.
  identity {
    type = "SystemAssigned"
  }

  # RBAC Kubernetes activé (sécurité).
  role_based_access_control_enabled = true

  tags = var.tags
}
