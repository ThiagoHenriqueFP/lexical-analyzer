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
    'class_decl : CLASS ID class_body'
    print(f"Classe definida: {p[2]}")

def p_class_body(p):
    '''class_body   : subclass_of_clause
                    | subclass_of_clause individuals_clause
                    | subclass_of_clause disjoint_classes_clause individuals_clause
                    | equivalent_to_clause
                    | equivalent_to_clause individuals_clause
                    | disjoint_classes_clause 
                    | disjoint_classes_clause individuals_clause
                    | empty'''
    pass

def p_subclass_of_clause(p):
    'subclass_of_clause : SUBCLASSOF subclass_properties'
    print("Subclasse definida")

def p_equivalent_to_clause(p):
    'equivalent_to_clause : EQUIVALENTO equivalent_properties'
    print("Classe equivalente definida")

def p_disjoint_classes_clause(p):
    'disjoint_classes_clause : DISJOINTCLASSES id_list'
    print("Classes disjuntas definidas")

def p_individuals_clause(p):
    'individuals_clause : STARTINDIVIDUALS individual_list'

def p_individual_list(p):
    '''individual_list  : INDIVIDUAL
                        | INDIVIDUAL SPECIAL individual_list'''
    print(f"Indivíduos definidos: {p[1]}")
    pass

def p_wrapped_expression(p):
    '''wrapped_expression   : SPECIAL expression SPECIAL
                            | SPECIAL expression SPECIAL and wrapped_expression
    '''
    pass

def p_expression(p):
    '''expression   : ID
                    | ID SPECIAL expression
                    | PROPERTY some ID
                    | PROPERTY or ID
                    | PROPERTY value ID
                    | PROPERTY value INDIVIDUAL
                    | PROPERTY some TYPE
                    | PROPERTY some wrapped_expression
                    | PROPERTY or TYPE
                    | PROPERTY value TYPE
                    | cardinal_expression
                    | mult_or_id
                    | type_with_num_stt'''    
    pass

def p_type_with_num_stt(p):
    '''type_with_num_stt    : PROPERTY some TYPE SPECIAL NUM SPECIAL
                            | PROPERTY some TYPE SPECIAL SPECIAL NUM SPECIAL
    '''
def p_subclass_properties(p):
    '''subclass_properties  : PROPERTY some ID
                            | PROPERTY some TYPE
                            | PROPERTY some ID SPECIAL subclass_properties
                            | PROPERTY some TYPE SPECIAL subclass_properties
                            | PROPERTY only subclass_properties_wrapped
                            | ID and SPECIAL expression SPECIAL
                            | ID SPECIAL subclass_properties
                            | ID
                            '''

def p_subclass_properties_wrapped(p):
    '''subclass_properties_wrapped  : SPECIAL mult_or_id SPECIAL'''

def p_cardinal_expression(p):
    '''cardinal_expression  : PROPERTY min NUM TYPE
                            | PROPERTY max NUM TYPE
                            | PROPERTY exactly NUM TYPE
                            | PROPERTY min NUM ID'''

def p_mult_or_id(p):
    '''mult_or_id   : ID or mult_or_id
                    | ID
    '''

def p_mult_and_equi(p):
    '''mult_and_equi    : and SPECIAL PROPERTY some ID SPECIAL mult_and_equi
                        | and SPECIAL PROPERTY some TYPE SPECIAL mult_and_equi
                        | and SPECIAL PROPERTY some TYPE SPECIAL
                        | and SPECIAL PROPERTY some ID SPECIAL
    '''

def p_equivalent_properties(p):
    '''equivalent_properties    : cl equivalent_list cr
                                | ID and SPECIAL equi_excludent_props SPECIAL
                                | ID mult_and_equi
                                | ID and SPECIAL expression SPECIAL
    '''

def p_equi_excludent_props(p):
    '''equi_excludent_props : PROPERTY only SPECIAL mult_or_id SPECIAL'''

def p_equivalent_list(p):
    '''equivalent_list  : INDIVIDUAL SPECIAL equivalent_list
                        | INDIVIDUAL
    '''

def p_id_list(p):
    '''id_list : ID
               | ID SPECIAL id_list'''
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
