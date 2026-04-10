# CONTRACT

## Core

- calcular_indice_saude_input_simples → {"score": float}

## API

POST /score
Input: receita, despesas, divida (float)
Output: score, classificacao, recomendacao

## Errors

- 422: validation
- 500: internal error
