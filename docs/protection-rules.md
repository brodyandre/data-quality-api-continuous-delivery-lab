# Protection Rules

Este documento resume uma configuracao simples e profissional para demonstrar governanca no fluxo de entrega continua.

## GitHub Environments

| Environment | Sugestao de regra |
| --- | --- |
| `development` | sem aprovacao manual |
| `staging` | pelo menos 1 aprovador |
| `production` | aprovacao manual obrigatoria e acesso restrito |

## Branch protection

Sugestoes para a branch `main`:

- exigir status checks do workflow `CI`
- bloquear merge com checks pendentes ou falhos
- exigir branch atualizada antes do merge, se fizer sentido para a demonstracao
- limitar bypass de regras a mantenedores do repositorio

## Producao

Para reforcar a narrativa do laboratorio:

- configure reviewers obrigatorios em `production`
- use `production` como ultima etapa da promocao
- deixe claro que a aprovacao existe para representar controle, nao deploy real em cloud

## Objetivo dessas regras

O valor dessas configuracoes esta em demonstrar:

- separacao entre ambientes
- gates de aprovacao
- protecao de producao
- boas praticas de governanca em pipelines de CI/CD
