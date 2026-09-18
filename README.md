# Kubernetes CI/CD Project

A complete DevOps demonstration project that packages a Flask REST API into a Docker container, runs it on Kubernetes, exposes it through a Service and NGINX Ingress, and automates testing and Docker image delivery through GitHub Actions and Jenkins.

---

## 1. Project Overview

This project demonstrates a simple user-service application deployed using modern container and Kubernetes practices.

### Application

The application is a Flask REST API that provides:

* Application status
* Health checking
* User listing
* User creation

### DevOps Components

* Python
* Flask
* Docker
* Kubernetes
* Kubernetes Deployment
* Kubernetes Service
* Kubernetes Ingress
* GitHub Actions
* Jenkins
* Docker Hub

---

## 2. Architecture

```text
                    Developer
                        |
                        v
                   GitHub Repository
                        |
            +-----------+-----------+
            |                       |
            v                       v
     GitHub Actions              Jenkins
            |                       |
      Run Tests                     |
            |                       |
      Build Image                   |
            |                       |
            +----------+------------+
                       |
                       v
                   Docker Hub
                       |
                       v
                 Kubernetes Cluster
                       |
                 Deployment
                  2 Replicas
                       |
                       v
                    Service
                       |
                       v
                    Ingress
                       |
                       v
                    Client
```

---

## 3. Repository Structure

```text
kube-project/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── app/
│   └── app.py
│
├── tests/
│   └── test_app.py
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## 4. Application API

| Method | Endpoint  | Purpose                 |
| ------ | --------- | ----------------------- |
| GET    | `/`       | Application status      |
| GET    | `/health` | Kubernetes health check |
| GET    | `/users`  | Get all users           |
| POST   | `/users`  | Create a user           |

### Example health response

```json
{
  "status": "healthy"
}
```

### Example GET `/users`

```json
[
  {
    "id": 1,
    "name": "Debraj"
  }
]
```

### Example POST `/users`

Request:

```json
{
  "name": "Alice"
}
```

Response:

```json
{
  "message": "User added",
  "user": {
    "id": 2,
    "name": "Alice"
  }
}
```

---

# 5. Prerequisites

Install or have access to:

* Python 3.12
* Docker
* kubectl
* A Kubernetes cluster
* An NGINX Ingress Controller for Ingress testing
* Docker Hub account
* GitHub account
* Jenkins, if using the Jenkins pipeline

Verify the tools:

```bash
python --version
docker --version
kubectl version --client
```

---

# 6. Run the Application Locally

Clone the repository:

```bash
git clone https://github.com/Dev03-hub/kube-project.git
cd kube-project
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run the application:

```bash
python app/app.py
```

The application listens on:

```text
http://localhost:5000
```

Test the health endpoint:

```text
http://localhost:5000/health
```

Test users:

```text
http://localhost:5000/users
```

---

# 7. Run Tests

Run:

```bash
pytest -v
```

The tests verify:

* Application status
* Health endpoint
* User retrieval
* User creation
* Invalid user requests

---

# 8. Build the Docker Image

Build the image:

```bash
docker build -t devhub01553/user-service:latest .
```

Verify:

```bash
docker images
```

---

# 9. Run Docker Container

Run:

```bash
docker run --rm -p 5000:5000 devhub01553/user-service:latest
```

Test:

```text
http://localhost:5000/health
```

The expected response is:

```json
{
  "status": "healthy"
}
```

---

# 10. Push Image to Docker Hub

Log in:

```bash
docker login
```

Push:

```bash
docker push devhub01553/user-service:latest
```

---

# 11. Kubernetes Deployment

The Kubernetes configuration contains:

* Deployment
* Service
* Ingress

Apply the Deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

Apply the Service:

```bash
kubectl apply -f k8s/service.yaml
```

Apply the Ingress:

```bash
kubectl apply -f k8s/ingress.yaml
```

---

# 12. Verify the Deployment

Check the Deployment:

```bash
kubectl get deployment user-service
```

Expected:

```text
NAME           READY   UP-TO-DATE   AVAILABLE
user-service   2/2     2            2
```

Check Pods:

```bash
kubectl get pods -l app=user-service
```

There should be two Pods.

Check the Service:

```bash
kubectl get service user-service
```

Check the Ingress:

```bash
kubectl get ingress my-app-ingress
```

Check rollout:

```bash
kubectl rollout status deployment/user-service
```

---

# 13. Kubernetes Health Checks

The Deployment contains two probes.

### Readiness Probe

The readiness probe checks:

```text
/health
```

on port:

```text
5000
```

A Pod is added to the Service endpoints only when it is ready.

### Liveness Probe

The liveness probe also checks:

```text
/health
```

If the application becomes unhealthy, Kubernetes can restart the container.

---

# 14. Service Configuration

The Service exposes:

```text
port: 80
```

and forwards traffic to:

```text
targetPort: 5000
```

The NodePort is:

```text
30007
```

Traffic therefore follows:

```text
NodePort 30007
       |
       v
Service port 80
       |
       v
Pod port 5000
       |
       v
Flask application
```

---

# 15. Ingress

The project uses an NGINX Ingress:

```text
my-app-ingress
```

The configured hostname is:

```text
myapp.local
```

The cluster must have an NGINX Ingress Controller installed for this resource to actually route traffic.

After the Ingress receives an address, map `myapp.local` to the Ingress IP in your local hosts file if necessary.

Then test:

```text
http://myapp.local/
```

or:

```text
http://myapp.local/health
```

and:

```text
http://myapp.local/users
```

