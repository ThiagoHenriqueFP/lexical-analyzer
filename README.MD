# Analisador léxico
### Discentes
* Thiago Henrique 
* Wender Enzo

## Referências
### Slides
* Slide 8 Tabela de simbolos
* Slide 12 Expressões regulares
* Slide 13 Reconhecimento de tokens
### Documentação
* Documentação do PLY - https://ply.readthedocs.io/en/latest/ply.html#lex
### Ferramentas de ajuda
* Regex101 - https://regex101.com/
## Como rodar
### Requisitos
* python 3
* pip
### Instruções
* Primeiro precisa instalar todas as dependências dentro do requeriments.txt com o comando ```pip install -r requeriments.txt ```
* Segundo rodar o programa com o comando ```python lex.py```
## Explicação da implementação
Inicialmente o programa vai pedir um **ARQUIVO TEXTO(TXT)** para ler e executar, caso seja enviado em branco, o programa ira usar o teste já preconfigurado no projeto.

À nível de código, a implementação inicia importando as funções do ply e definindo quais são as palavras reservadas e os tokens para cadastrar.

Depois vem as funções que irão testar cada palavra e irá tonkenizar e registrar na tabela de simbolos. **Importante**, a ordem é extremamente relvante para a implementação, pois caso seja marcada como algum token, ele somente será esse token, então se a ordem de "precedência" do tipo não for bem definida terá falsos tokens.