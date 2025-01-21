import ply.yacc as yacc
from lex import tokens

closure_axiom_tuple = []
current_class = '?'

# Regras da gramática
def p_ontology(p):
    'ontology : class_decl_list'

def p_class_decl_list(p):
    '''class_decl_list : class_decl
                       | class_decl_list class_decl'''

def p_class_decl(p):
    'class_decl : CLASS ID class_body'
    current_class = p[2]

def p_class_body(p):
    '''class_body   : primitive_class
                    | defined_class
                    | error_classes
                    | empty
    '''

def p_error_classes(p):
    '''error_classes    : only_disjoint'''

def p_only_disjoint(p):
    '''only_disjoint    : disjoint_clause'''
    print("A class cannot be declared only with a disjoint clause")
    raise SyntaxError


def p_subclassof_clause(p):
    'subclassof_clause : SUBCLASSOF subclass_properties'

def p_equivalento_clause(p):
    'equivalento_clause : EQUIVALENTO equivalent_properties'

def p_disjoint_clause(p):
    'disjoint_clause : DISJOINTCLASSES id_list'

def p_individuals_clause(p):
    'individuals_clause : STARTINDIVIDUALS individual_list'

def p_individual_list(p):
    '''individual_list  : INDIVIDUAL
                        | INDIVIDUAL SPECIAL individual_list'''
    pass

def p_primitive_class(p):
    '''primitive_class  : subclassof_clause
                        | subclassof_clause disjoint_clause
                        | subclassof_clause disjoint_clause individuals_clause
                        | subclassof_clause individuals_clause
    '''
    print(f"Classe primitiva declarada")

def p_defined_class(p):
    '''defined_class    : equivalento_clause
                        | equivalento_clause individuals_clause
    '''
    print("Classe definida declarada")

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
                    | PROPERTY some wrapped_expression
                    | PROPERTY or TYPE
                    | PROPERTY value TYPE
                    | cardinal_expression
                    | mult_or_id
                    | type_with_num_stt'''    
    pass

def p_type_with_num_stt(p):
    '''type_with_num_stt    : PROPERTY some TYPE SPECIAL SPECIAL NUM SPECIAL
                            | PROPERTY some TYPE SPECIAL SPECIAL SPECIAL NUM SPECIAL
    '''
    if len(p) == 8:
         print(f"Property '{p[1]}' with type {p[3]} {p[4]} {p[5]}{p[6]} {p[7]}")
    else: print(f"Property '{p[1]}' with type {p[3]} {p[4]} {p[5]}{p[6]}{p[7]} {p[8]}")
def p_subclass_properties(p):
    '''subclass_properties  : PROPERTY some ID
                            | PROPERTY some TYPE
                            | PROPERTY some ID SPECIAL subclass_properties
                            | PROPERTY some TYPE SPECIAL subclass_properties
                            | PROPERTY only subclass_properties_wrapped
                            | ID and SPECIAL expression SPECIAL
                            | ID SPECIAL closure_axiom
                            | ID
                            '''
    if len(closure_axiom_tuple) != 0:
        print(f"These IDs arent declared as properties in the closure axiom: {closure_axiom_tuple}")
        raise SyntaxError
    print("Class with closure axiom successfuly defined")
    
def p_closure_axiom(p):
    '''closure_axiom    : PROPERTY some ID SPECIAL closure_axiom
                        | PROPERTY some ID SPECIAL
                        | PROPERTY only SPECIAL closure_axiom_check SPECIAL
    '''
    if p[3] != '(':
        if p[3] in closure_axiom_tuple:
            closure_axiom_tuple.remove(p[3])
        else: 
            print(f"ID: {p[3]} not declared as the property, but declared in the closure")
            raise SyntaxError

def p_closure_axiom_check(p):
    '''closure_axiom_check  : ID 
                            | ID or closure_axiom_check
    '''

    closure_axiom_tuple.insert(0, p[1])

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
    '''equivalent_properties    : enumerated_class
                                | covered_class
                                | ID and SPECIAL equi_excludent_props SPECIAL
                                | ID mult_and_equi
                                | ID and SPECIAL expression SPECIAL
    '''

def p_enumerated_class(p):
    '''enumerated_class : equivalent_list'''
    print("Enumerated class defined")

def p_covered_class(p):
    '''covered_class    : mult_or_id'''
    print("Covered class defined")

def p_equi_excludent_props(p):
    '''equi_excludent_props : PROPERTY only SPECIAL mult_or_id SPECIAL'''

def p_equivalent_list(p):
    '''equivalent_list  : cl equivalent_list cr
                        | INDIVIDUAL SPECIAL equivalent_list
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
        print(f"Erro de sintaxe na linha: {p.lineno}: {p.value}")
    else:
        print("Erro de sintaxe: EOF inesperado")

parser = yacc.yacc()
