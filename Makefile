.PHONY: help install format lint type-check security
.PHONY: clean bump-patch bump-minor bump-major bump-build

.DEFAULT_GOAL := help


help: ## Show this help message
	@echo "Platform SDK - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

info: ## Show application and environment info
	@echo "🔧 Platform SDK Development Environment"
	@echo "Python version: $$(uv run python --version)"
	@echo "UV version: $$(uv --version)"
	@echo ""
	@echo "📦 Project Dependencies:"
	@uv tree --depth 1


# ------------------------------------------------------------------------
# Code Quality

format: ## Format code with ruff
	uv run ruff format platform_sdk/
	uv run ruff check --select I --fix platform_sdk/

lint: ## Run ruff linting
	uv run ruff check platform_sdk/

type-check: ## Run mypy type checking
	uv run mypy platform_sdk/

security: ## Run ruff security scanning (bandit rules)
	uv run ruff check --select S platform_sdk/

quality: format lint type-check security ## Run all code quality checks

check: quality ## Run all quality checks
	@echo "✅ All checks passed!"


# ------------------------------------------------------------------------
# Running the system (development environment)

clean: ## Clean temporary files and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage


# ------------------------------------------------------------------------
# Versioning

bump-patch: ## Bump patch version (e.g., 1.0.0 → 1.0.1)
	uv run bump2version patch

bump-minor: ## Bump minor version (e.g., 1.0.0 → 1.1.0)
	uv run bump2version minor

bump-major: ## Bump major version (e.g., 1.0.0 → 2.0.0)
	uv run bump2version major

bump-build: ## Bump build version (e.g., 1.0.0 → 1.0.0+1)
	uv run bump2version build

version: ## Show current version
	@echo "Current version: $$(cat VERSION)"
	@echo "Git tags:"
	@git tag --sort=-version:refname | head -5