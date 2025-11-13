.PHONY: help build run stop logs test clean deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker image
	docker build -t vnstock-mcp-server:latest .

build-simple: ## Build Docker image (simple version)
	docker build -f Dockerfile.simple -t vnstock-mcp-server:latest .

run: ## Run container with docker-compose
	docker-compose up -d

run-prod: ## Run container with production config
	docker-compose -f docker-compose.prod.yml up -d

run-http: ## Run container with streamable-http transport
	docker-compose -f docker-compose.streamable-http.yml up -d

stop: ## Stop containers
	docker-compose down

logs: ## View logs
	docker-compose logs -f vnstock-mcp-server

test: ## Test the server
	curl -v http://localhost:8000/ || echo "Server may not be running with HTTP transport"

clean: ## Clean up Docker resources
	docker-compose down -v
	docker rmi vnstock-mcp-server:latest || true

deploy-local: build run ## Build and run locally

deploy-http: build run-http ## Build and run with streamable-http

deploy-gcp: ## Deploy to Google Cloud Run
	@./scripts/deploy.sh gcp

deploy-aws: ## Deploy to AWS ECS
	@./scripts/deploy.sh aws

deploy-azure: ## Deploy to Azure Container Instances
	@./scripts/deploy.sh azure

shell: ## Open shell in container
	docker-compose exec vnstock-mcp-server /bin/bash

restart: stop run ## Restart containers

