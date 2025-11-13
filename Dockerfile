# Single-stage Dockerfile for vnstock-mcp-server
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv using official installer (system-wide)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.cargo/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv
ENV PATH="/usr/local/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser uv.lock* ./

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser MANIFEST.in ./

# Install dependencies with uv (as root, then fix permissions)
RUN uv sync --frozen && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for SSE/HTTP transport
EXPOSE 8000

# Health check - check if process is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD pgrep -f "python -m vnstock_mcp.server" || exit 1

# Default command: run with SSE transport for cloud deployment
# Users can override with docker run or docker-compose
# Using uv run to execute from source code
CMD ["uv", "run", "python", "-m", "vnstock_mcp.server", "--transport", "sse", "--mount-path", "/"]

