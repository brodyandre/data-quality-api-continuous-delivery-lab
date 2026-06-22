# Local Kubernetes

Este laboratorio pode ser executado localmente em Kubernetes com `k3d`.
Esse fluxo e opcional e nao altera os workflows do GitHub Actions.

## Requisitos

- Docker Desktop ou Docker Engine
- `k3d`
- `kubectl`

## Fluxo rapido

1. criar o cluster local
2. buildar a imagem Docker
3. importar a imagem para o cluster
4. aplicar o overlay desejado
5. verificar os recursos
6. fazer `port-forward`
7. testar a API com `curl`

## Comandos

```bash
make cluster-create
make docker-build
make cluster-import-image
make k8s-deploy-dev
make k8s-status K8S_ENV=development
make k8s-port-forward
```

Com o `port-forward` ativo, teste a API em outro terminal:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/quality-report
```

## Outros ambientes

Para aplicar outro overlay:

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

Os manifests desta versao usam os mesmos nomes de `Deployment` e `Service`.
Por isso, a forma mais simples e usar um ambiente por vez no cluster local.

## Validacao dos manifests

Para validar os overlays sem criar cluster:

```bash
make k8s-validate
```

## Limpeza

```bash
make k8s-clean
make cluster-delete
```
