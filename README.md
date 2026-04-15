# sistema-bancario-python
Projeto de sistema bancário desenvolvido como parte de um desafio da DIO.

O sistema funciona pelo terminal e permite:

- Depositar dinheiro
- Sacar dinheiro
- Ver extrato
- Criar usuários
- Criar contas bancárias

Além do que foi proposto no desafio, fiz algumas mudanças:

- Permiti que um cliente tenha mais de uma conta e possa escolher qual usar
- A data é salva como objeto datetime e formatada apenas na exibição do extrato
- Algumas melhorias de usabilidade: lista de contas numeradas e tratamento de erro ao escolher conta
- Correção de lógica no limite de saque (>= no lugar de >), que antes permitia mais saques do que o esperado
- Validação de entrada para valores numéricos no input

Conceitos utilizados:

Programação Orientada a Objetos
Herança
Classes abstratas (ABC)

Referência

Projeto baseado no desafio original da DIO:
https://github.com/digitalinnovationone/trilha-python-dio/blob/main/02%20-%20Programa%C3%A7%C3%A3o%20Orientada%20a%20Objetos/10%20-%20desafio/desafio_v2.py