---
name: model-fine-tuning-lab
description: Multi-agent AI model fine-tuning and quantization pipeline manager. Automates LoRA hyperparameter configuration, GGUF quantization (Q4_K_M, Q8_0), and vLLM inference server deployment checks.
---

# Model Fine-Tuning Lab (`/model-fine-tuning-lab`)

## Overview
This skill orchestrates open-source LLM fine-tuning (Unsloth, LLaMA-3, Qwen 2.5), quantization, and vLLM inference server deployment.

---

## 1. Fine-Tuning Execution Protocol

When invoked, the agent MUST run:

1. **Dataset & LoRA Hyperparameter Audit:**
   - Verify JSONL instruction dataset format (`instruction`, `input`, `output`).
   - Configure `r=16`, `lora_alpha=32`, and learning rate settings.

2. **GGUF Quantization & vLLM Serving Check:**
   - Convert safetensors to GGUF format (`Q4_K_M` / `Q8_0`).
   - Run latency and throughput health check on vLLM server.

---

## 2. Usage Instructions

Run in Mission Control:
```bash
/model-fine-tuning-lab
```
