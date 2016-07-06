# Si el codigo esta vacio o solo tiene espacios, saltos de linea y demas caracteres no imprimibles entonces no es valido

#
reserved = {
	'do':'DO',
	'while':'WHILE',
	'for':'FOR',
	'if':'IF',
	'then':'THEN',
	'else':'ELSE',
	'res':'RES',
	'return':'RETURN',
	'begin':'BEGIN',
	'end':'END',
	'capitalizar':'CAPITALIZAR',
	'length':'LENGTH',
	'print':'PRINT',
	'multiplicacionEscalar':'MULTIPLICACIONESCALAR',
	'colineales':'COLINEALES',
	'and':'AND',
	'or':'OR',
	'not':'NOT',

}

tokens = [
# Numeros
   'NUMBER',
   'PLUS',
   'TIMES',
   'MINUS',
   'ELEVADO',
   'MODULO',
   'DIV',
   'IGUAL',   
   'DISTINTO',
   'MAYOR',
   'MENOR',
# +=, -=, /=, *=, ++, --
   'AGREGAR',
   'SACAR',
   'DIVIDI',
   'MULTIPL',
   'MASMAS',
   'LESSLESS',
# Booleanos
	'BOOL',

#
   'INTERROGACION',
   'PUNTO',
   'DOSPUNTOS',
   'PUNTOYCOMA',
   'COMA',
   'COMENTARIO',
   'LLAVEDER',
   'LLAVEIZQ',
   'LPAREN',
   'RPAREN',
   'RCORCHETE',
   'LCORCHETE',
#
   'VARIABLE',
   'CADENA',

# Estos actualmente estan siendo ignorados, son tomados como tipo VARIABLE 
   'ASIGNACION',
] + list(reserved.values())

def t_NUMBER(token):
	r"(-?[0-9]+(\.[0-9][0-9]*)?)"
	return token

def t_NEWLINE(token):
  r"\n+"
  token.lexer.lineno += len(token.value)


t_IGUAL = r"=="
t_DISTINTO = r"\!="
t_AGREGAR = r"\+="
t_SACAR = r"-="
t_DIVIDI = r"/="
t_MULTIPL = r"\*="
t_MINUS = r"\-"
t_ELEVADO = r"\^"
t_MODULO = r"\%"
t_DIV = r"\/"
t_MASMAS = r"\+\+"
t_LESSLESS = r"--"
t_MAYOR = r">"
t_MENOR = r"<"
t_PLUS = r"\+"
t_TIMES = r"\*"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_RCORCHETE = r"\["
t_LCORCHETE = r"\]"
t_LLAVEIZQ = r"\{"
t_LLAVEDER = r"\}"
t_INTERROGACION = r"\?"
t_PUNTO = r"\."
t_DOSPUNTOS = r"\:"
t_PUNTOYCOMA = r"\;"
t_COMA = r"\,"
t_COMENTARIO = r"\#([a-z]|[A-Z]|\_|[ \t]|[0-9]|\=|\;|\,|\+|\*|\%|\#|\$|\/|\(|\)|\?|\{|\}|\-|\_|\'|\"|[|]|\.|\:|\<|\>|\|\!)*"


t_CADENA = r"\" ([a-z]|[A-Z]|\_|[ \t]|[0-9]|!)* \" "

def t_BOOL(token) : 
    r"true | false | FALSE | TRUE"
    return token

def t_VARIABLE(token):
	r"([a-z]|[A-Z]) ([a-z]|[A-Z]|\_|[0-9])*"
	token.type = reserved.get(token.value,'VARIABLE')
	return token

t_ASIGNACION = r"="

t_ignore = " \t"


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
