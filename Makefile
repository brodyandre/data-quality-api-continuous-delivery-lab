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

.PHONY: help install run test cluster-create cluster-delete docker-build cluster-import-image \
	k8s-validate k8s-deploy-dev k8s-deploy-staging k8s-deploy-production \
	k8s-status k8s-port-forward k8s-clean render-development render-staging render-production

help:
	@printf "make install                 Instala dependencias do projeto.\n"
	@printf "make run                     Executa a API localmente.\n"
	@printf "make test                    Executa os testes automatizados.\n"
	@printf "make docker-build            Cria a imagem Docker local.\n"
	@printf "make cluster-create          Cria o cluster Kubernetes local com k3d.\n"
	@printf "make cluster-import-image    Importa a imagem Docker local para o cluster k3d.\n"
	@printf "make k8s-validate            Valida os overlays Kustomize de development, staging e production.\n"
	@printf "make k8s-deploy-dev          Faz deploy local no ambiente development.\n"
	@printf "make k8s-deploy-staging      Faz deploy local no ambiente staging.\n"
	@printf "make k8s-deploy-production   Faz deploy local no ambiente production.\n"
	@printf "make k8s-status              Mostra deployment, pods e service do ambiente configurado em K8S_ENV.\n"
	@printf "make k8s-port-forward        Expoe localmente o service da API na porta 8000.\n"
	@printf "make k8s-clean               Remove os recursos Kubernetes dos ambientes development, staging e production.\n"
	@printf "make cluster-delete          Remove o cluster Kubernetes local.\n"
	@printf "make render-development      Renderiza os manifests finais do ambiente development.\n"
	@printf "make render-staging          Renderiza os manifests finais do ambiente staging.\n"
	@printf "make render-production       Renderiza os manifests finais do ambiente production.\n"

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
