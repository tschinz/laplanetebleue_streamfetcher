.PHONY: help clean data docs lint install uninstall export update env image container

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_INTERPRETER = python
CONDA_ENV_FILE = condaenv.yml
CONDA_ENV_NAME = laplanetebleue-env
APP_ENTRY = src/lpb_streamfetcher.py
IMAGE_NAME = lpb-image
CONTAINER_NAME = lpb-container

ifeq (,$(shell where conda))
HAS_CONDA=False
else
HAS_CONDA=True
SEARCH_ENV=$(shell conda.bat info --envs | grep $(CONDA_ENV_NAME))
FOUND_ENV_NAME = $(word 1, $(notdir $(SEARCH_ENV)))
# check if conda environment is active
ifneq ($(CONDA_DEFAULT_ENV),$(FOUND_ENV_NAME))
	CONDA_ACTIVATE := source $$(conda.bat info --base)/etc/profile.d/conda.sh ; conda activate $(CONDA_ENV_NAME)
else
    CONDA_ACTIVATE := true
endif
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

lint: ## Lint the python package
	@$(CONDA_ACTIVATE); pylint src

app: ## Start application
	@$(CONDA_ACTIVATE); python $(APP_ENTRY) -a -v

app-node: ## Start application for storing on node server
	@$(CONDA_ACTIVATE); python $(APP_ENTRY) -a -v -o '\\\\node.local\\multimedia\\Music\\Podcast\\La Planète Bleue\\'

.ONESHELL:
image:  ## Build docker image
	@$(CONDA_ACTIVATE)
	@$(PYTHON_INTERPRETER) helpers.py pre_image_build "$(IMAGE_NAME)"
	@docker build -t $(IMAGE_NAME) .
	@echo
	@echo ">>> Docker image created. Start a container with 'make container'."

container: ## Start image as container
	@docker container rm -f $(IMAGE_NAME)
	@echo ">>> Application started. $(IMAGE_NAME) as $(CONTAINER_NAME)"
	@docker run -v //c/data:/data --name $(CONTAINER_NAME) $(IMAGE_NAME)

env: ## Set up conda environment
ifeq (True,$(HAS_CONDA))
ifneq ($(FOUND_ENV_NAME),)
	@echo ">>> Found '$(CONDA_ENV_NAME)' environment. Skipping installation..."
else
	@echo ">>> Creating conda environment $(CONDA_ENV_NAME)"
	@conda env create -f $(CONDA_ENV_FILE) -n $(CONDA_ENV_NAME)
endif
else
	@echo ">>> Please install Anaconda you mammal!"
endif

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

