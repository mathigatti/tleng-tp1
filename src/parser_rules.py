from lexer_rules import tokens
import ply.yacc as yacc


# Diccionario donde se almacenaran las variables declaradas junto con su tipo
variables_dict = dict()

# Funcion que reemplaza los '\n' por '\n    ' o sea agrega un tab en cada salto de linea
def find_and_replace(palabra):
    j = 0
    res = ''
    for i in xrange(len(palabra)):
        if palabra[i] == '\n':
            res = res + palabra[j:i] + '\n    '
            j = i+1
    return res + palabra[j:]

# Funcion que devuelve lo que esta despues de un guion bajo en un string, por ejemplo si palabra = NUMBER_INT devuelve INT
def tipo(palabra):
	j = len(palabra)
	for i in xrange(len(palabra)):
		if palabra[i] == '_':
			j = i + 1
			break
	if j == len(palabra):
		return 'SINTIPO'
	return palabra[j:len(palabra)]

# Funcion que devuelve NUMBER_FLOAT o NUMBER_INT segun si en su entrada tiene algun FLOAT o no
def tipoNumber(*args):
	if len(args) == 2:
		palabra1 = args[0]
		palabra2 = args[1]
		if type(palabra1) == type(1.0) or type(palabra2) == type(1.0):
			return 'NUMBER_FLOAT'
		else: return 'NUMBER_INT'
	else: 
		palabra1 = args[0]
		if type(palabra1) == type(1.0):
			return 'NUMBER_FLOAT'
		else: return 'NUMBER_INT'

# Funcion que devuelve True si tiene como prefijo a NUMBER
def esNumber(palabra):
	return len(palabra) >= 6 and palabra[0:6] == 'NUMBER'

# Funcion que accede al diccionario de variables y devuelve su tipo (Si esta definida)
# Si no esta definida devuelve ND
def estaDefinida(key):
	if key in variables_dict:
		return variables_dict[key]
	else: return 'ND'

# hay diferencia entre arreglo y vector o deberian ser lo mismo?
# ?????????????????????????????????

# Funcion que devuelve True si tiene como prefijo a VECTOR
def esVector(palabra):
	return len(palabra) >= 6 and palabra[0:6] == 'VECTOR'

# Funcion que devuelve True si tiene como prefijo a ARREGLO
def esArreglo(palabra):
	return len(palabra) >= 7 and palabra[0:7] == 'ARREGLO'
# ???????????????????????????


# Funcion que convierte a str su entrada en caso que sea un int
def toStrIfInt(var):
    if isinstance( var, int ):
       return str(var)
    else:
       return var

class ParserException(Exception):
        pass

#Producciones Generales

def p_programa_s_pp(p):
    'p : sentencia pp'
    p[0] = [p[1][0] + '\n'  + p[2][0], ' COMPLETAR ']

def p_programa_coment_pp(p):
    'p : COMENTARIO p'
    p[0] = [p[1] + '\n'  + p[2][0], ' COMPLETAR ']

def p_programa_ctl_p(p):
    'p : control pp'
    p[0] = [p[1][0] + '\n'  + p[2][0], ' COMPLETAR ']

def p_pp_s_pp(p):
    'pp : sentencia pp'
    p[0] = [p[1][0] + '\n'  + p[2][0], ' COMPLETAR ']

def p_pp_ctl_pp(p):
    'pp : COMENTARIO pp'
    p[0] = [p[1] + '\n'  + p[2][0], ' COMPLETAR ']

def p_pp_comentario_p(p):
    'pp : control pp'
    p[0] = [p[1][0] + '\n'  + p[2][0], ' COMPLETAR ']

def p_pp_empty(p):
    'pp : empty'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_empty(p):
    'empty :'
    p[0] = ['', ' COMPLETAR ']
     
def p_sentencia_var_asig(p):
    'sentencia : var_asig PUNTOYCOMA'
    p[0] = [p[1][0] + ';', ' COMPLETAR ']


def p_sentencia_func(p):
    'sentencia : funcion PUNTOYCOMA'
    p[0] = [p[1][0] + ';', ' COMPLETAR ']

