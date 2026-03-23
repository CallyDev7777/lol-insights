# ⚔️ LoL Insights

A production-grade League of Legends stats platform built to demonstrate real platform engineering skills across the full infrastructure stack.

## 🏗️ Architecture
```
Internet → GCP Load Balancer → Kubernetes Ingress
                                      ↓
                            2x FastAPI API Pods
                                      ↓
                              Redis Cache Pod
                                      ↓
                              Riot Games API
```

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **Caching:** Redis (cache-aside pattern)
- **Containerisation:** Docker (multi-stage builds)
- **Infrastructure:** Terraform (IaC)
- **Orchestration:** Kubernetes (GKE Autopilot)
- **Cloud:** Google Cloud Platform (europe-west2)
- **Registry:** GCP Artifact Registry

## ✨ Features

- Summoner profile lookup with profile icon
- Ranked stats with tier badge and win rate bar
- Recent match history across all game modes (Arena, URF, ARAM, SR)
- Redis caching with force-refresh capability
- Runs with 2 replicas and zero-downtime rolling deployments

## 🚀 Infrastructure

Provisioned entirely with Terraform:
- VPC network and subnets
- GKE Autopilot cluster (London region)
- GCP Artifact Registry for Docker images

## 🐳 Running Locally
```bash
# Clone the repo
git clone https://github.com/CallyDev7777/lol-insights.git
cd lol-insights

# Add your Riot API key
cp .env.example .env
# Edit .env with your RIOT_API_KEY from developer.riotgames.com

# Start with Docker Compose
docker compose up --build
```

Visit `http://localhost:8000`

## ☸️ Kubernetes Deployment
```bash
# Provision infrastructure
cd terraform
terraform init
terraform apply

# Push Docker image
docker build -t europe-west2-docker.pkg.dev/YOUR_PROJECT/lol-insights/api:v1 .
docker push europe-west2-docker.pkg.dev/YOUR_PROJECT/lol-insights/api:v1

# Deploy to GKE
gcloud container clusters get-credentials lol-insights-cluster --region europe-west2
kubectl apply -f kubernetes/
```

## 📁 Project Structure
```
lol-insights/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── riot_client.py   # Riot API integration
│   ├── cache.py         # Redis cache-aside pattern
│   ├── models.py        # Pydantic data models
│   └── static/
│       └── index.html   # Frontend dashboard
├── kubernetes/
│   ├── deployment.yaml  # API deployment (2 replicas)
│   ├── service.yaml     # ClusterIP service
│   ├── ingress.yaml     # GCP load balancer
│   ├── redis.yaml       # Redis deployment + service
│   ├── configmap.yaml   # Non-secret config
│   └── secret.yaml      # Riot API key (encrypted)
├── terraform/
│   ├── main.tf          # GCP resources
│   ├── variables.tf     # Input variables
│   └── outputs.tf       # Output values
├── Dockerfile           # Multi-stage build
├── docker-compose.yml   # Local development
└── requirements.txt     # Python dependencies
```

## 🔑 Key Engineering Decisions

**Cache-aside pattern** — API responses cached in Redis for 5 minutes to handle Riot's dev key rate limits (100 req/2min). Force-refresh endpoint bypasses cache when needed.

**Multi-stage Docker build** — Separate builder and runtime stages keep the final image lean.

**GKE Autopilot** — Nodes managed by GCP, reducing operational overhead while maintaining full Kubernetes API compatibility.

**2 replicas** — Ensures availability during rolling deployments with zero downtime.