---

# 16. GitHub Actions

The GitHub Actions workflow is located at:

```text
.github/workflows/ci-cd.yml
```

The pipeline performs:

```text
GitHub Push
     |
     v
Run Python Tests
     |
     v
Build Docker Image
     |
     v
Push Image to Docker Hub
```

The Docker image is tagged with:

```text
Git commit SHA
```

and:

```text
latest
```

---

# 17. GitHub Secrets

For Docker Hub publishing, configure these repository secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

`DOCKERHUB_TOKEN` should be a Docker Hub access token rather than your normal Docker Hub password.

---

# 18. Jenkins Pipeline

The repository also contains a `Jenkinsfile`.

The Jenkins pipeline performs:

```text
Checkout
   |
Build Docker Image
   |
Run Application Tests
   |
Push Image to Docker Hub
   |
Apply Kubernetes Manifests
   |
Update Deployment Image
   |
Wait for Rollout
   |
Verify Kubernetes Resources
```

---

# 19. Jenkins Requirements

The Jenkins agent must have access to:

* Docker
* kubectl
* Kubernetes cluster credentials
* Docker Hub credentials

Create a Jenkins credential with the ID:

```text
dockerhub-credentials
```

The credential should contain the Docker Hub username and access token/password.

The Jenkins agent must also be authenticated to the Kubernetes cluster before running:

```bash
kubectl apply
```

---

# 20. Useful Kubernetes Commands

View all resources:

```bash
kubectl get all
```

View Deployment:

```bash
kubectl get deployment user-service
```

View Pods:

```bash
kubectl get pods -l app=user-service
```

View Pod details:

```bash
kubectl describe pod <POD_NAME>
```

View logs:

```bash
kubectl logs <POD_NAME>
```

View Service:

```bash
kubectl get svc user-service
```

View Ingress:

```bash
kubectl get ingress my-app-ingress
```

View Deployment YAML:

```bash
kubectl get deployment user-service -o yaml
```

---

# 21. Troubleshooting

## ImagePullBackOff

Check:

```bash
kubectl describe pod <POD_NAME>
```

Verify that the Docker image exists:

```text
devhub01553/user-service:latest
```

---

## CrashLoopBackOff

Check logs:

```bash
kubectl logs <POD_NAME>
```

Check previous container logs if required:

```bash
kubectl logs <POD_NAME> --previous
```

---

## Readiness Probe Failing

Check the application directly:

```bash
kubectl exec -it <POD_NAME> -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/health').read().decode())"
```

The expected response should contain:

```text
healthy
```

Also verify that the container is listening on:

```text
5000
```

---

## Ingress Has No Address

Check:

```bash
kubectl get ingress my-app-ingress
```

Then verify that an NGINX Ingress Controller is installed and running.

---

## Check Service Endpoints

Run:

```bash
kubectl get endpoints user-service
```

If the endpoints are empty, check the Pod labels and readiness status:

```bash
kubectl get pods --show-labels
```

The Pods should have:

```text
app=user-service
```

---

# 22. Scaling

The Deployment starts with:

```yaml
replicas: 2
```

You can temporarily scale it:

```bash
kubectl scale deployment user-service --replicas=3
```

Verify:

```bash
kubectl get pods -l app=user-service
```

---

# 23. Rollout and Rollback

Check rollout:

```bash
kubectl rollout status deployment/user-service
```

View rollout history:

```bash
kubectl rollout history deployment/user-service
```

Rollback if necessary:

```bash
kubectl rollout undo deployment/user-service
```

---

# 24. Cleanup

Delete the Ingress:

```bash
kubectl delete -f k8s/ingress.yaml
```

Delete the Service:

```bash
kubectl delete -f k8s/service.yaml
```

Delete the Deployment:

```bash
kubectl delete -f k8s/deployment.yaml
```

Or delete all three:

```bash
kubectl delete -f k8s/
```

---

# 25. Important Application Limitation

The user data is stored in Python memory:

```python
users = [...]
```

This is intentional for this demonstration project.

It means:

* Data is lost when a Pod restarts.
* Each Pod has its own copy of the data.
* Data is not shared between replicas.
* This is not suitable for production persistence.

A production application should use a persistent database such as PostgreSQL or another appropriate data store.

---

# 26. Project Learning Objectives

This project demonstrates:

1. Building a REST API with Flask.
2. Creating a Docker image.
3. Running the application in a container.
4. Writing Kubernetes Deployment manifests.
5. Running multiple replicas.
6. Creating a Kubernetes Service.
7. Configuring readiness and liveness probes.
8. Exposing an application using Ingress.
9. Running automated tests.
10. Building Docker images through CI.
11. Publishing Docker images to Docker Hub.
12. Deploying to Kubernetes through Jenkins.

---

## 27. Final Deployment Flow

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +----> Run Tests
    |
    +----> Build Docker Image
    |
    v
Docker Hub
    |
    v
Jenkins
    |
    v
Kubernetes
    |
    v
Deployment
    |
    +---- Replica 1
    |
    +---- Replica 2
    |
    v
Service
    |
    v
NGINX Ingress
    |
    v
Flask REST API
```

---

## 28. Quick Start

For a quick Kubernetes deployment:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

Then verify:

```bash
kubectl get deployment user-service
kubectl get pods -l app=user-service
kubectl get service user-service
kubectl get ingress my-app-ingress
```

The expected Deployment state is:

```text
2/2 replicas ready
```

The application health endpoint is:

```text
/health
```

and should return:

```json
{
  "status": "healthy"
}
```
