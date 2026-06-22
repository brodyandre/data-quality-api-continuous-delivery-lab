<a id="indice"></a>

# data-quality-api-continuous-delivery-lab

> Laboratorio pratico para demonstrar entrega continua com FastAPI, Docker, Kubernetes, Kustomize e GitHub Actions.

| Area | O que este repo cobre |
| --- | --- |
| API | FastAPI com endpoints simples para saude, versao, ambiente e relatorio de qualidade |
| CI | testes, validacao de build Docker e validacao de manifests |
| CD | promocao didatica entre `development`, `staging` e `production` |
| Governanca | uso de GitHub Environments e protecao de producao |
| Kubernetes local | execucao opcional com `k3d` e `kubectl port-forward` |

## Indice

1. [Titulo do projeto](#titulo-do-projeto)
2. [Resumo curto](#resumo-curto)
3. [Objetivo do laboratorio](#objetivo-do-laboratorio)
4. [Arquitetura resumida](#arquitetura-resumida)
5. [O que este projeto demonstra](#o-que-este-projeto-demonstra)
6. [Stack utilizada](#stack-utilizada)
7. [Fluxo da pipeline](#fluxo-da-pipeline)
8. [Environments usados](#environments-usados)
9. [Como rodar localmente](#como-rodar-localmente)
10. [Como rodar com Docker](#como-rodar-com-docker)
11. [Como validar Kubernetes/Kustomize](#como-validar-kuberneteskustomize)
12. [Como configurar GitHub Environments](#como-configurar-github-environments)
13. [Evidencias sugeridas com prints](#evidencias-sugeridas-com-prints)
14. [Proximos passos](#proximos-passos)

<a id="titulo-do-projeto"></a>

## 1. Titulo do projeto

`data-quality-api-continuous-delivery-lab`

Laboratorio voltado para estudo e demonstracao de CI/CD com foco em GitHub Actions, GitHub Environments, protecao de producao e entrega continua entre multiplos ambientes.

[Voltar ao indice](#indice)

<a id="resumo-curto"></a>

## 2. Resumo curto

Este projeto simula o ciclo de validacao e promocao de uma API pequena entre `development`, `staging` e `production`. O foco nao e cloud nem deploy real em producao, e sim a organizacao do fluxo, a separacao entre ambientes e a demonstracao de boas praticas de pipeline.

[Voltar ao indice](#indice)

<a id="objetivo-do-laboratorio"></a>

## 3. Objetivo do laboratorio

Demonstrar como estruturar um repositorio pequeno, claro e profissional para estudar:

- validacao automatizada em `pull requests` e `pushes`
- build local de imagem Docker
- organizacao de manifests com `Kustomize`
- promocao didatica entre ambientes
- uso de GitHub Environments com gates de aprovacao
- protecao de producao como parte do fluxo de entrega continua

O deploy deste laboratorio e simulado para fins didaticos. Nesta versao, nao ha deploy real em cloud e nao ha publicacao de imagem em registry.

[Voltar ao indice](#indice)

<a id="arquitetura-resumida"></a>

## 4. Arquitetura resumida

- `app/`: aplicacao FastAPI
- `tests/`: testes automatizados com `pytest`
- `Dockerfile`: empacotamento da API para execucao local
- `k8s/base/`: `Deployment` e `Service` compartilhados
- `k8s/overlays/`: variacoes por ambiente com `Kustomize`
- `.github/workflows/ci.yml`: pipeline de validacao
- `.github/workflows/cd-multi-environment.yml`: pipeline didatica de entrega continua
- `docs/`: material de apoio sobre ambientes, pipeline e execucao local

Documentos complementares:

- [docs/pipeline-flow.md](docs/pipeline-flow.md)
- [docs/environments.md](docs/environments.md)
- [docs/protection-rules.md](docs/protection-rules.md)
- [docs/local-kubernetes.md](docs/local-kubernetes.md)

[Voltar ao indice](#indice)

<a id="o-que-este-projeto-demonstra"></a>

## 5. O que este projeto demonstra

- pipeline de CI para `main`
- testes automatizados com `pytest`
- validacao de build Docker sem publicacao
- validacao de manifests Kubernetes com `kubectl kustomize`
- separacao clara entre `development`, `staging` e `production`
- uso de variaveis por ambiente com fallback em workflow
- promocao sequencial entre ambientes
- demonstracao opcional de deploy local real com `k3d`

[Voltar ao indice](#indice)

<a id="stack-utilizada"></a>

## 6. Stack utilizada

- Python
- FastAPI
- Pytest
- Docker
- Kubernetes
- Kustomize
- k3d
- GitHub Actions

[Voltar ao indice](#indice)

<a id="fluxo-da-pipeline"></a>

## 7. Fluxo da pipeline

### CI

O workflow `ci.yml` valida o projeto em `pull_request` para `main`, `push` para `main` e `workflow_dispatch`.

Etapas principais:

1. checkout do codigo
2. setup do Python
3. instalacao de dependencias
4. execucao dos testes com `pytest`
5. validacao do build Docker
6. validacao dos overlays com `kubectl kustomize`

### CD

O workflow `cd-multi-environment.yml` demonstra uma entrega continua em multiplos ambientes.

Sequencia:

1. `build`
2. `deploy-development`
3. `deploy-staging`
4. `deploy-production`

Cada job de deploy usa um GitHub Environment e simula a entrega renderizando o overlay correspondente. O objetivo e destacar governanca, promocao e protecao de producao, nao executar deploy real em cloud.

[Voltar ao indice](#indice)

<a id="environments-usados"></a>

## 8. Environments usados

| Environment | Uso no laboratorio | QUALITY_THRESHOLD | LOG_LEVEL | Replicas |
| --- | --- | --- | --- | --- |
| `development` | validacao inicial e feedback rapido | `80` | `debug` | `1` |
| `staging` | promocao intermediaria antes de producao | `90` | `info` | `1` |
| `production` | etapa final protegida do fluxo | `95` | `warning` | `2` |

Os manifests usam a mesma base e mudam apenas o necessario por ambiente.

[Voltar ao indice](#indice)

<a id="como-rodar-localmente"></a>

## 9. Como rodar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make test
make run
```

Depois disso, a API fica disponivel em `http://127.0.0.1:8000`.

Exemplos de teste:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/environment
curl http://127.0.0.1:8000/quality-report
```

[Voltar ao indice](#indice)

<a id="como-rodar-com-docker"></a>

## 10. Como rodar com Docker

```bash
make docker-build
docker run --rm -p 8000:8000 \
  -e APP_ENV=local \
  -e APP_VERSION=0.1.0 \
  -e QUALITY_THRESHOLD=90 \
  -e LOG_LEVEL=info \
  data-quality-api:local
```

Com o container em execucao:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/environment
curl http://127.0.0.1:8000/quality-report
```

[Voltar ao indice](#indice)

<a id="como-validar-kuberneteskustomize"></a>

## 11. Como validar Kubernetes/Kustomize

Sem cluster:

```bash
make k8s-validate
make render-development
make render-staging
make render-production
```

Execucao local opcional com `k3d`:

```bash
make cluster-create
make docker-build
make cluster-import-image
make k8s-deploy-dev
make k8s-status K8S_ENV=development
make k8s-port-forward
```

Guia detalhado: [docs/local-kubernetes.md](docs/local-kubernetes.md)

[Voltar ao indice](#indice)

<a id="como-configurar-github-environments"></a>

## 12. Como configurar GitHub Environments

Crie tres GitHub Environments:

- `development`
- `staging`
- `production`

Configure, quando desejar, estas variaveis:

- `APP_ENV`
- `QUALITY_THRESHOLD`
- `LOG_LEVEL`

Sugestao inicial:

- `development`: `APP_ENV=development`, `QUALITY_THRESHOLD=80`, `LOG_LEVEL=debug`
- `staging`: `APP_ENV=staging`, `QUALITY_THRESHOLD=90`, `LOG_LEVEL=info`
- `production`: `APP_ENV=production`, `QUALITY_THRESHOLD=95`, `LOG_LEVEL=warning`

Sugestao de governanca:

- `development` sem aprovacao manual
- `staging` como etapa intermediaria
- `production` com reviewers obrigatorios

Mesmo sem essas variaveis configuradas, os workflows usam fallback para continuar funcionais.

[Voltar ao indice](#indice)

<a id="evidencias-sugeridas-com-prints"></a>

## 13. Evidencias sugeridas com prints

Para apresentar este laboratorio a recrutadores tecnicos, vale registrar:

- execucao bem-sucedida do workflow `CI`
- execucao do workflow `CD Multi Environment`
- tela dos GitHub Environments configurados
- aprovacao manual ou regra de protecao de `production`
- logs de renderizacao por ambiente
- `make k8s-status` em um cluster local `k3d`
- respostas de `/health` e `/quality-report`

Os arquivos de apoio podem ficar em `docs/evidence/`.

[Voltar ao indice](#indice)

<a id="proximos-passos"></a>

## 14. Proximos passos

- publicar imagem em registry
- trocar o deploy simulado por aplicacao real em cluster
- adicionar verificacoes de seguranca e qualidade de imagem
- incluir testes de integracao na pipeline
- adicionar observabilidade basica para o ambiente local
- expandir a documentacao de branch protection e aprovacao de producao

[Voltar ao indice](#indice)
