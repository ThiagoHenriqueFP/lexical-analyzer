import ply.yacc as yacc
from lex import tokens

# Regras da gramática
def p_class_decl(p):
    'class_decl : CLASS IDENTIFIER class_body'
    print(f"Classe definida: {p[2]}")

def p_class_body(p):
    '''class_body : subclassof_clause
                  | empty'''
    pass

def p_subclassof_clause(p):
    'subclassof_clause : SUBCLASSOF list_of_properties'
    print("Subclasse definida")

def p_list_of_properties(p):
    '''list_of_properties : IDENTIFIER
                          | list_of_properties COMMA IDENTIFIER'''
    if len(p) == 2:
        print(f"Propriedade definida: {p[1]}")
        p[0] = [p[1]]
    else:
        print(f"Propriedade definida: {p[3]}")
        p[0] = p[1] + [p[3]]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: {p.value}")
    else:
        print("Erro de sintaxe: EOF inesperado")

# Inicializar o parser
parser = yacc.yacc()

