# Local Machine Orchestration Makefile
# =====================================

.PHONY: help start stop restart status logs clean setup test deploy

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
help:
	@echo "$(GREEN)Local Machine Orchestration Commands$(NC)"
	@echo "=========================================="
	@echo ""
	@echo "$(YELLOW)Orchestration Services:$(NC)"
	@echo "  make start          - Start all orchestration services (n8n + Prefect)"
	@echo "  make stop           - Stop all orchestration services"
	@echo "  make restart        - Restart all orchestration services"
	@echo "  make status         - Show status of all services"
	@echo "  make logs           - Show logs from all services"
	@echo ""
	@echo "$(YELLOW)n8n Workflow Automation:$(NC)"
	@echo "  make n8n-start      - Start only n8n service"
	@echo "  make n8n-stop       - Stop only n8n service"
	@echo "  make n8n-logs       - View n8n logs"
	@echo "  make n8n-backup     - Backup n8n workflows and credentials"
	@echo "  make n8n-restore    - Restore n8n from backup"
	@echo ""
	@echo "$(YELLOW)Prefect Workflow Orchestration:$(NC)"
	@echo "  make prefect-start  - Start Prefect server and agent"
	@echo "  make prefect-stop   - Stop Prefect services"
	@echo "  make prefect-logs   - View Prefect logs"
	@echo "  make prefect-deploy - Deploy example Prefect flows"
	@echo "  make prefect-test   - Test Prefect flows"
	@echo ""
	@echo "$(YELLOW)Development & Testing:$(NC)"
	@echo "  make setup          - Set up Python environment and dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make lint           - Lint Python code"
	@echo "  make format         - Format Python code"
	@echo ""
	@echo "$(YELLOW)Data Pipeline Examples:$(NC)"
	@echo "  make data-pipeline  - Run example data pipeline"
	@echo "  make ml-pipeline    - Run example ML training pipeline"
	@echo "  make etl-pipeline   - Run example ETL pipeline"
	@echo ""
	@echo "$(YELLOW)Maintenance:$(NC)"
	@echo "  make clean          - Clean up temporary files and containers"
	@echo "  make prune          - Prune Docker system"
	@echo "  make update         - Update all Docker images"

# Docker Compose Commands
start:
	@echo "$(GREEN)Starting all orchestration services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "  n8n:      http://localhost:5678"
	@echo "  Prefect:  http://localhost:4200"
	@echo ""
	@echo "Default credentials:"
	@echo "  n8n:      admin / password123"
	@echo "  Prefect:  No authentication by default"

stop:
	@echo "$(YELLOW)Stopping all orchestration services...$(NC)"
	docker-compose down

restart: stop start

status:
	@echo "$(GREEN)Service Status:$(NC)"
	docker-compose ps

logs:
	@echo "$(GREEN)Service Logs:$(NC)"
	docker-compose logs -f

# n8n Specific Commands
n8n-start:
	@echo "$(GREEN)Starting n8n service...$(NC)"
	docker-compose up -d n8n

n8n-stop:
	@echo "$(YELLOW)Stopping n8n service...$(NC)"
	docker-compose stop n8n

n8n-logs:
	@echo "$(GREEN)n8n Logs:$(NC)"
	docker-compose logs -f n8n

n8n-backup:
	@echo "$(GREEN)Backing up n8n data...$(NC)"
	@mkdir -p backups
	docker cp n8n:/home/node/.n8n backups/n8n_backup_$(shell date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)Backup created in backups/ directory$(NC)"

n8n-restore:
	@echo "$(YELLOW)Restoring n8n from backup...$(NC)"
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)Error: Please specify backup directory with BACKUP=path/to/backup$(NC)"; \
		exit 1; \
	fi
	docker stop n8n
	docker cp $(BACKUP)/. n8n:/home/node/.n8n
	docker start n8n
	@echo "$(GREEN)n8n restored from $(BACKUP)$(NC)"

# Prefect Specific Commands
prefect-start:
	@echo "$(GREEN)Starting Prefect services...$(NC)"
	docker-compose up -d prefect-server prefect-db prefect-agent

prefect-stop:
	@echo "$(YELLOW)Stopping Prefect services...$(NC)"
	docker-compose stop prefect-server prefect-db prefect-agent

prefect-logs:
	@echo "$(GREEN)Prefect Logs:$(NC)"
	docker-compose logs -f prefect-server prefect-agent

prefect-deploy:
	@echo "$(GREEN)Deploying example Prefect flows...$(NC)"
	python -c "from prefect_flows.example_flows import deploy_all; deploy_all()"

prefect-test:
	@echo "$(GREEN)Testing Prefect flows...$(NC)"
	python -m pytest tests/ -v

# Development Setup
setup:
	@echo "$(GREEN)Setting up Python environment...$(NC)"
	python -m venv venv
	@echo "$(GREEN)Activate the virtual environment:$(NC)"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Unix/Mac: source venv/bin/activate"
	@echo ""
	@echo "$(GREEN)Then install dependencies:$(NC)"
	@echo "  pip install -r requirements.txt"

test:
	@echo "$(GREEN)Running tests...$(NC)"
	python -m pytest tests/ -v

lint:
	@echo "$(GREEN)Linting Python code...$(NC)"
	python -m black prefect_flows/ tests/ --check
	python -m flake8 prefect_flows/ tests/

format:
	@echo "$(GREEN)Formatting Python code...$(NC)"
	python -m black prefect_flows/ tests/

# Example Pipelines
data-pipeline:
	@echo "$(GREEN)Running example data pipeline...$(NC)"
	python prefect_flows/data_pipeline.py

ml-pipeline:
	@echo "$(GREEN)Running example ML training pipeline...$(NC)"
	python prefect_flows/ml_pipeline.py

etl-pipeline:
	@echo "$(GREEN)Running example ETL pipeline...$(NC)"
	python prefect_flows/etl_pipeline.py

# Maintenance
clean:
	@echo "$(YELLOW)Cleaning up...$(NC)"
	docker-compose down -v
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

prune:
	@echo "$(YELLOW)Pruning Docker system...$(NC)"
	docker system prune -f

update:
	@echo "$(GREEN)Updating Docker images...$(NC)"
	docker-compose pull