PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
KUSTOMIZE ?= kubectl kustomize
TEST_PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,$(PYTHON))

.PHONY: install run test docker-build render-development render-staging render-production

install:
	$(PIP) install -r requirements.txt -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	$(TEST_PYTHON) -m pytest -q

docker-build:
	docker build -t data-quality-api:local .

render-development:
	$(KUSTOMIZE) k8s/overlays/development

render-staging:
	$(KUSTOMIZE) k8s/overlays/staging

render-production:
	$(KUSTOMIZE) k8s/overlays/production
