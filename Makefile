PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
K3D ?= k3d
KUBECTL ?= kubectl
KUSTOMIZE ?= kubectl kustomize
TEST_PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,$(PYTHON))
IMAGE ?= data-quality-api:local
CLUSTER_NAME ?= data-quality-lab
K8S_ENV ?= development
PORT_FORWARD_PORT ?= 8000

.PHONY: install run test cluster-create cluster-delete docker-build cluster-import-image \
	k8s-validate k8s-deploy-dev k8s-deploy-staging k8s-deploy-production \
	k8s-status k8s-port-forward k8s-clean render-development render-staging render-production

install:
	$(PIP) install -r requirements.txt -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	$(TEST_PYTHON) -m pytest -q

docker-build:
	docker build -t $(IMAGE) .

cluster-create:
	$(K3D) cluster create $(CLUSTER_NAME) --agents 1

cluster-delete:
	$(K3D) cluster delete $(CLUSTER_NAME)

cluster-import-image:
	$(K3D) image import $(IMAGE) -c $(CLUSTER_NAME)

k8s-validate:
	$(KUSTOMIZE) k8s/overlays/development > /dev/null
	$(KUSTOMIZE) k8s/overlays/staging > /dev/null
	$(KUSTOMIZE) k8s/overlays/production > /dev/null

k8s-deploy-dev:
	$(KUBECTL) apply -k k8s/overlays/development

k8s-deploy-staging:
	$(KUBECTL) apply -k k8s/overlays/staging

k8s-deploy-production:
	$(KUBECTL) apply -k k8s/overlays/production

k8s-status:
	$(KUBECTL) get deployment,pods,service -l app.kubernetes.io/name=data-quality-api,app.kubernetes.io/environment=$(K8S_ENV)

k8s-port-forward:
	$(KUBECTL) port-forward service/data-quality-api $(PORT_FORWARD_PORT):8000

k8s-clean:
	-$(KUBECTL) delete -k k8s/overlays/development --ignore-not-found
	-$(KUBECTL) delete -k k8s/overlays/staging --ignore-not-found
	-$(KUBECTL) delete -k k8s/overlays/production --ignore-not-found

render-development:
	$(KUSTOMIZE) k8s/overlays/development

render-staging:
	$(KUSTOMIZE) k8s/overlays/staging

render-production:
	$(KUSTOMIZE) k8s/overlays/production
