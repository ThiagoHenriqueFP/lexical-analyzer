import ply.lex as lex

reserved = {
  'SOME':'some',
  'ALL':'all',
  'VALUE':'value',
  'MIN':'min',
  'MAX':'max',
  'EXACTLY':'exactly',
  'THAT':'that',
  'AND':'and',
  'NOT':'not',
  'OR':'or',
  'ONLY': 'only',
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

# def t_IDENTIFIER(t):
#     r'[a-zA-Z_][a-zA-Z0-9_]*'
#     return t

# def t_COMMA(t):
#     r','
#     return t


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
  r'(has[a-zA-Z]+)|(is.+Of)|([a-z]+[A-Z][a-zA-Z]+)|([a-z]+[a-z])'
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
hasTopping some MozzarellPersonaTopping,
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
def lex(file) :
  with open("lex.lex", 'w') as out:
    out.write('')
    out.close()

  lexer.input(file)
  while True:
    tok = lexer.token()
    if not tok:
      break
    print(tok)
    with open("lex.lex", 'a') as out:
      out.writelines(str(tok) + '\n')
      out.close()