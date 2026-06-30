# FinOps — garde-fou budgétaire. Alertes par e-mail à 50%, 80% et 100% du
# plafond mensuel, plus une prévision à 100%. Indispensable sur un compte
# Student limité à 85 $.
resource "azurerm_consumption_budget_resource_group" "main" {
  count             = length(var.budget_alert_emails) > 0 ? 1 : 0
  name              = "budget-${local.name}"
  resource_group_id = azurerm_resource_group.main.id

  amount     = var.monthly_budget_amount
  time_grain = "Monthly"

  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00'Z'", timestamp())
  }

  notification {
    enabled        = true
    threshold      = 50
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = var.budget_alert_emails
  }

  notification {
    enabled        = true
    threshold      = 80
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = var.budget_alert_emails
  }

  notification {
    enabled        = true
    threshold      = 100
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Forecasted"
    contact_emails = var.budget_alert_emails
  }

  lifecycle {
    # Le start_date basé sur timestamp() ne doit pas forcer de recréation.
    ignore_changes = [time_period]
  }
}
