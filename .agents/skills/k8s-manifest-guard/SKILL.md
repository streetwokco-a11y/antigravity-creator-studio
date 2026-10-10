---
name: k8s-manifest-guard
description: Automated Kubernetes manifest and GitOps security auditor. Scans Kustomize and Helm manifests for missing resource limits, insecure privileged mode, missing liveness/readiness probes, and non-root user enforcement.
---

# Kubernetes Manifest Guard (`/k8s-manifest-guard`)

## Overview
This skill provides automated security and reliability auditing for Kubernetes manifests, Helm charts, and Kustomize overlays before deployment into production clusters.

---

## 1. Audit Checklist

When invoked, the agent MUST perform the following checks:

1. **Security Context Audit:**
   - Enforce `runAsNonRoot: true` and `allowPrivilegeEscalation: false`.
   - Flag any container running as root or with `privileged: true`.

2. **Resource Requests & Limits:**
   - Verify `resources.limits` and `resources.requests` for CPU and Memory.
   - Flag un-bounded containers to prevent node OOM events.

3. **Health Probe Verification:**
   - Check presence of `readinessProbe` and `livenessProbe`.

---

## 2. Usage Instructions

Run in Mission Control:
```bash
/k8s-manifest-guard
```
