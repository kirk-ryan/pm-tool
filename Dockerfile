# Stage 1: Build NextJS frontend
FROM node:20-slim AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend
FROM python:3.12-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy backend
COPY backend/ ./backend/

# Install dependencies
RUN cd backend && uv sync --no-install-project

# Copy built frontend from stage 1
COPY --from=frontend-builder /frontend/out ./frontend_out

# Expose port
EXPOSE 8000

# Make backend/ importable so `from db import ...` resolves inside main.py
ENV PYTHONPATH=/app/backend

# Run
CMD ["uv", "run", "--project", "backend", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
