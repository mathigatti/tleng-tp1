import lexer_rules

import parser_rules
from sys import argv, exit 
from ply.lex import lex        
from ply.yacc import yacc      



if __name__ == "__main__":
    if len(argv) != 2:
        print "Parametros invalidos."
        print "Uso:"
        print "SLSParser archivo_entrada"
        exit()

    src = open(argv[1], "r")

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    try:
        parser.parse(src.read(),lexer)       
    except parser_rules.ParserException as exception:
            print "Semantic error: " + str(exception)
    else:
            print "Syntax is valid."
