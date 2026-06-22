# Local Kubernetes

Este fluxo e opcional e existe para demonstrar o laboratorio em um cluster Kubernetes local com `k3d`.
Ele nao altera os workflows do GitHub Actions e nao e necessario para rodar os testes.

## Requisitos

- Docker Desktop ou Docker Engine
- `k3d`
- `kubectl`

## Fluxo recomendado

1. criar o cluster local
2. buildar a imagem Docker
3. importar a imagem para o cluster
4. aplicar o overlay `development`
5. verificar deployment, pods e service
6. fazer `port-forward`
7. testar a API com `curl`

## Comandos principais

```bash
make cluster-create
make docker-build
make cluster-import-image
make k8s-deploy-dev
make k8s-status K8S_ENV=development
make k8s-port-forward
```

Com o `port-forward` ativo:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/quality-report
```

## Outros ambientes

Se quiser trocar de ambiente no cluster local:

```bash
make k8s-clean
make k8s-deploy-staging
make k8s-status K8S_ENV=staging
```

Ou:

```bash
make k8s-clean
make k8s-deploy-production
make k8s-status K8S_ENV=production
```

## Observacao importante

Nesta versao, os manifests usam os mesmos nomes de `Deployment` e `Service`.
Por isso, a forma mais simples de demonstracao local e usar um ambiente por vez no cluster.

## Validacao sem cluster

Para validar os overlays sem criar cluster:

```bash
make k8s-validate
```

## Limpeza

```bash
make k8s-clean
make cluster-delete
```
