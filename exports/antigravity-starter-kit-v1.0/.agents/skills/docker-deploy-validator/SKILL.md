---
name: docker-deploy-validator
description: Validates Dockerfiles, container security, non-root user enforcement, and docker-compose configurations. Use when containerizing apps or writing deployment manifests.
---
# Docker Deployment Validator

## Goal
Audit, secure, and validate Docker deployment manifests, ensuring compliance with container security best practices, non-root execution, and clean compose orchestration.

## Step-by-Step Instructions

1. **Security Audit & Syntax Check:**
   - Audit `Dockerfile` for minimal base images (e.g. `alpine`, `distroless`), proper layer caching, non-root user (`USER appuser`), and mandatory `HEALTHCHECK` directives.
   - Run `hadolint` or standard linter on Dockerfile if available.

2. **Compose Manifest Validation:**
   - Verify `docker-compose.yml` or `compose.yaml` using `docker compose config` to validate syntax, ports, and resource limits.

3. **Container Test Execution:**
   - Execute test build `docker compose up --build -d`.
   - Inspect container logs via `docker logs`.
   - Probe health endpoints and verify network isolation.
   - Clean up containers via `docker compose down`.

## Constraints
- Containers MUST run under non-root permissions.
- Hardcoded secrets inside Dockerfiles are strictly prohibited.
