# Ambientes

O laboratorio usa tres ambientes com a mesma base de deploy e pequenas variacoes por overlay:

- `development`: feedback rapido com threshold inicial de qualidade.
- `staging`: validacao antes da promocao final.
- `production`: configuracao mais restritiva.

## Variaveis por ambiente

| Ambiente | APP_ENV | APP_VERSION | QUALITY_THRESHOLD | LOG_LEVEL |
| --- | --- | --- | --- | --- |
| development | `development` | `0.1.0-development` | `90` | `info` |
| staging | `staging` | `0.1.0-staging` | `93` | `info` |
| production | `production` | `0.1.0` | `95` | `warning` |

Cada overlay adiciona namespace, sufixo de nome e `ConfigMap` proprio.
