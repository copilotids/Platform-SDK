.PHONY: help install format lint type-check security
.PHONY: clean bump-patch bump-minor bump-major bump-build release
.PHONY: deb upload

.DEFAULT_GOAL := help


help: ## Show this help message
	@echo "Platform SDK - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

info: ## Show application and environment info
	@echo "🔧 Platform SDK Development Environment"
	@echo "Python version: $$(poetry run python --version)"
	@echo "Poetry version: $$(poetry --version)"
	@echo ""
	@echo "📦 Project Dependencies:"
	@poetry show --tree --only main | head -10


# ------------------------------------------------------------------------
# Code Quality

format: ## Format code with black and isort
	poetry run black src/
	poetry run isort src/

lint: ## Run flake8 linting
	poetry run flake8 src/

type-check: ## Run mypy type checking
	poetry run mypy src/

security: ## Run bandit security scanning (excluding external code)
	poetry run bandit -r src/

quality: format lint type-check security ## Run all code quality checks

check: quality ## Run all quality checks
	@echo "✅ All checks passed!"


# ------------------------------------------------------------------------
# Setup all dependencies

install: ## Install dependencies with Poetry
	poetry install


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
	poetry run bump2version patch

bump-minor: ## Bump minor version (e.g., 1.0.0 → 1.1.0)
	poetry run bump2version minor

bump-major: ## Bump major version (e.g., 1.0.0 → 2.0.0)
	poetry run bump2version major

bump-build: ## Bump build version (e.g., 1.0.0 → 1.0.0+1)
	poetry run bump2version build

version: ## Show current version
	@echo "Current version: $$(poetry version -s)"
	@echo "Git tags:"
	@git tag --sort=-version:refname | head -5


# ------------------------------------------------------------------------
# Release Management

release: check ## Create a release (run checks, bump minor version, push tags)
	@echo "🚀 Creating release..."
	@echo "Current version: $$(poetry version -s)"
	@read -p "Bump version (patch/minor/major) [minor]: " bump_type; \
	bump_type=$${bump_type:-minor}; \
	echo "Bumping $$bump_type version..."; \
	poetry run bump2version $$bump_type
	@echo "Pushing tags and commits..."
	git push origin master --tags
	@echo "✅ Release created! New version: $$(poetry version -s)"

release-patch: check ## Create a patch release
	@echo "🚀 Creating patch release..."
	poetry run bump2version patch
	git push origin master --tags
	@echo "✅ Patch release created! Version: $$(poetry version -s)"

release-minor: check ## Create a minor release
	@echo "🚀 Creating minor release..."
	poetry run bump2version minor
	git push origin master --tags
	@echo "✅ Minor release created! Version: $$(poetry version -s)"

release-major: check ## Create a major release
	@echo "🚀 Creating major release..."
	poetry run bump2version major
	git push origin master --tags
	@echo "✅ Major release created! Version: $$(poetry version -s)"


# ------------------------------------------------------------------------
# Deb creation and upload

deb:
	/bin/bash deploy/scripts/utility/create_deb.sh


NAME := platform-sdk
VERSION := $(shell cat VERSION)
PACKAGE_NAME := $(NAME)_$(VERSION).deb
PACKAGE_NAME_LATEST := $(NAME).deb
OWNCLOUD := https://owncloud.designcoaching.net

upload:
	ls -l deploy/builds/*deb
	curl --fail -u ids:ids -X PUT -H "Content-Type: multipart/form-data" \
	--data-binary "@deploy/builds/${PACKAGE_NAME}" ${OWNCLOUD}/remote.php/webdav/artefacts/${NAME}/${PACKAGE_NAME}
	curl --fail -u ids:ids -X PUT -H "Content-Type: multipart/form-data" \
	--data-binary "@deploy/builds/${PACKAGE_NAME}" ${OWNCLOUD}/remote.php/webdav/artefacts/latest/${PACKAGE_NAME_LATEST}
