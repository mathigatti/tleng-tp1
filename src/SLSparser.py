import lexer_rules

import parser_rules
from sys import argv, exit 
from ply.lex import lex        
from ply.yacc import yacc      



if __name__ == "__main__":
    if len(argv) != 3:
        print "Parametros invalidos."
        print "Uso:"
        print "SLSparser.py archivo_entrada archivo_salida"
        exit()

    src = open(argv[1], "r")

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    try:
        text = src.read()
        src.close()

        lexer = lex(module=lexer_rules)
        parser = yacc(module=parser_rules)

        salida = parser.parse(text,lexer)

        output_file = open(argv[2], "w")
        output_file.write(salida)
        output_file.close()       
    except parser_rules.ParserException as exception:
            print "Semantic error: " + str(exception)
    else:
            print "Syntax is valid."


