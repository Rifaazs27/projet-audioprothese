#!/usr/bin/env bash
# FinOps — DÉTRUIT toute l'infrastructure Azure pour stopper la facturation.
# À lancer systématiquement après chaque session de démonstration.
set -euo pipefail
cd "$(dirname "$0")/../infra/terraform"

echo "ATTENTION : cette commande supprime TOUTES les ressources Azure du projet."
read -r -p "Confirmer la destruction ? (tapez 'oui') " reponse
[ "$reponse" = "oui" ] || { echo "Annulé."; exit 1; }

terraform destroy -auto-approve
echo "Infrastructure détruite. Facturation stoppée."
