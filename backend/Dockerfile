FROM python:3.12-slim

WORKDIR /app

# Copy agentx framework
COPY ../../agentx /app/agentx

# Copy backend
COPY . /app/backend

# Install dependencies
RUN pip install --no-cache-dir -e /app/agentx && \
    pip install --no-cache-dir aiohttp>=3.9.0

WORKDIR /app/backend

EXPOSE 8081

ENV AGENTX_PORT=8081
ENV AGENTX_LOG_LEVEL=INFO

CMD ["python", "app.py"]
