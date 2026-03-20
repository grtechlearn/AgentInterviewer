FROM python:3.12-slim

WORKDIR /app

# Install git for pip to clone from GitHub
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Install AgentX framework from GitHub
RUN pip install --no-cache-dir "agentx @ git+https://github.com/grtechlearn/agentx.git@main"

# Install additional dependencies
RUN pip install --no-cache-dir aiohttp>=3.9.0

# Copy backend code
COPY . /app

EXPOSE 8081

ENV AGENTX_PORT=8081
ENV AGENTX_LOG_LEVEL=INFO

CMD ["python", "app.py"]
