terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "hasib_platform" {
  name     = "hasib-platform-rg"
  location = "West US 2"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "hasib-aks-cluster"
  location            = azurerm_resource_group.hasib_platform.location
  resource_group_name = azurerm_resource_group.hasib_platform.name
  dns_prefix          = "hasib-platform-k8s"

  default_node_pool {
    name                = "default"
    vm_size             = "Standard_D2as_v5"
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 3
  }

  identity {
    type = "SystemAssigned"
  }

  role_based_access_control_enabled = true

  tags = {
    environment = "Learning"
    project     = "HasibPlatform"
  }
}

output "resource_group_name" {
  value = azurerm_resource_group.hasib_platform.name
}

output "kubernetes_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}