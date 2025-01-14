from lex import lexer
from yacc import parser

def main():
  filename = input("Insira o nome do arquivo desejado para abrir, caso deseje testar deixe vazio\n")
  if (len(filename) > 0):
    file = ''
    with open(filename, 'r')as dataFile:
      file = dataFile.read()

  lexer(file)
  result = parser.parse(lexer=lexer, input=file)
  print(result)

if __name__ == "__main":
  main()
