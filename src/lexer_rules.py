# Si el codigo esta vacio o solo tiene espacios, saltos de linea y demas caracteres no imprimibles entonces no es valido

#

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
   'AND',
   'OR',
   'NOT',
   'BOOLEANO',
# Funciones
   'LENGTH',
   'PRINT',
   'CAPITALIZAR',
   'COLINEALES',
   'MULTIPLICACIONESCALAR',
#
   'INTERROGACION',
   'DOSPUNTOS',
   'PUNTOYCOMA',
   'COMA',
   'NUMERAL', #Esto hay que cambiarlo por comentario y que borre las lineas hasta el primer \n
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
   'IF',
   'ELSE',
   'FOR',
   'WHILE',
   'DO',
   'RES',
   'RETURN',
   'BEGIN',
   'ASIGNACION',
   'END'
]


def t_NUMBER(token):
	r"(-?[0-9]+(\.[0-9][0-9]*)?)"
	token.value = float(token.value)
	return token
# Falta agregarle decimales, Podra ser negativo?

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
t_DOSPUNTOS = r"\:"
t_PUNTOYCOMA = r"\;"
t_COMA = r"\,"
t_NUMERAL = r"\#"


t_BOOLEANO = r"(false|FALSE|true|TRUE)"
t_AND = r"(and|AND)"
t_OR = r"(or|OR)"
t_NOT = r"(NOT|not)"

t_LENGTH = r"length"
t_PRINT = r"print"
t_CAPITALIZAR = r"capitalizar"
t_COLINEALES = r"colineales"
t_MULTIPLICACIONESCALAR = r"multiplicacionEscalar"

t_CADENA = r"\" ([a-z]|[A-Z]|\_|[ \t]|[0-9]|!)* \" "
t_VARIABLE = r"([a-z]|[A-Z]) ([a-z]|[A-Z]|\_|[0-9])*"

"""
Deberian sacarse todos estos valores del conjunto que forma a VARIABLE:
((DO|do)|(while|WHILE)|(for|FOR)|(if|IF) |(else|ELSE) |(res|RES) | (return|RETURN) |(begin|BEGIN) | (end|END) | capitalizar |length | print | multiplicacionEscalar | colineales | (true|TRUE) | (false|FALSE) | (and|AND) | (or|OR) | (NOT|not) )"""

t_DO = r"(DO|do)"
t_WHILE = r"(while|WHILE)"
t_FOR = r"(for|FOR)"
t_IF = r"(if|IF)"
t_ELSE = r"(else|ELSE)"
t_RES = r"(res|RES)"
t_RETURN = r"(return|RETURN)"
t_BEGIN = r"(begin|BEGIN)"
t_END = r"(end|END)"
t_ASIGNACION = r"="

t_ignore = " \t"


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
