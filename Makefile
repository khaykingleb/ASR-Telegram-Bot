SHELL := /bin/bash
VERSION := 1.0.0
PYTHON := 3.10.5
CONDA_CH := defaults conda-forge pytorch
BASENAME := $(shell basename $(CURDIR))

##==================================================================================================
##@ Helper

help: ## Display help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: \033[36m\033[0m\n"} /^[a-zA-Z\.\%-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

##==================================================================================================
##@ Repo initialization

repo-pre-commit: ## Install pre-commit
	pre-commit install
	pre-commit install -t commit-msg
.PHONY: repo-pre-commit

repo-env-init: ## Ititialize environment
	conda create -n $(BASENAME) -y
.PHONY: repo-env-init

repo-deps: ## Install dependencies
	pip install -r requirements-pip.txt
	poetry config virtualenvs.create false --local && poetry install
.PHONY: repo-deps

repo-env-vars: ## Configure environment variables
	cat .test.env  > .env
	echo "dotenv" > .envrc
.PHONY: repo-env-vars

repo-init: repo-pre-commit repo-env-init repo-deps repo-env-vars ## Initialize repository by executing above commands
.PHONY: repo-init

##==================================================================================================
##@ Docker

docker-build:  ## Build docker images
	docker-compose up --build
.PHONY: docker-build

##==================================================================================================
##@ AWS

aws-model-pull: ## Pull model from S3 bucket
	poetry run dvc pull
.PHONY: aws-model-pull

##==================================================================================================
##@ Research

jupyter: ## Run jupyter lab
	poetry run jupyter lab
.PHONY:	jupyter

##==================================================================================================
##@ Secrets

gen-detect-secrets-baseline:  ## Create or update .secrets.baseline file
	poetry run detect-secrets scan > .secrets.baseline
.PHONY:	gen-detect-secrets-baseline

##==================================================================================================
##@ Checks

mypy: ## Run type checker
	poetry run mypy
.PHONY:	mypy

##==================================================================================================
##@ Cleaning

clean-general: ## Delete general files
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage
.PHONY: clean-general

clean-all: clean-general ## Delete all "junk" files
.PHONY: clean-all

##==================================================================================================
##@ Miscellaneous

upd-pre-commit-hooks:  ## Bump pre-commit hooks versions
	pre-commit autoupdate
.PHONY: upd-pre-commit-hooks
