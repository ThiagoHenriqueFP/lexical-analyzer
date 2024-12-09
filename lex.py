# ----------------- Specs -----------------
# owl2lex.py
# Especificar um analisador léxico para a linguagem OWL2 no formato Manchester Syntax, considerando as seguintes especificações:
# Palavras reservadas:
# ● SOME, ALL, VALUE, MIN, MAX, EXACTLY, THAT
# ● NOT
# ● AND
# ● OR
# ● Class, EquivalentTo, Individuals, SubClassOf, DisjointClasses (todos sucedidos por “:”, que indicam tipos na linguagem OWL)
# 
# Identificadores de classes:
# ● Nomes começando com letra maiúscula, p.ex.: Pizza.
# ● Nomes compostos concatenados e com iniciais maiúsculas, p.ex.: VegetarianPizza.
# ● Nomes compostos separados por underline, p.ex.: Margherita_Pizza.
# 
# Identificadores de propriedades:
# ● Começando com “has”, seguidos de uma string simples ou composta, p.ex.: hasSpiciness, hasTopping, hasBase.
# ● Começando com “is”, seguidos de qualquer coisa, e terminados com “Of”, p.ex.: isBaseOf, isToppingOf.
# ● Nomes de propriedades geralmente começam com letra minúscula e são seguidos por qualquer outra sequência de letras, p.ex: ssn, hasPhone, numberOfPizzasPurchased.
# 
# Símbolos especiais:
# ● Exemplos: [, ], {, }, (, ), >, <, e “,”
# 
# Nomes de indivíduos:
# ● Começando com uma letra maiúscula, seguida de qualquer combinação de letras minúsculas e
# terminando com um número. Por exemplo: Customer1, Waiter2, AmericanHotPizza1, etc.
# 
# Tipos de dados:
# ● Identificação de tipos nativos das linguagens OWL, RDF, RDFs ou XML Schema, por exemplo: owl:
# real, rdfs: domain, ou xsd: string.
# 
# Cardinalidades:
# ● Representadas por números inteiros, p.ex.: hasTopping min 3
# /---------------- Specs ----------------/

import ply.lex as lex

reserved = {
  'some':'some',
  'all':'all',
  'value':'value',
  'min':'min',
  'max':'max',
  'exactly':'exactly',
  'that':'that',
  'and':'and',
  'not':'not',
  'or':'or',
  'Class:': 'CLASS',
  'EquivalentTo:': 'EQUIVALENTO',
  'SubClassOf:': 'SUBCLASSOF',
  'DisjointClasses:': 'DISJOINTCLASSES'
}

tokens = [
  'ID',
  'NUM',
  'TYPE',
  'SPECIAL',
  'PROPERTY',
  'INDIVIDUAL',
 ] + list(reserved.values())

t_ignore = ' \t'

def t_COMMENT(t):
  r'\#.*'
  pass

def t_newline(t):
  r'\n+'
  # ler nova linha e conta mais um ao número de linhas
  t.lexer.lineno += len(t.value)

def t_TYPE(t):
    r'owl:real|rdfs:domain|xsd:string|xsd:integer'
    return t

def t_NUM(t):
  r'\d+'
  t.valeu = int(t.value)
  return t

def t_SPECIAL(t):
    r'\[|\]|\{|\}|\(|\)|>|<|,'
    return t

def t_INDIVIDUAL(t):
   r'[A-Z][A-Za-z]+[0-9]+'
   return t

def t_PROPERTY(t):
  r'(has[a-zA-Z]+)|(is.+Of)|([a-z]+[A-Z][a-zA-Z]+)'
  if t.value.upper() in reserved:
    t.type = reserved[t.value.upper() ]
  return t

def t_ID(t):
  r'([A-Z][a-zA-z]+:)|([A-Z][a-zA-Z]+_[A-Z][a-zA-Z]+)|([A-Z][a-zA-Z]+([A-Z][a-z]+)?)|([a-z]+)'

  if t.value.upper() in reserved:
    t.type = reserved[t.value.upper()]
  else:
    t.type = reserved.get(t.value, 'ID')

  return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = '''
Class: Customer
EquivalentTo:
Person
and (purchasedPizza some Pizza)
and (hasPhone some xsd:string)
Individuals:
Customer1,
Customer10,
Customer2,
Customer3,
Customer4,
Customer5,
Customer6,
Customer7,
Customer8,
Customer9
Class: Employee
SubClassOf:
Person
and (ssn min 1 xsd:string)
Individuals:
Chef1,
Manager1,
Waiter1,
Waiter2
Class: Pizza
SubClassOf:
hasBase some PizzaBase,
hasCaloricContent some xsd:integer
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Individuals:
CustomPizza1,
CustomPizza2
Class: CheesyPizza
EquivalentTo:
Pizza
and (hasTopping some CheeseTopping)
Individuals:
CheesyPizza1
Class: HighCaloriePizza
EquivalentTo:
Pizza
and (hasCaloricContent some xsd:integer [>= 400])
Class: InterestingPizza
EquivalentTo:
Pizza
and (hasTopping min 3 PizzaTopping)
Class: LowCaloriePizza
EquivalentTo:
Pizza
and (hasCaloricContent some xsd:integer [< 400])
Class: NamedPizza
SubClassOf:
Pizza
Class: AmericanaHotPizza
SubClassOf:
NamedPizza,
hasTopping some JalapenoPepperTopping,
hasTopping some MozzarellaTopping,
hasTopping some PepperoniTopping,
hasTopping some TomatoTopping
DisjointClasses:
AmericanaPizza, MargheritaPizza, SohoPizza
Individuals:
AmericanaHotPizza1,
AmericanaHotPizza2,
AmericanaHotPizza3,
ChicagoAmericanaHotPizza1
Class: AmericanaPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some PepperoniTopping,
hasTopping some TomatoTopping
DisjointClasses:
AmericanaHotPizza, MargheritaPizza, SohoPizza
Individuals:
AmericanaPizza1,
AmericanaPizza2
Class: MargheritaPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some TomatoTopping,
hasTopping only
(MozzarellaTopping or TomatoTopping)
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, SohoPizza
Individuals:
MargheritaPizza1,
MargheritaPizza2
Class: SohoPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some OliveTopping,
hasTopping some ParmesanTopping,
hasTopping some TomatoTopping,
hasTopping only
(MozzarellaTopping or OliveTopping or ParmesanTopping or TomatoTopping)
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, MargheritaPizza
Individuals:
SohoPizza1,
SohoPizza2
Class: SpicyPizza
EquivalentTo:
Pizza
and (hasTopping some (hasSpiciness value Hot1))
Class: VegetarianPizza
EquivalentTo:
Pizza
and (hasTopping only
(CheeseTopping or VegetableTopping))
Class: PizzaBase
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Class: PizzaTopping
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Class: Spiciness
EquivalentTo:
{Hot1 , Medium1 , Mild1}
'''
fileName = input("Insira o nome do arquivo desejado para abrir, caso deseje testar deixe vazio\n")

if (len(fileName) > 0):
  file = ''
  with open(fileName, 'r')as dataFile:
    file = dataFile.read()
  lexer.input(file)

  while True:
    tok = lexer.token()
    if not tok:
      break
    print(tok)
else:
  lexer.input(data)

  while True:
    tok = lexer.token()
    if not tok:
      break
    print(tok)