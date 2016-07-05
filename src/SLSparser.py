# Para correr el parser hay tres opciones:
# SLSparser.py -o archivo_salida -c archivo_entrada
# SLRparser.py -o arvhico_salida 'texto de entrada escrito en el terminal directamente'
# SLRparser.py 'texto de entrada' <---- En este caso la salida se imprime en el terminal

import lexer_rules

import parser_rules
from sys import argv, exit 
from ply.lex import lex        
from ply.yacc import yacc      



if __name__ == "__main__":
    if len(argv) < 2:
        print "Parametros invalidos."
        print "Uso:"
        print "SLSparser.py archivo_entrada archivo_salida"
        exit()


    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    try:
		if argv[1] == '-o':
			output_file = open(argv[2], "w")
			if argv[3] == '-c':
				src = open(argv[4], "r")
				text = src.read()
				src.close()
			else:
				text = argv[3]
			salida = parser.parse(text,lexer)
			output_file.write(salida)
			output_file.close()       


		elif argv[1] == '-c':
			src = open(argv[2], "r")
			text = src.read()
			src.close()
			salida = parser.parse(text,lexer)
			print salida

		else:
			text = argv[1]
			salida = parser.parse(text,lexer)
			print salida

    except parser_rules.ParserException as exception:
            print "Semantic error: " + str(exception)
    else:
            print "Syntax is valid."


