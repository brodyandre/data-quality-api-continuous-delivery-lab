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
make run
```

API disponivel em `http://127.0.0.1:8000` e documentacao interativa em `http://127.0.0.1:8000/docs`.

## Comandos uteis

```bash
make test
make docker-build
make render-development
make render-staging
make render-production
```

## Fluxo do laboratorio

- `ci.yml`: instala dependencias, executa testes, valida overlays e faz build da imagem Docker.
- `cd-multi-environment.yml`: renderiza manifests para `development`, `staging` e `production` em sequencia.

Os detalhes de ambientes e protecoes ficam em `docs/`.
