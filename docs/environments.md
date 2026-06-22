# Ambientes

O laboratorio usa tres ambientes com a mesma base de deploy e pequenas variacoes por overlay:

- `development`: feedback rapido com threshold inicial de qualidade.
- `staging`: validacao antes da promocao final.
- `production`: configuracao mais restritiva.

## Variaveis por ambiente

| Ambiente | APP_ENV | QUALITY_THRESHOLD | LOG_LEVEL | Replicas |
| --- | --- | --- | --- | --- |
| development | `development` | `80` | `debug` | `1` |
| staging | `staging` | `90` | `info` | `1` |
| production | `production` | `95` | `warning` | `2` |

Cada overlay reutiliza a mesma base e muda apenas as variaveis de ambiente e a quantidade de replicas.
