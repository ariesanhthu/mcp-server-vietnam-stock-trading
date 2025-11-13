# Docker Deployment Guide

Hướng dẫn nhanh để deploy vnstock-mcp-server với Docker.

## Quick Start

### Build và chạy local

```bash
# Build image
make build
# hoặc
docker build -t vnstock-mcp-server:latest .

# Chạy với docker-compose
make run
# hoặc
docker-compose up -d

# Xem logs
make logs
# hoặc
docker-compose logs -f
```

### Test

```bash
# Test server (với SSE/HTTP transport)
curl http://localhost:8000
```

## Docker Compose

### Development

```bash
docker-compose up -d
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

Tạo file `.env`:

```env
TRANSPORT=sse
MOUNT_PATH=/
PORT=8000
```

## Makefile Commands

```bash
make help          # Xem tất cả commands
make build         # Build Docker image
make run           # Chạy container
make stop          # Dừng container
make logs          # Xem logs
make test          # Test server
make clean         # Clean up
make deploy-local  # Build và run
```

## Deploy lên Cloud

Xem file [DEPLOY.md](./DEPLOY.md) để biết chi tiết cách deploy lên:

- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Instances

### Quick Deploy Scripts

```bash
# Deploy lên Google Cloud Run
make deploy-gcp
# hoặc
./scripts/deploy.sh gcp

# Deploy lên AWS
make deploy-aws
# hoặc
./scripts/deploy.sh aws

# Deploy lên Azure
make deploy-azure
# hoặc
./scripts/deploy.sh azure
```

## Transport Modes

Server hỗ trợ 3 transport modes:

1. **stdio** - Cho desktop MCP clients (không dùng trong Docker)
2. **sse** - Server-Sent Events (khuyến nghị cho cloud)
3. **streamable-http** - HTTP streaming (cho API services)

Đổi transport mode bằng environment variable:

```bash
docker run -e TRANSPORT=sse vnstock-mcp-server:latest
```

## Troubleshooting

### Container không start

```bash
# Check logs
docker logs vnstock-mcp-server

# Check status
docker ps -a
```

### Port conflict

Thay đổi port mapping trong `docker-compose.yml`:

```yaml
ports:
  - "8001:8000" # Map host port 8001 to container port 8000
```

### Health check failed

Health check sử dụng `pgrep` để kiểm tra process. Nếu failed, check logs:

```bash
docker-compose logs vnstock-mcp-server
```

## Production Best Practices

1. Sử dụng `docker-compose.prod.yml` với resource limits
2. Enable logging với rotation
3. Sử dụng reverse proxy (Nginx) nếu cần
4. Monitor container health
5. Set up auto-restart policies

## Support

Xem [DEPLOY.md](./DEPLOY.md) để biết thêm chi tiết về deployment.
