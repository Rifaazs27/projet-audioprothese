# Cluster AKS managé. Le plan de contrôle est gratuit ; seul le pool de
# nœuds est facturé. 1 nœud B2s pour rester dans le budget Student.
resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.project}${var.environment}"
  # SKU Free : pas de SLA payant sur le plan de contrôle (FinOps).
  sku_tier = "Free"

  default_node_pool {
    name           = "system"
    node_count     = var.aks_node_count
    vm_size        = var.aks_node_size
    vnet_subnet_id = azurerm_subnet.aks.id
    # Disque OS éphémère/Managé minimal pour réduire les coûts.
    os_disk_size_gb = 32
  }

  # Identité managée : pas de secret de service principal à gérer.
  identity {
    type = "SystemAssigned"
  }

  # RBAC Kubernetes activé (sécurité).
  role_based_access_control_enabled = true

  network_profile {
    network_plugin = "azure"
    network_policy = "azure" # network policies pour le cloisonnement des pods
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  tags = var.tags
}
