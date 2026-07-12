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
  description = "Région Azure."
  type        = string
  default     = "polandcentral"
}

# --- FinOps : dimensionnement volontairement minimal (compte Student 85 $) ---
variable "aks_node_count" {
  description = "Nombre de nœuds AKS (2 pour héberger app + ingress + stack monitoring)"
  type        = number
  default     = 2
}

variable "aks_node_size" {
  description = "Taille des VM du pool AKS."
  type        = string
  default     = "Standard_B2s_v2"
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
  description = "Adresses notifiées par les alertes de budget (vide = budget désactivé)"
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
