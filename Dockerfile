# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./
COPY .python-version ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy application code
COPY app ./app

# Expose port
EXPOSE 8080

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--forwarded-allow-ips", "*", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
