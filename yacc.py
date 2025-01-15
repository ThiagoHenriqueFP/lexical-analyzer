import ply.yacc as yacc
from lex import tokens

# Regras da gramática
def p_ontology(p):
    'ontology : class_decl_list'
    print("Ontologia analisada com sucesso")

def p_class_decl_list(p):
    '''class_decl_list : class_decl
                       | class_decl_list class_decl'''
    pass

def p_class_decl(p):
    'class_decl : CLASS IDENTIFIER class_body'
    print(f"Classe definida: {p[2]}")

def p_class_body(p):
    '''class_body : subclass_of_clause
                  | equivalent_to_clause
                  | disjoint_classes_clause
                  | individuals_clause
                  | empty'''
    pass

def p_subclass_of_clause(p):
    'subclass_of_clause : SUBCLASSOF expressions'
    print("Subclasse definida")

def p_equivalent_to_clause(p):
    'equivalent_to_clause : EQUIVALENTO expressions'
    print("Classe equivalente definida")

def p_disjoint_classes_clause(p):
    'disjoint_classes_clause : DISJOINTCLASSES identifier_list'
    print("Classes disjuntas definidas")

def p_individuals_clause(p):
    'individuals_clause : INDIVIDUAL identifier_list'
    print(f"Indivíduos definidos: {p[2]}")
    p[0] = p[2]

def p_expressions(p):
    '''expressions : expression
                   | expressions and expression'''
    pass

def p_expression(p):
    '''expression : IDENTIFIER
                  | IDENTIFIER some IDENTIFIER
                  | IDENTIFIER or IDENTIFIER
                  | IDENTIFIER value IDENTIFIER'''
    pass


def p_identifier_list(p):
    '''identifier_list : IDENTIFIER
                       | IDENTIFIER COMMA identifier_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: {p.value}")
    else:
        print("Erro de sintaxe: EOF inesperado")

parser = yacc.yacc()
