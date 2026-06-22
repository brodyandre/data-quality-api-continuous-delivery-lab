# Ambientes

O laboratorio usa tres ambientes com a mesma base de deploy e pequenas variacoes por overlay:

- `development`: feedback rapido, limiar de nulos mais permissivo.
- `staging`: validacao antes da promocao final.
- `production`: configuracao mais restritiva.

## Variaveis por ambiente

| Ambiente | APP_ENV | APP_VERSION | DEFAULT_NULL_THRESHOLD |
| --- | --- | --- | --- |
| development | `development` | `0.1.0-development` | `0.25` |
| staging | `staging` | `0.1.0-staging` | `0.15` |
| production | `production` | `0.1.0` | `0.05` |

Cada overlay adiciona namespace, sufixo de nome e `ConfigMap` proprio.
