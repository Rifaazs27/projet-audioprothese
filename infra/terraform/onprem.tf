# --- Simulation "on-premise" -------------------------------------------------
# Le cahier des charges décrit une architecture hybride (cloud + serveurs
# on-premise pour les données sensibles). On simule l'on-premise par une VM
# Linux placée dans un VNet TOTALEMENT SÉPARÉ (non peeré au réseau AKS) :
# elle représente un site distinct, joint depuis le cloud via son IP publique
# (comme le serait un site on-prem via Internet/VPN). Cette VM héberge MinIO
# (stockage objet chiffré) pour les sauvegardes — pilotée par Ansible.

variable "enable_onprem" {
  description = "Active la VM on-prem simulée + MinIO"
  type        = bool
  default     = true
}

variable "onprem_vm_size" {
  description = "Taille de la VM on-prem (FinOps : burstable)"
  type        = string
  default     = "Standard_B2s_v2"
}

variable "onprem_admin_user" {
  description = "Utilisateur admin de la VM on-prem"
  type        = string
  default     = "azureuser"
}

variable "minio_root_user" {
  description = "Compte root MinIO"
  type        = string
  default     = "audiominio"
}

# Mot de passe MinIO + clé de chiffrement KMS, générés aléatoirement.
resource "random_password" "minio" {
  count   = var.enable_onprem ? 1 : 0
  length  = 24
  special = false
}

resource "random_id" "minio_kms" {
  count       = var.enable_onprem ? 1 : 0
  byte_length = 32
}

# Clé SSH générée pour qu'Ansible se connecte sans secret pré-existant.
resource "tls_private_key" "onprem" {
  count     = var.enable_onprem ? 1 : 0
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Réseau "on-prem" isolé (espace d'adressage distinct, aucun peering).
resource "azurerm_virtual_network" "onprem" {
  count               = var.enable_onprem ? 1 : 0
  name                = "vnet-onprem-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.20.0.0/16"]
  tags                = merge(var.tags, { tier = "on-premise-simule" })
}

resource "azurerm_subnet" "onprem" {
  count                = var.enable_onprem ? 1 : 0
  name                 = "snet-onprem"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.onprem[0].name
  address_prefixes     = ["10.20.1.0/24"]
}

resource "azurerm_public_ip" "onprem" {
  count               = var.enable_onprem ? 1 : 0
  name                = "pip-onprem-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = var.tags
}

# Pare-feu : SSH (Ansible) + ports MinIO (API 9000, console 9001).
resource "azurerm_network_security_group" "onprem" {
  count               = var.enable_onprem ? 1 : 0
  name                = "nsg-onprem-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = var.tags

  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "MinIO"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["9000", "9001"]
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface" "onprem" {
  count               = var.enable_onprem ? 1 : 0
  name                = "nic-onprem-${local.name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = var.tags

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.onprem[0].id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.onprem[0].id
  }
}

resource "azurerm_network_interface_security_group_association" "onprem" {
  count                     = var.enable_onprem ? 1 : 0
  network_interface_id      = azurerm_network_interface.onprem[0].id
  network_security_group_id = azurerm_network_security_group.onprem[0].id
}

resource "azurerm_linux_virtual_machine" "onprem" {
  count                 = var.enable_onprem ? 1 : 0
  name                  = "vm-onprem-${local.name}"
  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  size                  = var.onprem_vm_size
  admin_username        = var.onprem_admin_user
  network_interface_ids = [azurerm_network_interface.onprem[0].id]
  tags                  = merge(var.tags, { tier = "on-premise-simule" })

  admin_ssh_key {
    username   = var.onprem_admin_user
    public_key = tls_private_key.onprem[0].public_key_openssh
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 32
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # python3 est présent sur l'image Ubuntu : Ansible peut piloter la VM
  # directement. L'installation de Docker/MinIO est faite par les playbooks.
}
