# Environments

Este laboratorio usa tres ambientes para demonstrar promocao entre etapas de entrega continua sem depender de cloud ou deploy real em producao.

## Resumo

| Environment | Papel no fluxo | APP_ENV | QUALITY_THRESHOLD | LOG_LEVEL | Replicas |
| --- | --- | --- | --- | --- | --- |
| `development` | feedback rapido e validacao inicial | `development` | `80` | `debug` | `1` |
| `staging` | validacao intermediaria antes da promocao final | `staging` | `90` | `info` | `1` |
| `production` | etapa final protegida do laboratorio | `production` | `95` | `warning` | `2` |

## Como os ambientes sao aplicados

- `k8s/base` contem os manifests compartilhados da aplicacao.
- `k8s/overlays` define apenas o que muda por ambiente.
- os workflows de GitHub Actions usam `development`, `staging` e `production` como GitHub Environments.

## O que muda por ambiente

- `APP_ENV`
- `QUALITY_THRESHOLD`
- `LOG_LEVEL`
- quantidade de replicas

## Observacao

O objetivo desses ambientes e demonstrar organizacao, promocao e governanca.
Nesta versao, a entrega continua continua didatica e o deploy remoto permanece simulado.