#Producciones para estructuras de control
def p_control_ifelse(p):
    'control : ifelse'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_control_loop(p):
    'control : loop'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_loop_while(p):
    'loop : WHILE LPAREN valores RPAREN bloque'
    p[0] = ['while('+ p[3][0] + ')\n' + find_and_replace(p[5][0]), ' COMPLETAR ']

    if (p[3][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_loop_do(p):
    'loop : DO bloque WHILE LPAREN valores RPAREN PUNTOYCOMA'
    p[0] = ['do\n    ' + find_and_replace(p[2][0]) + '\nwhile(' + p[5][0] + ');' +'\n', ' COMPLETAR ']

    if (p[5][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_loop_for(p):
    'loop : FOR LPAREN var_asig PUNTOYCOMA valores PUNTOYCOMA exp_arit RPAREN bloque'
    p[0] = ['for(' + p[3][0] + ';' + p[5][0] + ';' + p[7][0] +')\n    ' + find_and_replace(p[9][0]) + '\n', ' COMPLETAR ']

    if (p[5][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_ifelse(p):
    'ifelse : IF LPAREN valores RPAREN bloque ELSE bloque'
    p[0] = ['If(' + p[3][0] + ')\n    ' + find_and_replace(p[5][0]) + '\nelse\n    ' + find_and_replace(p[7][0]) + '\n', 'COMPLETAR']

    if (p[3][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_ifSinElse(p):
    'ifelse : IF LPAREN valores RPAREN bloque'
    p[0] = ['If(' + p[3][0] + ')\n    ' + find_and_replace(p[5][0]) + '\n', ' COMPLETAR ']

    if (p[3][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_bloque_cb(p):
    'bloque : COMENTARIO bloque'
    p[0] = [p[1], ' COMPLETAR ']

def p_bloque_s(p):
    'bloque : sentencia'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_bloque_c(p):
    'bloque : control'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_bloque_p(p):
    'bloque : LLAVEIZQ p LLAVEDER'
    p[0] = ['{' + p[2][0] + '}', ' COMPLETAR ']

#Producciones para funciones
def p_funcion_ret(p):
    'funcion : func_ret'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_funcion_void(p):
    'funcion : func_void '
    p[0] = [p[1][0], ' COMPLETAR ']

def p_func_void(p):
    'func_void : PRINT LPAREN valores RPAREN'
    p[0] = ['print(' + p[3][0] + ')', ' COMPLETAR ']

def p_funcion_ret_int(p):
    'func_ret : func_ret_int'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_funcion_ret_cadena(p):
    'func_ret : func_ret_cadena'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_funcion_ret_bool(p):
    'func_ret : func_ret_bool'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_funcion_ret_arreglo(p):
    'func_ret : func_ret_arreglo'
    p[0] = [p[1][0], ' COMPLETAR ']

def p_funcion_ret_arreglo_3(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores COMA valores RPAREN'
    p[0] = ['multiplicacionEscalar(' + p[3][0] + ',' + p[5][0] + ',' + p[7][0] + ')', ' COMPLETAR ']

    if (p[3][1] != "VECTOR_NUMBER" or not esNumber(p[5][1]) or p[7][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_funcion_ret_arreglo_2(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores RPAREN'
    p[0] = ['multiplicacionEscalar(' + p[3][0] + ',' + p[5][0] + ')', ' COMPLETAR ']

    if (p[3][1] != "VECTOR_NUMBER" or not esNumber(p[5][1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_funcion_ret_int_length(p):
    'func_ret_int : LENGTH LPAREN valores RPAREN'
    p[0] = ['length(' + p[3][0] + ')', ' COMPLETAR ']

    if (p[3][1] != "STRING" and not esVector(p[3][1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_funcion_ret_string(p):
    'func_ret_cadena : CAPITALIZAR LPAREN valores RPAREN'
    p[0] = ['capitalizar(' + p[3][0] + ')', ' COMPLETAR ']

    if (p[3][1] != "STRING"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_funcion_ret_bool_f(p):
    'func_ret_bool : COLINEALES LPAREN valores COMA valores RPAREN '
    p[0] = ['colineales(' + p[3][0] + ',' + p[5][0] + ')', ' COMPLETAR ']

    if (p[3][1] != 'VECTOR_NUMBER' or p[5][1] != 'VECTOR_NUMBER'):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

#Producciones para vectores y variables
def p_valores_exp_arit(p):
    'valores : exp_arit'
    p[0] = [toStrIfInt(p[1][0]), 'NUMBER']

def p_valores_exp_bool(p):
    'valores : comparacion'
    p[0] = [p[1][0], 'BOOL']

def p_valores_exp_cadena(p):
    'valores : exp_cadena'
    p[0] = [p[1][0], 'STRING']

def p_valores_exp_arreglo(p):
    'valores : exp_arreglo'
    p[0] = [p[1][0], 'ARREGLO']

def p_valores_reg(p):
    'valores : reg'
    p[0] = [p[1][0], 'REGISTRO']

def p_valores_variables(p):
    'valores : var_asig_l'
    p[0] = [p[1][0], p[1][1]]

def p_exp_arreglo(p):
    'exp_arreglo : LCORCHETE lista_valores RCORCHETE'
    p[0] = ['[' + toStrIfInt(p[2][0]) +  ']', 'ARREGLO_' + p[2][1]]

def p_exp_arreglo_vacio(p):
    'exp_arreglo : LCORCHETE RCORCHETE'
    p[0] = ['[]', 'ARREGLO_VACIO']

def p_exp_arreglo_mult_escalar(p):
    'exp_arreglo : func_ret_arreglo'
    p[0] = [p[1][0], p[1][1]]

def p_lista_valores_end(p):
    'lista_valores : valores'
    p[0] = [p[1][0], p[1][1]]

def p_lista_valores_lista(p):
    'lista_valores : valores COMA lista_valores'

    tipo = p[3][1]
    if p[1][1] != 'ND':
    	tipo = p[1][1]

    p[0] = [p[1][0] + ',' + p[3][0], tipo]

    if (p[1][1] != p[3][1] or p[1][1] == 'ND' or p[3][1] == 'ND'):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

#INCOMPLETO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

#Producciones Registros
def p_reg(p):
    'reg : LLAVEIZQ reg_item LLAVEDER'
    p[0] = ['{' + p[1][0] + '}',' COMPLETAR']

def p_reg_item_list(p):
    'reg_item : CADENA DOSPUNTOS valores COMA reg_item' 
    p[0] = [p[1] + ":" + toStrIfInt(p[3][0]) + ',' + p[5][0],' COMPLETAR']

def p_reg_item(p):
    'reg_item : CADENA DOSPUNTOS valores' 
    p[0] = [p[1] + ":" + toStrIfInt(p[3][0]), ' COMPLETAR ']

#Producciones de asignaciones
def p_var_asig_l_var(p):
    'var_asig_l : VARIABLE'
    p[0] = [p[1], 'ND' ]


def p_var_asig_l_res(p):
    'var_asig_l : RES'
    p[0] = [p[1], 'ND' ]

def p_var_asig_l_vec(p):
    'var_asig_l : VARIABLE LCORCHETE exp_arit RCORCHETE'
    p[0] = [p[1] + '[' + str(p[3][0]) +  ']',tipo(estaDefinida(p[1]))]

    if not p[1] in variables_dict or tipo(estaDefinida(p[3])) != 'INT':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_l_vec1(p):
    'var_asig_l : VARIABLE LCORCHETE VARIABLE RCORCHETE'
    p[0] = [p[1] + '[' + p[3] +  ']',tipo(estaDefinida(p[1]))]

    if not (p[1] in variables_dict) or not (p[3] in variables_dict) or tipo(estaDefinida(p[3])) != 'INT':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_l_reg(p):
    'var_asig_l : VARIABLE PUNTO VARIABLE'
    p[0] = [p[1] + '.' + p[3],tipo(estaDefinida(p[1]))]

    if not (p[1] in variables_dict) or not (p[3] in variables_dict):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_base_mm(p):
    'var_asig : var_asig_l LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', ' COMPLETAR ']

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_var_asig_mm_base(p):
    'var_asig : LESSLESS var_asig_l'
    p[0] = ['--' + toStrIfInt(p[2][0]), ' COMPLETAR ']

    if not esNumber(p[2][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_var_asig_base_pp(p):
    'var_asig : var_asig_l MASMAS'
    p[0] = [toStrIfInt(p[1][0]) + '++', ' COMPLETAR ']
    # p[0] = toStrIfInt(p[1]) + str(type(p[1]))

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_var_asig_pp_base(p):
    'var_asig : MASMAS var_asig_l '
    p[0] = ['++' + toStrIfInt(p[2][0]), ' COMPLETAR ']

    if not esNumber(p[2][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_var_asig_multipl(p):
    'var_asig : var_asig_l MULTIPL valores'
    p[0] = [p[1][0] + '=*' + toStrIfInt(p[3][0]), ' COMPLETAR ']

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_dividi(p):
    'var_asig : var_asig_l DIVIDI valores'
    p[0] = [p[1][0] + '=/' + toStrIfInt(p[3][0]), ' COMPLETAR ']

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

#def p_var_asig_sigual(p):
#    'var_asig : VARIABLE'
#    p[0] = p[1]

def p_var_asig_agregar(p):
    'var_asig : var_asig_l AGREGAR valores'
    p[0] = [p[1][0] + '+=' + toStrIfInt(p[3][0]), ' COMPLETAR ']

    if (esNumber(p[1][1]) and esNumber(p[1][1])) or (p[1][1] == "STRING" and p[3][1] == "STRING")  :
        pass
    else:
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_sacar(p):
    'var_asig : var_asig_l SACAR valores'
    p[0] = [p[1][0] + '-=' + toStrIfInt(p[3][0], ' COMPLETAR ')]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig_multipl(p):
    'var_asig : var_asig_l MULTIPL valores'
    p[0] = [p[1][0] + '=*' + toStrIfInt(p[3][0]), ' COMPLETAR ']

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_var_asig(p):
    'var_asig : var_asig_l ASIGNACION valores'
    p[0] = [p[1][0] + '=' + toStrIfInt(p[3][0]), ' COMPLETAR ']

# En asignacion no importa el tipo, por mas que tengas una variable 'aux' del tipo que sea
# aux = 10; deberia ser valido



#def p_var_asig_vec1(p):
#    'var_asig : VARIABLE LCORCHETE exp_arit RCORCHETE ASIGNACION valores'
#    p[0] = p[1] + '[' + str(p[3]) +  '] =' + p[6]

#def p_var_asig_vec2(p):
#    'var_asig : VARIABLE LCORCHETE VARIABLE RCORCHETE ASIGNACION valores'
    #Chequear tipo de variable sea NAT
#    p[0] = p[1] + '[' + p[3] +  '] =' + p[6]

#def p_var_asig_reg(p):
#    'var_asig : VARIABLE PUNTO VARIABLE ASIGNACION valores'
#    p[0] = p[1] + '.' + p[3] +  ' = ' + p[5]



def p_var_asig_oper_ternario(p):
    'var_asig : var_asig_l ASIGNACION operador_ternario'
    p[0] = [p[1][0] + '=' + p[3][0], ' COMPLETAR ']

    if (p[1][1] != "OPERADOR_TERNARIO"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_operador_ternarioret_bool(p):
    'operador_ternario : exp_bool INTERROGACION exp_bool DOSPUNTOS exp_bool'
    p[0] = [ p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0] , ' COMPLETAR ']

    if (p[1][1] != "BOOL" or p[3][1] != "BOOL" or p[5][1] != "BOOL"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_operador_ternarioret_mat(p):
    'operador_ternario : exp_bool INTERROGACION exp_arit DOSPUNTOS exp_arit'
    p[0] = [ p[1][0] + ' ? ' + toStrIfInt(p[3][0]) + ':' + p[5][0], ' COMPLETAR ']

    if (p[1][1] != "BOOL" or p[3][1] != "NUMBER" or p[5][1] != "NUMBER"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_operador_ternarioret_cadena(p):
    'operador_ternario : exp_cadena INTERROGACION exp_cadena DOSPUNTOS exp_cadena'
    p[0] = [p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0], ' COMPLETAR ']

    if (p[1][1] != "BOOL" or p[3][1] != "STRING" or p[5][1] != "STRING"):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_oper_var_reg(p):
    'var_oper : VARIABLE PUNTO  VARIABLE'
    p[0] = [p[1] + '.' + p[3], ' COMPLETAR ']

def p_oper_var_vec(p):
    'var_oper : VARIABLE LCORCHETE VARIABLE RCORCHETE'
    p[0] = [p[1] + '[' + p[3] + ']', tipo(estaDefinida(p[1]))]

    if not esArreglo(estaDefinida(p[1])) or estaDefinida(p[3]) != "NUMBER_ENTERO":
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_oper_var_vec2(p):
    'var_oper : VARIABLE LCORCHETE exp_arit RCORCHETE'
    p[0] = [p[1] + '[' + p[3][0] + ']', tipo(estaDefinida(p[1]))]

    if not esArreglo(estaDefinida(p[1])) or p[3][1] != "NUMBER_ENTERO":
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


#Producciones operaciones binarias con enteros
def p_exp_arit_ept(p):
    'exp_arit : exp_arit PLUS term'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]


def p_exp_arit_epv(p):
    'exp_arit : exp_arit PLUS VARIABLE'
    p[0] = [p[1][0] + ' + ' + p[3], tipoNumber(p[1][1],estaDefinida(p[3]))]

    if not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_epv2(p):
    'exp_arit : exp_arit PLUS var_oper'
    p[0] = [p[1][0] + ' + ' + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_vpt(p):
    'exp_arit : VARIABLE PLUS term'
    p[0] = [p[1] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(estaDefinida(p[1]),p[3][1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_v2pt(p):
    'exp_arit : var_oper PLUS term'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_vpv(p):
    'exp_arit : VARIABLE PLUS VARIABLE'
    p[0] = [p[1] + ' + ' + toStrIfInt(p[3]), tipoNumber(estaDefinida(p[1]),estaDefinida(p[3]))]

    if not esNumber(estaDefinida(p[1])) or not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_v2pv2(p):
    'exp_arit : var_oper PLUS var_oper'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


def p_exp_arit_emt(p):
    'exp_arit : exp_arit MINUS term'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

def p_exp_arit_emv(p):
    'exp_arit : exp_arit MINUS VARIABLE'
    p[0] = [p[1][0] + ' - ' + p[3], tipoNumber(p[1][1],estaDefinida(p[3]))]

    if not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_exp_arit_emv2(p):
    'exp_arit : exp_arit MINUS var_oper'
    p[0] = [p[1][0] + ' - ' + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_exp_arit_vmt(p):
    'exp_arit : VARIABLE MINUS term'
    p[0] = [p[1] + ' - ' + toStrIfInt(p[3][0]), tipoNumber(estaDefinida(p[1]),p[3][1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_v2mt(p):
    'exp_arit : var_oper MINUS term'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_exp_arit_vmv(p):
    'exp_arit : VARIABLE MINUS VARIABLE'
    p[0] = [p[1] + ' - ' + toStrIfInt(p[3]), tipoNumber(estaDefinida(p[1]),estaDefinida(p[3]))]

    if not esNumber(estaDefinida(p[1])) or not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_arit_v2mv2(p):
    'exp_arit : var_oper MINUS var_oper'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]),  tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_exp_arit_term(p):
    'exp_arit : term'
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]




def p_arit_oper2_times(p):
    'arit_oper_2 : TIMES'
    p[0] = [p[1], 'ND' ]

def p_arit_oper2_div(p):
    'arit_oper_2 : DIV'
    p[0] = [p[1], 'ND' ]

def p_arit_oper2_mod(p):
    'arit_oper_2 : MODULO'
    p[0] = [p[1], 'ND' ]


def p_term_tmf(p):
    'term : term arit_oper_2 factor'
    p[0] = [p[1][0] + p[2][0] + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if p[2][0] == '/' and not p[3][0]:
        message = "[Math Error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_term_tmv(p):
    'term : term arit_oper_2 VARIABLE'
    p[0] = [p[1][0] + p[2][0] + p[3], tipoNumber(p[1][1],estaDefinida(p[3]))]

    if not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_term_tmv2(p):
    'term : term arit_oper_2 var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_term_vmf(p):
    'term : VARIABLE  arit_oper_2 factor'
    p[0] = [p[1] + p[2][0] + toStrIfInt(p[3][0]), tipoNumber(estaDefinida(p[3]),p[3][1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_term_v2mf(p):
    'term : var_oper arit_oper_2 factor'
    p[0] = [p[1][0] + p[2][0] + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_term_vmv(p):
    'term : VARIABLE arit_oper_2 VARIABLE'
    p[0] = [p[1] + p[2][0] + p[3], tipoNumber(estaDefinida(p[3]),estaDefinida(p[3][1]))]

    if not esNumber(estaDefinida(p[1])) or not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_term_v2mv2(p):
    'term : var_oper arit_oper_2 var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_term_factor(p):
    'term : factor'
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]

def p_factor_base_exp(p):
    'factor : base ELEVADO sigexp'
    p[0] = [p[1][0] + ' ^' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

def p_factor_var_exp(p):
    'factor : VARIABLE ELEVADO sigexp'
    p[0] = [p[1] + ' ^' + toStrIfInt(p[3][0]), tipoNumber(estaDefinida(p[1]),p[3][1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_factor_var_op__exp(p):
    'factor : var_oper ELEVADO sigexp'
    p[0] = [p[1][0] + ' ^' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_factor_base(p):
    'factor : base '
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]

def p_factor_m_base(p):
    'factor : MINUS base '
    p[0] = ['-' + toStrIfInt(p[2][0]), 'NUMBER_FLOAT']

def p_factor_var_mm(p):
    'factor : VARIABLE LESSLESS'
    p[0] = [toStrIfInt(p[1]) + '--', estaDefinida(p[1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_factor_var_op_mm(p):
    'factor : var_oper LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', p[1][1]]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_factor_base_mm(p):
    'factor : base LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', p[1][1]]

def p_factor_mm_var(p):
    'factor : LESSLESS VARIABLE'
    p[0] = ['--' + toStrIfInt(p[2]), estaDefinida(p[2])]

    if not esNumber(estaDefinida(p[2])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_factor_mm_var_op(p):
    'factor : LESSLESS var_oper'
    p[0] = ['--' + toStrIfInt(p[2][0]), p[2][1]]

    if not esNumber(p[2][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_factor_mm_base(p):
    'factor : LESSLESS base '
    p[0] = ['--' + toStrIfInt(p[2][0]), p[2][1]]

def p_factor_var_pp(p):
    'factor : VARIABLE MASMAS'
    p[0] = [toStrIfInt(p[1]) + '++', estaDefinida(p[1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_factor_var_op_pp(p):
    'factor : var_oper MASMAS'
    p[0] = [toStrIfInt(p[1][0]) + '++', p[1][1]]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_factor_base_pp(p):
    'factor : base MASMAS'
    p[0] = [toStrIfInt(p[1][0]) + '++', p[1][1]]

def p_factor_pp_var(p):
    'factor : MASMAS VARIABLE'
    p[0] = ['++' + toStrIfInt(p[2]), estaDefinida(p[2])]

    if not esNumber(estaDefinida(p[2])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_factor_pp_var_op(p):
    'factor : MASMAS var_oper'
    p[0] = ['++' + toStrIfInt(p[2][0]), p[2][1]]

    if not esNumber(p[2][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)

def p_factor_pp_base(p):
    'factor : MASMAS base '
    p[0] = ['++' + toStrIfInt(p[2][0]), p[2][1]]

def p_base_expr(p):
    'base : LPAREN exp_arit RPAREN'
    p[0] = ['(' + toStrIfInt(p[2][0]) + ')', p[2][1]]

def p_base_valor(p):
    'base : NUMBER'
    #chequear que el valor sea numerico <-------- podria no se un numero ???????????????
    p[0] =  [toStrIfInt(p[1]), tipoNumber(p[1])] 

def p_base_func_ret_int(p):
    'base : func_ret_int'
    #chequear que el valor sea numerico <-------- podria no se un numero ???????????????
    p[0] =  [toStrIfInt(p[1][0]), p[1][1]] 

def p_sigexp_m(p):
    'sigexp : MINUS exp'
    p[0] = ['-' + p[2][0], p[2][1]]

def p_sigexp_exp(p):
    'sigexp : exp'
    p[0] =  [toStrIfInt(p[1][0]), p[1][1]]

def p_exp_var(p):
    'exp : VARIABLE'
    p[0] =  [p[1], estaDefinida(p[1])]

    if not esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_var_op(p):
    'exp : var_oper'
    p[0] =  [p[1][0], p[1][1]]

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_exp_valor(p):
    'exp : NUMBER'
    #chequear que el valor sea numerico <--------- Es necesario ???????
    p[0] =  [toStrIfInt(p[1]), tipoNumber(p[1])]

def p_exp__expr(p):
    'exp : LPAREN exp_arit RPAREN'
    p[0] = ['(' + toStrIfInt(p[2][0]) + ')', p[2][1]]


#Producciones operaciones con Strings
def p_exp_cadena_concat(p):
    'exp_cadena : exp_cadena PLUS term_cadena'
    p[0] = [p[1][0] + ' + ' +  p[3][0], 'STRING']

def p_exp_cadena_concat_1(p):
    'exp_cadena : VARIABLE PLUS term_cadena'
    p[0] = [p[1] + ' + ' +  p[3][0], 'STRING']

    if estaDefinida(p[1]) != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_exp_cadena_concat_2(p):
    'exp_cadena : exp_cadena PLUS VARIABLE'
    p[0] = [p[1][0] + ' + ' +  p[3], 'STRING']

    if estaDefinida(p[2]) != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_exp_cadena_term(p):
    'exp_cadena : term_cadena'
    p[0] = [p[1][0], 'STRING']

def p_exp_cadena_cadena(p):
    'term_cadena : CADENA'
    p[0] = [p[1], 'STRING' ]

def p_exp_cadena_funct_ret_string(p):
    'term_cadena : CAPITALIZAR LPAREN valores RPAREN'
    p[0] = ['capitalizar(' + p[3][0] + ')', 'STRING']

    if p[3][1] != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_exp_cadena_parent(p):
    'term_cadena : LPAREN exp_cadena RPAREN'
    p[0] = ['(' + p[2][0] + ')', 'STRING']



#Producciones de operaciones booleanas

def p_comparacionarision_igual(p):
    'comparacion : comparacion IGUAL exp_bool'
    p[0] = [p[1][0] + ' == ' + p[3][0], 'BOOL']

def p_comparacionarision_dis(p):
    'comparacion : comparacion DISTINTO exp_bool'
    p[0] = [p[1][0] + ' != ' + p[3][0], 'BOOL']

def p_comparacionarision_bool_exp(p):
    'comparacion : exp_bool'
    p[0] = [p[1][0], 'BOOL']

def p_bool_expr_eat(p):
    'exp_bool : exp_bool AND term_bool'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

def p_bool_expr_vaf(p):
    'exp_bool : VARIABLE AND term_bool'
    p[0] = [p[1] + ' and ' + p[3][0], 'BOOL']

    if estaDefinida(p[1]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_bool_expr_v2af(p):
    'exp_bool : var_oper AND term_bool'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if p[1][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_expr_eav(p):
    'exp_bool : exp_bool AND VARIABLE'
    p[0] = [p[1][0] + ' and ' + p[3], 'BOOL']

    if estaDefinida(p[3]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_expr_eav2(p):
    'exp_bool : exp_bool AND var_oper'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if p[3][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_expr_v2av2(p):
    'exp_bool : var_oper AND var_oper'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if p[3][1] != 'BOOL' or p[1][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_expr_vav(p):
    'exp_bool : VARIABLE AND VARIABLE'
    p[0] = [p[1] + ' and ' + p[3], 'BOOL']

    if estaDefinida(p[1]) != 'BOOL' or estaDefinida(p[3]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_expr_term(p):
    'exp_bool : term_bool'
    p[0] = [p[1][0], 'BOOL' ]

def p_bool_tof(p):
    'term_bool : term_bool OR factor_bool'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

def p_bool_tov(p):
    'term_bool : term_bool OR VARIABLE'
    p[0] = [p[1][0] + ' or ' + p[3], 'BOOL']

    if estaDefinida(p[3]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_bool_tov2(p):
    'term_bool : term_bool OR var_oper'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if p[3][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_vof(p):
    'term_bool : VARIABLE OR factor_bool'
    p[0] = [p[1] + ' or ' + p[3][0], 'BOOL']

    if estaDefinida(p[1]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_v2of(p):
    'term_bool : var_oper OR factor_bool'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if p[1][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_v2ov2(p):
    'term_bool : var_oper OR var_oper'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if p[1][1] != 'BOOL' or p[3][1] != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_bool_vov(p):
    'term_bool : VARIABLE OR VARIABLE'
    p[0] = [p[1] + ' or ' + p[3], 'BOOL']

    if estaDefinida(p[1]) != 'BOOL' or estaDefinida(p[3]) != 'BOOL':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_bool_term_factor(p):
    'term_bool : factor_bool'
    p[0] = [p[1][0], ' BOOL'] 

def p_term_not(p):
    'term_bool : NOT factor_bool'
    p[0] = ['not ' + p[2][0], 'BOOL']

def p_term_bool_parentesis(p):
    'factor_bool : LPAREN exp_bool RPAREN'
    p[0] = ['(' + p[2][0] + ')', 'BOOL']

def p_term_bool_bool(p):
    'factor_bool : BOOL'
    p[0] = [str(p[1]), 'BOOL']

def p_term_bool_func(p):
    'factor_bool : func_ret_bool'
    p[0] = [str(p[1][0]), 'BOOL']

#def p_bool_expr_comparacion(p):
#    'factor_bool : comparacion'
#    p[0] = p[1] 

def p_operador_comparacion_igual(p):
    'operador_comp : IGUAL'
    p[0] = [' == ', 'ND']

def p_operador_comparacion_mayor(p):
    'operador_comp : MAYOR'
    p[0] = [' > ', 'ND']

def p_operador_comparacion_menor(p):
    'operador_comp : MENOR'
    p[0] = [' < ', 'ND']

def p_operador_comparacion_dif(p):
    'operador_comp : DISTINTO'
    p[0] = [' != ', 'ND']

def p_comparcion_exp_arit(p):
    'comparacion : exp_arit operador_comp exp_arit'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

def p_comparcion_acv(p):
    'comparacion : exp_arit operador_comp VARIABLE'
    p[0] = [p[1][0] + p[2][0] + p[3], 'BOOL']

    if not esNumber(estaDefinida(p[3])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_acv2(p):
    'comparacion : exp_arit operador_comp var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

    if not esNumber(p[3][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_vca(p):
    'comparacion : VARIABLE operador_comp exp_arit'
    p[0] = [p[1] + p[2][0] + p[3][0], 'BOOL']

    if esNumber(estaDefinida(p[1])):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_v2ca(p):
    'comparacion : var_oper operador_comp exp_arit'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

    if not esNumber(p[1][1]):
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_comparcion_exp_cadena(p):
    'comparacion : exp_cadena operador_comp exp_cadena'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

def p_comparcion_exp_vcc(p):
    'comparacion : VARIABLE operador_comp exp_cadena'
    p[0] = [p[1] + p[2][0] + p[3][0], ' COMPLETAR ']

    if estaDefinida(p[1]) != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_exp_v2cc(p):
    'comparacion : var_oper operador_comp exp_cadena'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

    if p[1][1] != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_comparcion_exp_ccv(p):
    'comparacion : exp_cadena operador_comp VARIABLE'
    p[0] = [p[1][0] + p[2][0] + p[3], 'BOOL']

    if estaDefinida(p[3]) != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_exp_ccv2(p):
    'comparacion : exp_cadena operador_comp var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

    if p[3][1] != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)


def p_comparcion_exp_vcv(p):
    'comparacion : VARIABLE operador_comp VARIABLE'
    p[0] = [p[1] + p[2][0] + p[3], 'BOOL']

    if estaDefinida(p[1]) != 'STRING' or estaDefinida(p[3]) != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_comparcion_exp_v2cv2(p):
    'comparacion : var_oper operador_comp var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']

    if p[1][1] != 'STRING' or p[3][1] != 'STRING':
        message = "[Semantic error]"
        if p is not None:
            message += "\ntype:" + p[0][1]
            message += "\nvalue:" + p[0][0]
            # message += "\nline:" + str(p.lineno)
            # message += "\nposition:" + str(p.lexpos)


        raise Exception(message)

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
