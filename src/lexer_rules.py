
#
reserved = {
	'do':'DO',
	'while':'WHILE',
	'for':'FOR',
	'if':'IF',
	'else':'ELSE',
	'res':'RES',
	'true':'TRUE',
	'false':'FALSE',
	'return':'RETURN',
	'begin':'BEGIN',
	'end':'END',
	'capitalizar':'CAPITALIZAR',
	'length':'LENGTH',
	'print':'PRINT',
	'multiplicacionescalar':'MULTIPLICACIONESCALAR',
	'colineales':'COLINEALES',
	'and':'AND',
	'or':'OR',
	'not':'NOT',

}

notokens = {
	'begin':'BEGIN',
	'end':'END',
	'true':'TRUE',
	'false':'FALSE',
	'return':'RETURN',
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

   'ASIGNACION',
] + [valor for valor in list(reserved.values()) if valor not in list(notokens.values())]

def t_NUMBER(token):
	r"([0-9]+(\.[0-9][0-9]*)?)"
	return token

def t_NEWLINE(token):
  r"\n+"
  token.lexer.lineno += len(token.value)

def t_IGUAL(token):
    r"=(\n)*="
    token.value = '=='
    return token


def t_DISTINTO(token):
    r"\!(\n)*="
    token.value = '!='
    return token;

def t_AGREGAR(token):
    r"\+(\n)*="
    token.value = '+='
    return token;

def t_SACAR(token):
    r"\-(\n)*="
    token.value = '-='
    return token

def t_DIVIDI(token):
    r"/(\n)*="
    token.value = '/='
    return token;

def t_MULTIPL(token):
    r"\*(\n)*="
    token.value = '*='
    return token;

def t_MASMAS(token):
    r"\+(\n)*\+"
    token.value = '++'
    return token

def t_LESSLESS(token):
    r"-(\n)*-"
    token.value = '--'
    return token

t_MINUS = r"\-"
t_ELEVADO = r"\^"
t_MODULO = r"\%"
t_DIV = r"\/"
t_MAYOR = r">"
t_MENOR = r"<"
t_PLUS = r"\+"
t_TIMES = r"\*"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LCORCHETE = r"\["
t_RCORCHETE = r"\]"
t_LLAVEIZQ = r"\{"
t_LLAVEDER = r"\}"
t_INTERROGACION = r"\?"
t_PUNTO = r"\."
t_DOSPUNTOS = r"\:"
t_PUNTOYCOMA = r"\;"
t_COMA = r"\,"
t_COMENTARIO = r"\#.*"


t_CADENA = r"\" .*? \" "

def t_BOOL(token) : 
    r"true | false | FALSE | TRUE"
    return token

def t_VARIABLE(token):
  r"([a-z]|[A-Z]) ([a-z]|[A-Z]|\_|[0-9])*"
  token.type = reserved.get(token.value.lower(),'VARIABLE')
  if token.type in notokens.values():
  	raise Exception('Su codigo contiene palabras reservadas')
  else:	
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
