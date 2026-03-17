# Cloud-Native Django Microservices Platform with Kubernetes & GitOps

A production-style cloud-native microservices project demonstrating modern DevOps and backend deployment practices using Django, RabbitMQ, Docker, Kubernetes, GitHub Actions, and GitOps principles.

This repository simulates a real-world microservices environment where services are built, containerized, deployed, and continuously delivered to a Kubernetes cluster through a GitOps-style workflow.

---

# Architecture Overview

## High-Level Flow

Developer Push → GitHub Actions (CI) → Docker Image Build → Docker Hub → GitOps-style Kubernetes Manifest Update → Kubernetes Cluster

---

## System Components

### Application Layer
- Auth Service (Django REST + JWT)
- User Service (Django REST)
- User Consumer Worker (RabbitMQ consumer)
- Event-driven service communication using RabbitMQ
- Stateless containerized services

### Infrastructure Layer
- Kubernetes manifests
- Docker containerization
- Docker Compose for local development
- Kubernetes-ready deployment structure

### CI/CD Layer
- GitHub Actions for Continuous Integration
- Docker Hub image publishing
- Declarative Kubernetes configuration
- GitOps-style image tag updates in manifests

---

# ⚙️ Technology Stack

## Application
- Python
- Django
- Django REST Framework
- Simple JWT
- RabbitMQ
- SQLite

## Infrastructure
- Docker
- Docker Compose
- Kubernetes

## CI/CD
- GitHub Actions
- Docker Hub
- GitOps-style manifest update flow

---

# Project Goals

This project demonstrates:

- Designing stateless microservices with clear service boundaries
- Using asynchronous communication with RabbitMQ
- Automating CI pipelines for Dockerized Django services
- Publishing versioned images to Docker Hub
- Updating Kubernetes manifests automatically from CI
- Maintaining production-style repository structure
- Separating local development, CI, and deployment concerns clearly

---

# Key Design Decisions

## Why Microservices?
To simulate independently deployable services with separate responsibilities:
- auth-service owns authentication and JWT issuing
- user-service owns user read data
- user-consumer handles async event processing

## Why RabbitMQ?
RabbitMQ allows decoupled asynchronous communication between services.
The auth service publishes a `USER_CREATED` event, and the user-consumer processes that event and syncs the user into the user-service database.

## Why Docker?
To ensure reproducible environments and consistent local and deployment workflows.

## Why Kubernetes?
To support orchestration, service separation, rolling updates, scaling, and production-style deployment patterns.

## Why Separate CI and CD?
CI:
- builds and validates services
- builds Docker images
- pushes images to Docker Hub
- updates Kubernetes manifests with new image tags

CD:
- is handled by Kubernetes / GitOps tooling consuming those manifests

This separation reflects production-style DevOps practices.

---

# Repository Structure

- `apps/` → application services
- `k8s/` → Kubernetes manifests
- `.github/workflows/` → GitHub Actions CI pipelines
- `docker-compose.yml` → local development environment

Example structure:

```text
k8s-ci-cd-microservice-python-django/
├─ apps/
│  ├─ auth-service/
│  └─ user-service/
├─ .github/workflows/
├─ k8s/
├─ docker-compose.yml
└─ README.md
```

---

## Services

### auth-service
Responsibilities:
- user signup
- user login
- JWT token generation
- publishing `USER_CREATED` event to RabbitMQ

Default local port:
- `8000`

---

### user-service
Responsibilities:
- storing synced user information
- returning user information via API

Default local port:
- `8001`

---

### user-consumer
Responsibilities:
- consuming `USER_CREATED` events from RabbitMQ
- syncing users into user-service database

---

### RabbitMQ
Responsibilities:
- message broker between services

Default ports:
- `5672`
- management UI: `15672`

---

## API Endpoints

### Auth Service
- `POST /api/auth/signup/`
- `POST /api/auth/login/`

### User Service
- `GET /api/users/`

---

## How It Works

### Signup Flow
1. Client sends signup request to **auth-service**
2. **auth-service** creates the user
3. **auth-service** publishes a `USER_CREATED` event to RabbitMQ
4. **user-consumer** receives the event
5. **user-consumer** stores the user data in the **user-service** database
6. **user-service** exposes the user data through API

---

### Login Flow
1. Client sends login request to **auth-service**
2. **auth-service** validates credentials
3. JWT access and refresh tokens are returned

---

## Local Development

Run the full stack locally:

```bash
docker compose up --build
```

This starts:
- RabbitMQ
- auth-service
- user-service
- user-consumer

---

## Docker Notes

This project uses **multi-stage Docker builds** for service images.

Benefits:
- cleaner production images
- better separation between build and runtime stages
- closer to real production container practices

---

## CI/CD Flow

### Continuous Integration
When code is pushed to `main`:

1. GitHub Actions builds Docker images
2. Images are pushed to Docker Hub
3. Images are tagged with:
   - `latest`
   - commit SHA
4. Kubernetes manifest image tags are updated automatically

---

### Continuous Deployment
The repository is structured for a GitOps-style deployment process where Kubernetes manifests are updated by CI and then applied by deployment tooling.

---

## Why This Project Is Valuable

This project demonstrates practical skills in:

- Django backend development
- JWT authentication
- event-driven microservices
- RabbitMQ integration
- Docker and Docker Compose
- Kubernetes-ready application design
- CI/CD automation with GitHub Actions
- Docker Hub image publishing
- GitOps-oriented deployment workflow

---

## Future Improvements

- replace SQLite with PostgreSQL
- add automated tests to CI
- add Kubernetes readiness and liveness probes
- add Ingress configuration
- add Argo CD for full GitOps deployment
- add Terraform for infrastructure provisioning
- add environment-specific deployment configuration

---

## Summary

This project is a cloud-native Django microservices platform built to practice and demonstrate real-world backend architecture, containerization, CI/CD, and Kubernetes deployment concepts in a production-style repository structure.
