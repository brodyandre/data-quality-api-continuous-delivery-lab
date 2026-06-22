# data-quality-api-continuous-delivery-lab

Laboratorio pratico de entrega continua com uma API simples de qualidade de dados, pipelines no GitHub Actions e manifests Kubernetes organizados por ambiente com `kustomize`.

## Stack

- Python
- FastAPI
- Pytest
- Docker
- GitHub Actions
- Kubernetes
- Kustomize

## Estrutura

```text
app/
tests/
k8s/
.github/workflows/
docs/
```

## Como executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make test
make run
```

API disponivel em `http://127.0.0.1:8000` e documentacao interativa em `http://127.0.0.1:8000/docs`.

## Comandos

```bash
# criar ambiente virtual
python3 -m venv .venv

# ativar ambiente virtual
source .venv/bin/activate

# instalar dependencias
pip install -r requirements.txt -r requirements-dev.txt

# rodar testes
make test

# rodar API localmente
make run

# buildar imagem Docker
docker build -t data-quality-api:local .

# executar container Docker
docker run --rm -p 8000:8000 \
  -e APP_ENV=local \
  -e APP_VERSION=0.1.0 \
  -e QUALITY_THRESHOLD=90 \
  -e LOG_LEVEL=info \
  data-quality-api:local
```

## Endpoints

- `GET /health`
- `GET /version`
- `GET /environment`
- `GET /quality-report`

## Running on local Kubernetes

O suporte a `k3d` e opcional e nao faz parte obrigatoria dos testes ou do CD.

```bash
make cluster-create
make docker-build
make cluster-import-image
make k8s-deploy-dev
make k8s-status K8S_ENV=development
make k8s-port-forward
```

Detalhes adicionais em `docs/local-kubernetes.md`.

## Exemplos curl

```bash
curl http://127.0.0.1:8000/health

curl http://127.0.0.1:8000/version

curl http://127.0.0.1:8000/environment

curl http://127.0.0.1:8000/quality-report
```

## Fluxo do laboratorio

- `ci.yml`: instala dependencias, executa testes, valida overlays e faz build da imagem Docker.
- `cd-multi-environment.yml`: renderiza manifests para `development`, `staging` e `production` em sequencia.

Os detalhes de ambientes e protecoes ficam em `docs/`.
