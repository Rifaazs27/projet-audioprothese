# Ansible — gestion de la configuration on-premise

Ces playbooks configurent la VM **on-premise simulée** (provisionnée par
Terraform dans un VNet séparé) et gèrent le **PRA** via MinIO.

| Playbook | Rôle |
|---|---|
| `playbooks/minio.yml` | Installe Docker + MinIO (stockage objet **chiffré** SSE-S3) et crée le bucket de sauvegardes |
| `playbooks/backup.yml` | Sauvegarde PostgreSQL (`pg_dump`) vers MinIO |
| `playbooks/restore.yml` | Restauration de la dernière sauvegarde depuis MinIO |

## Exécution (en CI)

La CI génère automatiquement `inventory.ini` et la clé SSH à partir des sorties
Terraform, puis lance `minio.yml`. Voir `.github/workflows/deploy.yml` et le
workflow planifié `.github/workflows/backup.yml`.

## Exécution manuelle

```bash
cd ansible
# 1) Récupérer les infos depuis Terraform
terraform -chdir=../infra/terraform output -raw onprem_ssh_private_key > onprem_id_rsa
chmod 600 onprem_id_rsa
IP=$(terraform -chdir=../infra/terraform output -raw onprem_public_ip)
cp inventory.ini.example inventory.ini && sed -i "s/REMPLACER_PAR_IP_PUBLIQUE/$IP/" inventory.ini

# 2) Déployer MinIO
ansible-playbook playbooks/minio.yml \
  -e minio_root_user="$(terraform -chdir=../infra/terraform output -raw minio_root_user)" \
  -e minio_root_password="$(terraform -chdir=../infra/terraform output -raw minio_root_password)" \
  -e minio_kms_key="$(terraform -chdir=../infra/terraform output -raw minio_kms_key)"

# 3) Sauvegarde
ansible-playbook playbooks/backup.yml \
  -e database_dsn="$(terraform -chdir=../infra/terraform output -raw database_dsn_psql)" \
  -e minio_root_user="..." -e minio_root_password="..."
```

## Prérequis

```bash
pip install ansible
ansible-galaxy collection install community.docker
```

La console MinIO est accessible sur `http://<onprem_public_ip>:9001`.
