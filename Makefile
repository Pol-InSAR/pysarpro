#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = pysarpro
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
MAMBA_ACTIVATE=source $$(mamba info --base)/etc/profile.d/mamba.sh ; mamba activate ; mamba activate


## Install Python Dependencies
.PHONY: requirements
requirements:
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune
	

## Install Python Dev Dependencies
.PHONY: dev
dev:
	mamba create --yes --name $(PROJECT_NAME)-dev python=3.11 pre-commit 
	$(CONDA_ACTIVATE) $(PROJECT_NAME)-dev
	pip install -r requirements.txt
	pip install -r requirements/build.txt
	pip install -r requirements/docs.txt

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 pysarpro
	black --check --config pyproject.toml pysarpro


## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml pysarpro




## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	conda env create --name $(PROJECT_NAME) -f environment.yml
	
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) pysarpro/data/make_dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)