from lex import lexer, lex
from yacc import parser

def main():
  # filename = input("Insira o nome do arquivo desejado para abrir, caso deseje testar deixe vazio\n")
  filename = "sample.txt"
  if (len(filename) > 0):
    file = ''
    with open(filename, 'r')as dataFile:
      file = dataFile.read()

  # lex(file)
  result = parser.parse(lexer=lexer, input=file)
  print(result)

if __name__ == "__main__":
  main()
