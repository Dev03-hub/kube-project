# Kubernetes CI/CD Project

## 🚀 Overview
This project demonstrates end-to-end DevOps pipeline:
- Dockerized application
- Kubernetes deployment
- CI/CD using GitHub Actions
- Monitoring with Prometheus & Grafana

---

## 🏗️ Architecture
GitHub → GitHub Actions → Docker Hub → Kubernetes

---

## ⚙️ Tech Stack
- Docker
- Kubernetes
- GitHub Actions
- Prometheus
- Grafana

---

## ▶️ Deployment Steps

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
