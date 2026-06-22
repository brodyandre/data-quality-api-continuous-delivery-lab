# Pipeline Flow

Este repositorio separa claramente validacao tecnica e promocao entre ambientes.
O foco e demonstrar CI/CD com GitHub Actions, GitHub Environments e protecao de producao.

## Visao geral

- `pull_request` para `main`: executa CI
- `push` para `main`: executa CI e CD
- `workflow_dispatch`: permite executar os workflows manualmente

## CI

O workflow `ci.yml` valida a base do projeto antes de qualquer promocao.

Etapas principais:

1. checkout do codigo
2. setup do Python
3. instalacao de dependencias
4. execucao dos testes com `pytest`
5. validacao do build Docker
6. validacao dos overlays com `kubectl kustomize`

## CD

O workflow `cd-multi-environment.yml` demonstra promocao sequencial entre ambientes.

Sequencia dos jobs:

1. `build`
2. `deploy-development`
3. `deploy-staging`
4. `deploy-production`

Cada job de deploy:

- usa um GitHub Environment
- imprime as variaveis do ambiente
- aplica fallback caso `vars.APP_ENV`, `vars.QUALITY_THRESHOLD` ou `vars.LOG_LEVEL` ainda nao estejam configuradas
- simula o deploy renderizando o overlay com `kubectl kustomize`

## O que e simulado

Neste laboratorio:

- a imagem Docker e buildada, mas nao publicada
- os manifests sao renderizados por ambiente
- nao ha deploy real em cloud
- nao ha uso de secrets reais

## Execucao local opcional

O uso de `k3d` serve para demonstrar deploy local real em Kubernetes sem alterar o comportamento dos workflows remotos.
Os workflows do GitHub Actions continuam didaticos e independentes de cluster local.
