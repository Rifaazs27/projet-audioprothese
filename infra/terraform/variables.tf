variable "project" {
  description = "Préfixe de nommage des ressources"
  type        = string
  default     = "audioprothese"
}

variable "environment" {
  description = "Environnement (mvp, dev, prod)"
  type        = string
  default     = "mvp"
}

variable "location" {
  description = "Région Azure. France Central pour la conformité RGPD/HDS (données de santé)."
  type        = string
  default     = "francecentral"
}

# --- FinOps : dimensionnement volontairement minimal (compte Student 85 $) ---
variable "aks_node_count" {
  description = "Nombre de nœuds AKS (1 pour le MVP)"
  type        = number
  default     = 1
}

variable "aks_node_size" {
  description = "Taille des VM du pool AKS. B2s = ~30 $/mois, suffisant pour le MVP."
  type        = string
  default     = "Standard_B2s"
}

variable "postgres_sku" {
  description = "SKU PostgreSQL Flexible Server. B1ms = palier le moins cher (burstable)."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "postgres_storage_mb" {
  description = "Stockage PostgreSQL en Mo (minimum 32768)"
  type        = number
  default     = 32768
}

variable "postgres_admin_login" {
  description = "Login administrateur PostgreSQL"
  type        = string
  default     = "audioadmin"
}

variable "monthly_budget_amount" {
  description = "Plafond budgétaire mensuel en USD (alertes FinOps)"
  type        = number
  default     = 50
}

variable "budget_alert_emails" {
  description = "Adresses notifiées par les alertes de budget"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Étiquettes communes (suivi des coûts / FinOps)"
  type        = map(string)
  default = {
    projet     = "projet-etude-m2"
    cours      = "devops"
    managed_by = "terraform"
  }
}
