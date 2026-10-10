# Stage 1: Build & Security Hardening
FROM python:3.12-slim AS runtime

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Enforce non-root execution
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

# Copy dependency specifications
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and grant ownership to non-root user
COPY backend/ ./backend/
COPY leads.db .
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Built-in health probe
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
