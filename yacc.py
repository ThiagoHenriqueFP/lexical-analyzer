import ply.yacc as yacc
import re
from lex import tokens

errors = []
warnings = []
class_type = []
class_modifiers = []
closure_axiom_tuple = []

def clear():
    errors.clear()
    warnings.clear()
    class_type.clear()
    class_modifiers.clear()
    closure_axiom_tuple.clear()

def print_class(current):
    is_success = "was successfuly analysed" if len(errors) == 0 else "has errors encoutntered after analyse"
    class_type_str = ''
    for ct in class_type:
        class_type_str += f"{ct} "
    print(f"Class: {current} {class_type_str}{is_success}")
    for cm in class_modifiers:
        print("\t",cm)
    if len(errors) > 0:
        print("ERRORS")
        for e in errors:
            print('\033[91m'+"X ", e)

    if len(warnings) > 0:
        print("WARNINGS")
        for e in warnings:
            print('\033[93m',"! ", e)
    print('\033[0m', '----------------------\n')
    clear()

# Regras da gramática
def p_ontology(p):
    'ontology : class_decl_list'

def p_class_decl_list(p):
    '''class_decl_list : class_decl
                       | class_decl_list class_decl'''
    
def p_class_decl(p):
    'class_decl : CLASS ID class_body'
    print_class(p[2])

def p_class_body(p):
    '''class_body   : primitive_class
                    | defined_class
                    | error_classes
                    | empty
    '''

def p_error_classes(p):
    '''error_classes    : only_disjoint
                        | only_individuals
                        | out_of_order
                        | missing_directives
    '''

def p_missing_directives(p):
    '''missing_directives   : subclass_properties
                            | equivalent_properties
    '''

    errors.append("cannot instance a class without SubClassOf or EquivalentTo directives")

def p_only_disjoint(p):
    '''only_disjoint    : disjoint_clause'''
    errors.append("A class cannot be declared only with a disjoint clause")

def p_only_individuals(p):
    '''only_individuals : individuals_clause'''
    errors.append("A class cannot be declared only with a individuals list")

def p_out_of_order(p):
    '''out_of_order : subclassof_clause equivalento_clause
                    | subclassof_clause equivalento_clause disjoint_clause
                    | subclassof_clause equivalento_clause disjoint_clause individuals_clause
                    | subclassof_clause equivalento_clause individuals_clause
    '''
    errors.append("Class defined out of the order")

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

def p_primitive_class(p):
    '''primitive_class  : subclassof_clause
                        | subclassof_clause disjoint_clause
                        | subclassof_clause disjoint_clause individuals_clause
                        | subclassof_clause individuals_clause
    '''
    class_type.insert(0, f"declarated as primitive class")

def p_defined_class(p):
    '''defined_class    : equivalento_clause
                        | equivalento_clause individuals_clause
                        | equivalento_clause disjoint_clause 
                        | equivalento_clause disjoint_clause individuals_clause
                        | equivalento_clause subclassof_clause individuals_clause
                        | equivalento_clause subclassof_clause disjoint_clause 
                        | equivalento_clause subclassof_clause disjoint_clause individuals_clause
    '''
    class_type.insert(0, "declarated as defined class")

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
    '''type_with_num_stt    : PROPERTY some TYPE
                            | PROPERTY some TYPE bl SPECIAL NUM br
                            | PROPERTY some TYPE bl NUM br
    '''
    if len(p) == 8:
        class_modifiers.append(f"Property '{p[1]}' with type {p[3]} {p[4]}{p[5]} {p[6]}{p[7]} [Data Property]")
    elif len(p) == 6:
        class_modifiers.append(f"Property '{p[1]}' with type {p[3]} {p[4]}{p[6]}{p[7]} [Data Property]")
    else: 
        class_modifiers.append(f"Property '{p[1]}' with type {p[3]} [Data Property]")
        if p[3] == 'xsd:integer':
            warnings.append("if a integer range is not provided, it will be assumed as (+-)infinit")

def p_subclass_properties(p):
    '''subclass_properties  : PROPERTY some ID
                            | type_with_num_stt
                            | type_with_num_stt SPECIAL subclass_properties
                            | PROPERTY some ID SPECIAL subclass_properties
                            | PROPERTY only subclass_properties_wrapped
                            | ID and SPECIAL expression SPECIAL
                            | ID SPECIAL closure_axiom
                            | ID
                            '''
    if 'flag' in closure_axiom_tuple:
        if len(closure_axiom_tuple) > 1:
            errors.append(f"These IDs arent declared as properties in the closure axiom: {closure_axiom_tuple}")
        else :
            class_modifiers.append("Class with closure axiom successfuly defined")
    
def p_closure_axiom(p):
    '''closure_axiom    : PROPERTY some ID SPECIAL closure_axiom
                        | PROPERTY some ID SPECIAL
                        | PROPERTY only SPECIAL closure_axiom_check SPECIAL
    '''
    if p[2] == 'only':
        closure_axiom_tuple.append('flag')
    else:
        class_modifiers.append(f"{p[1]} is a Object Property with id: {p[3]}")
    if p[3] != '(' and 'flag' in closure_axiom_tuple:
        if p[3] in closure_axiom_tuple:
            closure_axiom_tuple.remove(p[3])
        else: 
            errors.append(f"ID: {p[3]} not declared as the property, but declared in the closure")
            

def p_closure_axiom_check(p):
    '''closure_axiom_check  : ID 
                            | ID or closure_axiom_check
    '''

    closure_axiom_tuple.insert(0, p[1])

def p_subclass_properties_wrapped(p):
    '''subclass_properties_wrapped  : SPECIAL mult_or_id SPECIAL'''

def p_cardinal_expression(p):
    '''cardinal_expression  : PROPERTY min NUM ID
                            | PROPERTY max NUM ID
                            | PROPERTY max NUM TYPE
                            | PROPERTY min NUM TYPE
                            | PROPERTY exactly NUM ID
                            | PROPERTY exactly NUM TYPE
    '''

def p_mult_or_id(p):
    '''mult_or_id   : ID or mult_or_id
                    | ID
    '''

def p_mult_and_equi(p):
    '''mult_and_equi    : and SPECIAL PROPERTY some ID SPECIAL mult_and_equi
                        | and SPECIAL type_with_num_stt SPECIAL mult_and_equi
                        | and SPECIAL type_with_num_stt SPECIAL
                        | and SPECIAL PROPERTY some ID SPECIAL
    '''

def p_equivalent_properties(p):
    '''equivalent_properties    : enumerated_class
                                | covered_class
                                | ID mult_and_equi
                                | ID and SPECIAL expression SPECIAL
    '''

# def p_mult_properties(p):
#     '''mult_properties  : and SPECIAL expression SPECIAL mult_properties
#                         | and SPECIAL expression SPECIAL
#     '''

def p_enumerated_class(p):
    '''enumerated_class : equivalent_list'''
    class_type.insert(0,"and enumerated")

def p_covered_class(p):
    '''covered_class    : mult_or_id'''
    class_type.insert(0,"and covered")

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
