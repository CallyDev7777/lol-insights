# Tell Terraform we're using GCP and what version of google provider to use
terraform {
    required_providers {
        google = {
            source  = "hashicorp/google"
            version = "~> 5.0"
        }
    }
}
# Configure GCP (Logging in)
provider "google"{
    project = var.project_id
    region  = var.region
}
# Create VPC network to colonise
resource "google_compute_network" "main" {
    name                    = "lol-insights-network"
    auto_create_subnetworks = false
}
# create subnet inside network
resource "google_compute_subnetwork" "main" {
    name          = "lol-insights-subnet"
    ip_cidr_range = "10.0.0.0/16"
    region        = var.region
    network       = google_compute_network.main.id

    secondary_ip_range {
        range_name    = "pods"
        ip_cidr_range = "10.1.0.0/16"
    }

    secondary_ip_range {
        range_name    = "services"
        ip_cidr_range = "10.2.0.0/16"
    }
}

# Create kubernetes cluster
resource "google_container_cluster" "main" {
    name     = "lol-insights-cluster"
    location = var.region

    network    = google_compute_network.main.id
    subnetwork = google_compute_subnetwork.main.id

    # Autopilot enabled so GCP can handle nodes
    enable_autopilot = true

    ip_allocation_policy {
        cluster_secondary_range_name  = "pods"
        services_secondary_range_name = "services"
    }

    deletion_protection = false
}

resource "google_artifact_registry_repository" "main" {
    location      = var.region
    repository_id = "lol-insights"
    format        = "DOCKER"
}