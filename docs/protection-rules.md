# Protection Rules

Sugestao de configuracao para os ambientes do GitHub:

- `development`: sem aprovacao manual, para demonstracoes rapidas.
- `staging`: exigir pelo menos 1 aprovador.
- `production`: exigir aprovacao manual, limitar deploy a mantenedores e proteger a branch `main`.

## Regras recomendadas

- Ativar branch protection na `main`.
- Exigir status checks do workflow `CI`.
- Configurar GitHub Environments com o mesmo nome dos jobs: `development`, `staging` e `production`.
- Em `production`, habilitar reviewers obrigatorios.

Essas protecoes deixam o fluxo simples, mas ja mostram controles reais de promocao.
