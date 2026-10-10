---
name: saas-stripe-billing-sync
description: Stripe billing and subscription portal synchronizer for B2B SaaS applications. Auto-scaffolds webhook handlers (checkout.session.completed, customer.subscription.updated), price tier definitions, and customer portal routes.
---

# SaaS Stripe Billing Sync (`/saas-stripe-billing-sync`)

## Overview
This skill automates the creation and validation of Stripe payment webhooks, subscription billing portals, and database entitlement checks.

---

## 1. Billing Protocol

When invoked, the agent MUST run:

1. **Webhook Signature & Payload Verification:**
   - Scaffolds `/api/webhooks/stripe` endpoint with signature verification (`stripe.webhooks.constructEvent`).

2. **Entitlement & Subscription Sync:**
   - Maps subscription statuses (`active`, `past_due`, `canceled`) to database organization tiers.

---

## 2. Usage Instructions

Run in Mission Control:
```bash
/saas-stripe-billing-sync
```
