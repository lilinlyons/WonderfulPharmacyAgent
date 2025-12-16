# Build stage for frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Backend stage
FROM python:3.10-slim
WORKDIR /app

# Install Node.js for frontend serving (optional, if you want to serve frontend from same container)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

# Expose ports
EXPOSE 8000

# Load .env and run
CMD ["sh", "-c", "set -a && [ -f .env ] && source .env && set +a && uvicorn app:app --host 0.0.0.0 --port 8000"]
