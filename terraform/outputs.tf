output "cluster_name" {
    description = "GKE cluster name"
    value       = google_container_cluster.main.name
}

output "cluster_region" {
    description = "GKE cluster region"
    value       = google_container_cluster.main.location
}

output "artifact_registry_url" {
    description = "URL to push Docker images to"
    value       = "${var.region}-docker.pkg.dev/${var.project_id}/lol-insights"
}