# tleng-tp
Primer Cuatrimestre 2016, Trabajo Práctico de Teoría de Lenguajes

----------------------------------

Para instalar ply en ubuntu:

	apt-get install python-ply

Los 3 ejemplos se corren ejecutando parser.py

	codigo_aritmetica, te hace la cuenta
		python parser.py 2+2
	codigo, te guarda el AST
		python parser.py archivo_entrada archivo_salida
	codigo_arreglos
		no entendi como se corre, me tira syntax error.

El codigo del tp esta en src. Solo esta hecho en parte el lexer, hay tambien un ejemplo para testearlo que se corre con:	
	python ./lexer.py ./test.txt ./salida

