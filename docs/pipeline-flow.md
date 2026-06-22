# Pipeline Flow

## CI

Em `push` e `pull_request`, o workflow `ci.yml`:

1. instala dependencias
2. executa os testes com `pytest`
3. valida os overlays com `kustomize build`
4. faz build da imagem Docker

## CD

Em `push` para `main` ou acionamento manual, o workflow `cd-multi-environment.yml`:

1. renderiza manifests de `development`
2. promove para `staging`
3. promove para `production`

Neste laboratorio, a etapa de deploy gera os manifests renderizados como artefatos.
Quando houver cluster e credenciais, essa etapa pode ser trocada por `kubectl apply -k`.
