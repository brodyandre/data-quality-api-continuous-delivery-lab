# Pipeline Flow

## CI

Em `push` e `pull_request`, o workflow `ci.yml`:

1. instala dependencias
2. executa os testes com `pytest`
3. valida os manifests com `kustomize build`
4. faz build da imagem Docker

## CD

Em `push` para `main` ou acionamento manual, o workflow `cd-multi-environment.yml`:

1. renderiza o overlay de `development`
2. renderiza o overlay de `staging`
3. renderiza o overlay de `production`

## Estrutura dos manifests

`k8s/base` guarda os manifests compartilhados da aplicacao:

- `Deployment`
- `Service`

Cada overlay em `k8s/overlays` define apenas o que muda por ambiente:

- `APP_ENV`
- `QUALITY_THRESHOLD`
- `LOG_LEVEL`
- quantidade de replicas

Nesta versao:

- `development`: 1 replica, threshold `80`, log `debug`
- `staging`: 1 replica, threshold `90`, log `info`
- `production`: 2 replicas, threshold `95`, log `warning`

Neste laboratorio, o workflow de CD gera os manifests renderizados como artefatos.
Quando houver cluster e credenciais, a entrega pode usar `kubectl apply -k k8s/overlays/<ambiente>`.
