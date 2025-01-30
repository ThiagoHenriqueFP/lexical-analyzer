# Compilador OWL - Manchester Syntax
### Discentes
* Thiago Henrique 
* Wender Enzo

## Clonando o repositório
* copie o link ssh ou https e rode o comando ```git clone <link>```
* entre no diretório lexical-analyzer
OU
* baixe o zip e extraia para o local desejado
* entre no diretório lexical-analyzer

## Referências
### Documentação
* Documentação do PLY - https://ply.readthedocs.io/en/latest/ply.html#lex
### Ferramentas de ajuda
* Regex101 - https://regex101.com/
## Como rodar
### Requisitos
* python 3 instalado
* pip instalado
### Instruções
* Primeiro precisa instalar todas as dependências dentro do requeriments.txt rodando o comando ```pip install -r requeriments.txt ``` no terminal
* Segundo rodar o programa com o comando ```python lex.py``` no terminal
## Explicação da implementação
### Analisador2 léxica
Inicialmente o programa vai pedir um **ARQUIVO TEXTO(TXT)** para ler e executar, caso seja enviado em branco, o programa ira usar o teste já preconfigurado no projeto.

À nível de código, a implementação inicia importando as funções do ply e definindo quais são as palavras reservadas e os tokens para cadastrar.

Depois vem as funções que irão testar cada palavra e irá tonkenizar e registrar na tabela de simbolos. **Importante**, a ordem é extremamente relvante para a implementação, pois caso seja marcada como algum token, ele somente será esse token, então se a ordem de "precedência" do tipo não for bem definida terá falsos tokens.

