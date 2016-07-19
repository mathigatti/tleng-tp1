from lexer_rules import tokens
import ply.yacc as yacc
from semantic_error import SemanticException

# Diccionario donde se almacenaran las variables declaradas junto con su tipo
variables_dict = dict()
reg_dict = dict()
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

# Funcion que devuelve True si es o puede llegar a ser NUMBER
def esNumber(palabra):
	return (palabra[0:6] == 'NUMBER' or palabra == 'CUALQUIER_TIPO') 

# Funcion que devuelve True si es o puede llegar a ser REGISTRO
def esRegistro(palabra):
	return (palabra[0:8] == 'REGISTRO' or palabra == 'CUALQUIER_TIPO')

# Funcion que devuelve True si es o puede llegar a ser VECTOR
def esVector(palabra):
    return (palabra[0:6] == 'VECTOR' or palabra == 'CUALQUIER_TIPO') 

# Funcion que devuelve True si es o puede llegar a ser BOOL
def esBool(palabra):
    return (palabra == 'BOOL' or palabra == 'CUALQUIER_TIPO') 

# Funcion que devuelve True si es o puede llegar a ser STRING
def esString(palabra):
    return (palabra == 'STRING' or palabra == 'CUALQUIER_TIPO') 

# Funcion que accede al diccionario de variables y devuelve su tipo (Si esta definida)
# Si no esta definida devuelve ND
def estaDefinida(key):
	if key in variables_dict:
		return variables_dict[key]
	else: return 'ND'

# Funcion que accede al diccionario de variables y devuelve su tipo (Si esta definida)
# Si no esta definida devuelve ND
def estaReg(key):
    if key in reg_dict:
        return reg_dict[key]
    else: return 'ND'


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
    if (p.lineno(1) == p.lineno(2)) and p[2][1] == 'COMENTARIO':    	
        p[0] = [p[1][0] + ' '  + p[2][0], 'ND']
    else:
        p[0] = [p[1][0] + '\n'  + p[2][0], 'ND']

def p_programa_coment_pp(p):
    'p : COMENTARIO p'
    p[0] = [p[1] + '\n'  + p[2][0], 'COMENTARIO']

def p_programa_ctl_p(p):
    'p : control pp'
    if (p.lineno(1) == p.lineno(2)) and p[2][1] == 'COMENTARIO':    	
        p[0] = [p[1][0] + ' '  + p[2][0], 'ND']
    else:
        p[0] = [p[1][0] + '\n'  + p[2][0], 'ND']

def p_pp_s_pp(p):
    'pp : sentencia pp'
    if (p.lineno(1) == p.lineno(2)) and p[2][1] == 'COMENTARIO':    	
        p[0] = [p[1][0] + ' '  + p[2][0], 'ND']
    else:
        p[0] = [p[1][0] + '\n'  + p[2][0], 'ND']

def p_pp_ctl_pp(p):
    'pp : COMENTARIO pp'
    p[0] = [p[1] + '\n'  + p[2][0], 'COMENTARIO']

def p_pp_comentario_p(p):
    'pp : control pp'
    if (p.lineno(1) == p.lineno(2)) and p[2][1] == 'COMENTARIO':    	
        p[0] = [p[1][0] + ' '  + p[2][0], 'ND']
    else:
        p[0] = [p[1][0] + '\n'  + p[2][0], 'ND']

def p_pp_empty(p):
    'pp : empty'
    p[0] = [p[1][0], 'ND']

def p_empty(p):
    'empty :'
    p[0] = ['', 'ND']
     
def p_sentencia_var_asig(p):
    'sentencia : var_asig PUNTOYCOMA'
    p[0] = [p[1][0] + ';', p[1][1]]


def p_sentencia_func(p):
    'sentencia : funcion PUNTOYCOMA'
    p[0] = [p[1][0] + ';', p[1][1]]

#Producciones para estructuras de control
def p_control_ifelse(p):
    'control : ifelse'
    p[0] = [p[1][0], 'ND']

def p_control_loop(p):
    'control : loop'
    p[0] = [p[1][0], 'ND']

def p_control_cond_term_var_asig_l(p):
    'control_cond_term : var_asig_l'
    p[0] = [ p[1][0],p[1][1]]

def p_control_cond_term_e_bool(p):
    'control_cond_term : exp_bool'
    p[0] = [ p[1][0],p[1][1]]

def p_control_cond_term_comp(p):
    'control_cond_term : comparacion'
    p[0] = [ p[1][0],p[1][1]]

def p_control_cond_term_ternario(p):
    'control_cond_term : operador_ternario'
    p[0] = [ p[1][0],p[1][1]]

def p_loop_while(p):
    'loop : WHILE LPAREN control_cond_term RPAREN bloque'
    p[0] = ['while('+ p[3][0] + ')\n    ' + find_and_replace(p[5][0]), 'ND']

    if not esBool(p[3][1]):
        pass
        raise SemanticException('LOOP',p.lineno(1),p.lexpos(1))

def p_loop_do(p):
    'loop : DO bloque WHILE LPAREN control_cond_term RPAREN PUNTOYCOMA'
    p[0] = ['do\n    ' + find_and_replace(p[2][0]) + '\nwhile(' + p[5][0] + ');' +'\n', 'ND']

    if not esBool(p[5][1]):
        pass
        raise SemanticException('LOOP',p.lineno(1),p.lexpos(1))

def p_loop_for(p):
    'loop : for'
    p[0] = [ p[1][0],'ND']

def p_for_main(p):
    'for : FOR LPAREN form_term PUNTOYCOMA form_term_2 PUNTOYCOMA form_term RPAREN bloque'
    p[0] = ['for(' + p[3][0] + ';' + p[5][0] + ';' + p[7][0] +')\n    ' + find_and_replace(p[9][0]) + '\n', 'ND']

    if not esBool(p[5][1]):
        pass
        raise SemanticException('LOOP',p.lineno(1),p.lexpos(1))

def p_for_term(p):
    'form_term : var_asig '
    p[0] = [ p[1][0],p[1][1]]

def p_for_term_2_val(p):
    'form_term_2 : valores '
    p[0] = [ p[1][0],p[1][1]]

def p_for_term_2_comp(p):
    'form_term_2 : comparacion'
    p[0] = [ p[1][0],p[1][1]]

def p_for_term_empty(p):
    'form_term : '
    p[0] = ['','ND']

def p_ifelse(p):
    'ifelse : IF LPAREN control_cond_term RPAREN bloque ELSE bloque'
    p[0] = ['If(' + p[3][0] + ')\n    ' + find_and_replace(p[5][0]) + '\nelse\n    ' + find_and_replace(p[7][0]) + '\n', 'ND']

    if not esBool(p[3][1]):
        pass
        raise SemanticException('IF',p.lineno(1),p.lexpos(1))

def p_ifSinElse(p):
    'ifelse : IF LPAREN control_cond_term RPAREN bloque'
    p[0] = ['If(' + p[3][0] + ')\n    ' + find_and_replace(p[5][0]) + '\n', 'ND']

    if not esBool(p[3][1]):
        pass
        raise SemanticException('IF',p.lineno(1),p.lexpos(1))

def p_bloque_cb(p):
    'bloque : COMENTARIO bloque'
    p[0] = [p[1] + '\n'  + p[2][0], 'COMENTARIO']

def p_bloque_s(p):
    'bloque : sentencia'
    p[0] = [p[1][0], 'ND']

def p_bloque_c(p):
    'bloque : control'
    p[0] = [p[1][0], 'ND']

def p_bloque_p(p):
    'bloque : LLAVEIZQ p LLAVEDER'
    p[0] = ['{' + p[2][0] + '}', 'ND']

#Producciones para funciones
def p_funcion_ret(p):
    'funcion : func_ret'
    p[0] = [p[1][0], p[1][1]]

def p_funcion_void(p):
    'funcion : func_void '
    p[0] = [p[1][0], 'ND']

def p_func_void(p):
    'func_void : PRINT LPAREN valores RPAREN'
    p[0] = ['print(' + p[3][0] + ')', 'ND']

def p_funcion_ret_int(p):
    'func_ret : func_ret_int'
    p[0] = [p[1][0], p[1][1]]

def p_funcion_ret_cadena(p):
    'func_ret : func_ret_cadena'
    p[0] = [p[1][0], p[1][1]]

def p_funcion_ret_bool(p):
    'func_ret : func_ret_bool'
    p[0] = [p[1][0], p[1][1]]

def p_funcion_ret_arreglo(p):
    'func_ret : func_ret_arreglo'
    p[0] = [p[1][0], p[1][1]]

def p_funcion_ret_arreglo_3(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores COMA valores RPAREN'
    p[0] = ['multiplicacionEscalar(' + p[3][0] + ',' + p[5][0] + ',' + p[7][0] + ')', 'VECTOR_NUMBER_' + tipoNumber(tipo(p[3][1]),p[5][1])]

    if (not esNumber(tipo(p[3][1])) and p[3][1] != "VECTOR_VACIO") or not esNumber(p[5][1]) or not esBool(p[7][1]):
        pass
        raise SemanticException('MULTIPLICACIONESCALAR',p.lineno(3),p.lexpos(3))

def p_funcion_ret_arreglo_2(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores RPAREN'
    p[0] = ['multiplicacionEscalar(' + p[3][0] + ',' + p[5][0] + ')', 'VECTOR_NUMBER_' + tipoNumber(tipo(p[3][1]),p[5][1])]

    if (not esNumber(tipo(p[3][1])) and p[3][1] != "VECTOR_VACIO") or not esNumber(p[5][1]):
        pass
        raise SemanticException('MULTIPLICACIONESCALAR',p.lineno(3),p.lexpos(3))

def p_funcion_ret_int_length(p):
    'func_ret_int : LENGTH LPAREN valores RPAREN'
    p[0] = ['length(' + p[3][0] + ')', 'NUMBER_INT']

    if (not esString(p[3][1]) and not esVector(p[3][1])):
        pass
        raise SemanticException('LENGTH',p.lineno(3),p.lexpos(3))


def p_funcion_ret_string(p):
    'func_ret_cadena : CAPITALIZAR LPAREN valores RPAREN'
    p[0] = ['capitalizar(' + p[3][0] + ')', 'STRING']

    if not esString(p[3][1]):
        pass
        raise SemanticException('CAPITALIZAR',p.lineno(3),p.lexpos(3))

def p_funcion_ret_bool_f(p):
    'func_ret_bool : COLINEALES LPAREN valores COMA valores RPAREN '
    p[0] = ['colineales(' + p[3][0] + ',' + p[5][0] + ')', 'BOOL']

    if (not esNumber(tipo(p[3][1])) and p[3][1] != "VECTOR_VACIO") or (not esNumber(tipo(p[5][1])) and p[5][1] != "VECTOR_VACIO"):
        pass
        raise SemanticException('COLINEALES',p.lineno(2),p.lexpos(2))

#Producciones para vectores y variables
def p_valores_exp_arit(p):
    'valores : exp_arit'
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]

def p_valores_exp_bool(p):
    'valores : exp_bool'
    p[0] = [p[1][0], 'BOOL']

def p_valores_exp_cadena(p):
    'valores : exp_cadena'
    p[0] = [p[1][0], 'STRING']

def p_valores_exp_arreglo(p):
    'valores : exp_arreglo'
    p[0] = [p[1][0], p[1][1]]


def p_valores_reg(p):
    'valores : reg'
    p[0] = [p[1][0], p[1][1]]

def p_valores_reg2(p):
    'valores : reg PUNTO VARIABLE'
    p[0] = [p[1][0] + '.' + p[3], 'CUALQUIER_TIPO']
    if estaReg(p[3]) == 'ND':
        pass
        raise SemanticException('REGISTRO',p.lineno(1),p.lexpos(1))

def p_valores_variables(p):
    'valores : var_asig_l'
    p[0] = [p[1][0], p[1][1]]


def p_valor_perador(p):
    'valores : LPAREN operador_ternario RPAREN '
    p[0] = [ '(' + p[2][0] + ')',p[2][1]]

def p_exp_arreglo(p):
    'exp_arreglo : LCORCHETE lista_valores RCORCHETE'
    p[0] = ['[' + toStrIfInt(p[2][0]) +  ']', 'VECTOR_' + p[2][1]]

def p_exp_arreglo_vacio(p):
    'exp_arreglo : LCORCHETE RCORCHETE'
    p[0] = ['[]', 'VECTOR_VACIO']

def p_exp_arreglo_mult_escalar(p):
    'exp_arreglo : func_ret_arreglo'
    p[0] = [p[1][0], p[1][1]]

def p_lista_valores_end(p):
    'lista_valores : valores'
    p[0] = [p[1][0], p[1][1]]

def p_lista_pt_end(p):
    'lista_valores : operador_ternario'
    p[0] = [p[1][0], p[1][1]]

def p_lista_valores_lista(p):
    'lista_valores : valores COMA lista_valores'

    tipo_lista = p[3][1]
    if p[1][1] != 'ND':
    	tipo_lista = p[1][1]
    p[0] = [p[1][0] + ',' + p[3][0], tipo_lista]

    if (p[1][1] != p[3][1] and p[1][1] != 'ND' and p[3][1] != 'ND' and p[1][1] != 'CUALQUIER_TIPO' and p[3][1] != 'CUALQUIER_TIPO'):
        pass
        raise SemanticException('LISTAINCORRECTA',p.lineno(1),p.lexpos(1))

def p_lista_ot_lista(p):
    'lista_valores : operador_ternario COMA lista_valores'

    tipo_lista = p[3][1]
    if p[1][1] != 'ND':
    	tipo_lista = p[1][1]

    p[0] = [p[1][0] + ',' + p[3][0], tipo_lista]

    if (p[1][1] != p[3][1] and p[1][1] != 'ND' and p[3][1] != 'ND'):
        pass
        #raise SemanticException('LISTAINCORRECTA',p.lineno(1),p.lexpos(1))
        
#Producciones Registros
def p_reg(p):
    'reg : LLAVEIZQ reg_item LLAVEDER'
    p[0] = ['{' + p[2][0] + '}', 'REGISTRO']

def p_reg_item_list(p):
    'reg_item : VARIABLE DOSPUNTOS valores COMA reg_item' 
    p[0] = [p[1] + ":" + toStrIfInt(p[3][0]) + ',' + p[5][0], 'ND']
    reg_dict[p[1]] = p[3][1]
    

def p_reg_item(p):
    'reg_item : VARIABLE DOSPUNTOS valores' 
    p[0] = [p[1] + ":" + toStrIfInt(p[3][0]), 'ND']
    reg_dict[p[1]] = p[3][1]


#Producciones de asignaciones
def p_var_asig_l_var(p):
    'var_asig_l : VARIABLE'
    p[0] = [p[1],estaDefinida(p[1])]


def p_var_asig_l_res(p):
    'var_asig_l : RES'
    p[0] = [p[1],estaDefinida(p[1])]

def p_var_asig_l_var_mem(p):
    'var_asig_l : VARIABLE var_member'
    p[0] = [p[1] + p[2][0],'CUALQUIER_TIPO']
    if not esVector(estaDefinida(p[1])) and not esRegistro(estaDefinida(p[1])):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))
    	

def p_var_member_vec_item_rec(p):
    'var_member : LCORCHETE var_asig_l RCORCHETE var_member'
    p[0] = ['[' + p[2][0] + ']' + p[4][0],'ND']
    if tipo(p[2][1]) != 'INT' and p[2][1] != 'CUALQUIER_TIPO':
        pass
        raise SemanticException('INDEX_NOT_NAT',p.lineno(2),p.lexpos(2))

    
def p_var_member_vec_item_2(p):
    'var_member : LCORCHETE exp_arit RCORCHETE'
    p[0] = ['[' + p[2][0] + ']','ND']
    if tipo(p[2][1]) != 'INT':
        pass
        raise SemanticException('INDEX_NOT_NAT',p.lineno(2),p.lexpos(2))
    
def p_var_member_vec_item_2_rec(p):
    'var_member : LCORCHETE exp_arit RCORCHETE var_member'
    p[0] = ['[' + p[2][0] + ']' + p[4][0], 'ND']
    if tipo(p[2][1]) != 'INT':
        pass
        raise SemanticException('INDEX_NOT_NAT',p.lineno(2),p.lexpos(2))
    
def p_var_member_vec_item_3(p):
    'var_member : LCORCHETE var_asig_l RCORCHETE'
    p[0] = ['[' + p[2][0] + ']', 'ND']
    if tipo(p[2][1]) != 'INT' and p[2][1] != 'CUALQUIER_TIPO':
        pass
        raise SemanticException('INDEX_NOT_NAT',p.lineno(2),p.lexpos(2))

def p_var_member_reg_item(p):
    'var_member : PUNTO VARIABLE'
    p[0] = [ '.' + p[2], 'ND']

    if estaReg(p[2]) == 'ND':
        pass
        raise SemanticException('REGISTRO',p.lineno(2),p.lexpos(2))

    
def p_var_member_reg_item_rec(p):
    'var_member : PUNTO VARIABLE var_member'
    p[0] = [ '.' + p[2] + p[3][0], 'ND' ]
    
    if estaReg(p[2]) == 'ND':
        pass
        raise SemanticException('REGISTRO',p.lineno(2),p.lexpos(2))

def p_var_asig_base_mm(p):
    'var_asig : var_asig_l LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', p[1][1]]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))


def p_var_asig_mm_base(p):
    'var_asig : LESSLESS var_asig_l'
    p[0] = ['--' + toStrIfInt(p[2][0]), p[2][1]]

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))


def p_var_asig_base_pp(p):
    'var_asig : var_asig_l MASMAS'
    p[0] = [toStrIfInt(p[1][0]) + '++', p[1][1]]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))


def p_var_asig_pp_base(p):
    'var_asig : MASMAS var_asig_l '
    p[0] = ['++' + toStrIfInt(p[2][0]), p[2][1]]

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))


def p_var_asig_multipl(p):
    'var_asig : var_asig_l MULTIPL valores'
    p[0] = [p[1][0] + '=*' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))

def p_var_asig_dividi(p):
    'var_asig : var_asig_l DIVIDI valores'
    p[0] = [p[1][0] + '=/' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))

def p_var_asig_agregar(p):
    'var_asig : var_asig_l AGREGAR valores'
    p[0] = [p[1][0] + '+=' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if (esNumber(p[1][1]) and esNumber(p[1][1])) or (p[1][1] == "STRING" and p[3][1] == "STRING")  :
        pass
    else:
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))

def p_var_asig_sacar(p):
    'var_asig : var_asig_l SACAR valores'
    p[0] = [p[1][0] + '-=' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('NODEFINIDA',p.lineno(1),p.lexpos(1))

def p_var_asig(p):
    'var_asig : var_asig_l ASIGNACION valores'
    p[0] = [p[1][0] + '=' + toStrIfInt(p[3][0]), 'ASIGNACION']
    variables_dict[p[1][0]] = p[3][1]

def p_var_comparacion(p):
    'var_asig : var_asig_l ASIGNACION comparacion'
    p[0] = [p[1][0] + '=' + toStrIfInt(p[3][0]), 'ASIGNACION']
    variables_dict[p[1][0]] = p[3][1]

def p_var_op_ternario(p):
    'var_asig : var_asig_l ASIGNACION operador_ternario'
    p[0] = [p[1][0] + '=' + toStrIfInt(p[3][0]), 'ASIGNACION']
    variables_dict[p[1][0]] = p[3][1]

# En asignacion no importa el tipo, por mas que tengas una variable 'aux' del tipo que sea
# aux = 10; deberia ser valido

def p_operador_ternario(p):
    'operador_ternario : valores INTERROGACION valores DOSPUNTOS valores'
    p[0] = [  p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0],p[3][1]]
    if not esBool(p[1][1]) or (p[3][1] != p[5][1] and not(esNumber(p[3][1]) and esNumber(p[5][1])) and p[3][1] != 'CUALQUIER_TIPO' and p[5][1] != 'CUALQUIER_TIPO'):
            raise SemanticException('OPTERNARIO',p.lineno(1),p.lexpos(1))

def p_operador_ternario_2(p):
    'operador_ternario : comparacion INTERROGACION valores DOSPUNTOS valores'
    p[0] = [  p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0],p[3][1]]
    if not esBool(p[1][1]) or (p[3][1] != p[5][1] and not(esNumber(p[3][1]) and esNumber(p[5][1])) and p[3][1] != 'CUALQUIER_TIPO' and p[5][1] != 'CUALQUIER_TIPO'):
            raise SemanticException('OPTERNARIO',p.lineno(1),p.lexpos(1))

def p_operador_ternario_3(p):
    'operador_ternario : valores INTERROGACION valores DOSPUNTOS operador_ternario'
    p[0] = [  p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0],p[3][1]]
    if not esBool(p[1][1]) or (p[3][1] != p[5][1] and not(esNumber(p[3][1]) and esNumber(p[5][1])) and p[3][1] != 'CUALQUIER_TIPO' and p[5][1] != 'CUALQUIER_TIPO'):
        raise SemanticException('OPTERNARIO',p.lineno(1),p.lexpos(1))

def p_operador_ternario_4(p):
    'operador_ternario : comparacion INTERROGACION valores DOSPUNTOS operador_ternario'                             
    p[0] = [  p[1][0] + ' ? ' + p[3][0] + ':' + p[5][0],p[3][1]]
    if not esBool(p[1][1]) or (p[3][1] != p[5][1] and not(esNumber(p[3][1]) and esNumber(p[5][1])) and p[3][1] != 'CUALQUIER_TIPO' and p[5][1] != 'CUALQUIER_TIPO'):
            raise SemanticException('OPTERNARIO',p.lineno(1),p.lexpos(1))

def p_oper_var(p):
    'var_oper : var_asig_l'
    p[0] = [p[1][0] , p[1][1]]

def p_oper_ternaerio(p):
    'var_oper : LPAREN operador_ternario RPAREN '
    p[0] = [ '(' + p[2][0] + ')', p[2][1]]

def p_oper_arreglo(p):
    'var_oper : exp_arreglo'
    p[0] = [p[1][0] , p[1][1]]

def p_oper_reg_correcto(p):
    'var_oper : reg PUNTO VARIABLE'
    p[0] = [p[1][0] , 'CUALQUIER_TIPO']

def p_exp_arregloValor(p):
    'exp_arreglo : LCORCHETE lista_valores RCORCHETE exp_arreglo'
    p[0] = ['[' + toStrIfInt(p[2][0]) +  ']' + p[4][0], 'CUALQUIER_TIPO']

#Producciones operaciones binarias con Numeros


def p_exp_arit_ept(p):
    'exp_arit : exp_arit PLUS term'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]


def p_exp_arit_epv2(p):
    'exp_arit : exp_arit PLUS var_oper'
    p[0] = [p[1][0] + ' + ' + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_exp_arit_v2pt(p):
    'exp_arit : var_oper PLUS term'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_exp_arit_v2pv2(p):
    'exp_arit : var_oper PLUS var_oper'
    p[0] = [p[1][0] + ' + ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_arit_emt(p):
    'exp_arit : exp_arit MINUS term'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]


def p_exp_arit_emv2(p):
    'exp_arit : exp_arit MINUS var_oper'
    p[0] = [p[1][0] + ' - ' + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_arit_v2mt(p):
    'exp_arit : var_oper MINUS term'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_arit_v2mv2(p):
    'exp_arit : var_oper MINUS var_oper'
    p[0] = [p[1][0] + ' - ' + toStrIfInt(p[3][0]),  tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

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

    if p[2][0] == '/' and p[3][0] == 0:
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_term_tmv2(p):
    'term : term arit_oper_2 var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_term_v2mf(p):
    'term : var_oper arit_oper_2 factor'
    p[0] = [p[1][0] + p[2][0] + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_term_v2mv2(p):
    'term : var_oper arit_oper_2 var_oper'
    p[0] = [p[1][0] + p[2][0] + p[3][0], tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]) or not esNumber(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_term_factor(p):
    'term : factor'
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]

def p_factor_base_exp(p):
    'factor : base ELEVADO sigexp'
    p[0] = [p[1][0] + ' ^' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]


def p_factor_var_op__exp(p):
    'factor : var_oper ELEVADO sigexp'
    p[0] = [p[1][0] + ' ^' + toStrIfInt(p[3][0]), tipoNumber(p[1][1],p[3][1])]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_factor_base(p):
    'factor : base '
    p[0] = [toStrIfInt(p[1][0]), p[1][1]]

def p_factor_m_base(p):
    'factor : MINUS base '
    p[0] = ['-' + toStrIfInt(p[2][0]), 'NUMBER_FLOAT']

def p_factor_m_var_oper(p):
    'factor : MINUS var_oper'
    p[0] = ['-' + p[2][0], 'NUMBER_FLOAT']

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_factor_var_op_mm(p):
    'factor : var_oper LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', p[1][1]]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

        
def p_factor_base_mm(p):
    'factor : base LESSLESS'
    p[0] = [toStrIfInt(p[1][0]) + '--', p[1][1]]

def p_factor_mm_var_op(p):
    'factor : LESSLESS var_oper'
    p[0] = ['--' + toStrIfInt(p[2][0]), p[2][1]]

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_factor_mm_base(p):
    'factor : LESSLESS base '
    p[0] = ['--' + p[2][0], p[2][1]]

def p_factor_var_op_pp(p):
    'factor : var_oper MASMAS'
    p[0] = [p[1][0] + '++', p[1][1]]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_factor_base_pp(p):
    'factor : base MASMAS'
    p[0] = [toStrIfInt(p[1][0]) + '++', p[1][1]]

def p_factor_pp_var_op(p):
    'factor : MASMAS var_oper'
    p[0] = ['++' + p[2][0], p[2][1]]

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_factor_pp_base(p):
    'factor : MASMAS base '
    p[0] = ['++' + p[2][0], p[2][1]]

def p_base_expr(p):
    'base : LPAREN exp_arit RPAREN'
    p[0] = ['(' + p[2][0] + ')', p[2][1]]

def p_base_paren_var_oper(p):
    'base : LPAREN var_oper RPAREN'
    p[0] = ['(' + p[2][0] + ')', p[2][1]]

    if not esNumber(p[2][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_base_valor(p):
    'base : NUMBER'
    p[0] =  [toStrIfInt(p[1]), tipoNumber(p[1])] 

def p_base_func_ret_int(p):
    'base : func_ret_int'
    p[0] =  [p[1][0], p[1][1]] 

def p_sigexp_m(p):
    'sigexp : MINUS exp'
    p[0] = ['-' + p[2][0], p[2][1]]

def p_sigexp_exp(p):
    'sigexp : exp'
    p[0] =  [p[1][0], p[1][1]]

def p_exp_var_op(p):
    'exp : var_oper'
    p[0] =  [p[1][0], p[1][1]]

    if not esNumber(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_valor(p):
    'exp : NUMBER'
    p[0] =  [toStrIfInt(p[1]), tipoNumber(p[1])]

def p_exp__expr(p):
    'exp : LPAREN exp_arit RPAREN'
    p[0] = ['(' + p[2][0] + ')', p[2][1]]


#Producciones operaciones con Strings
def p_exp_cadena_concat(p):
    'exp_cadena : exp_cadena PLUS term_cadena'
    p[0] = [p[1][0] + ' + ' +  p[3][0], 'STRING']

def p_exp_cadena_concat_1(p):
    'exp_cadena : var_oper PLUS term_cadena'
    p[0] = [p[1][0] + ' + ' +  p[3][0], 'STRING']

    if not esString(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_cadena_concat_2(p):
    'exp_cadena : exp_cadena PLUS var_oper'
    p[0] = [p[1][0] + ' + ' +  p[3][0], 'STRING']

    if not esString(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_exp_cadena_term(p):
    'exp_cadena : term_cadena'
    p[0] = [p[1][0], 'STRING']

def p_exp_cadena_cadena(p):
    'term_cadena : CADENA'
    p[0] = [p[1], 'STRING' ]

def p_exp_cadena_funct_ret_string(p):
   'term_cadena : func_ret_cadena'
   p[0] =  [p[1][0], p[1][1]] 

def p_exp_cadena_parent(p):
    'term_cadena : LPAREN exp_cadena RPAREN'
    p[0] = ['(' + p[2][0] + ')', 'STRING']

#Producciones de operaciones booleanas

def p_bool_expr_eat(p):
    'exp_bool : exp_bool AND term_bool'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']


def p_bool_expr_v2af(p):
    'exp_bool : var_oper AND term_bool'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if not esBool(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_bool_expr_eav2(p):
    'exp_bool : exp_bool AND var_oper'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if not esBool(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_bool_expr_v2av2(p):
    'exp_bool : var_oper AND var_oper'
    p[0] = [p[1][0] + ' and ' + p[3][0], 'BOOL']

    if not esBool(p[3][1]) or not esBool(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_bool_expr_term(p):
    'exp_bool : term_bool'
    p[0] = [p[1][0], 'BOOL' ]

def p_bool_tof(p):
    'term_bool : term_bool OR factor_bool'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

def p_bool_tov2(p):
    'term_bool : term_bool OR var_oper'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if not esBool(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_bool_v2of(p):
    'term_bool : var_oper OR factor_bool'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if not esBool(p[1][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_bool_v2ov2(p):
    'term_bool : var_oper OR var_oper'
    p[0] = [p[1][0] + ' or ' + p[3][0], 'BOOL']

    if not esBool(p[1][1]) or not esBool(p[3][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))

def p_bool_term_factor(p):
    'term_bool : factor_bool'
    p[0] = [p[1][0], 'BOOL'] 

def p_term_not(p):
    'term_bool : NOT factor_bool'
    p[0] = ['not ' + p[2][0], 'BOOL']

def p_term_not_var_oper(p):
    'term_bool : NOT var_oper'
    p[0] = ['not ' + p[2][0], 'BOOL']

    if not esBool(p[2][1]):
        pass
        raise SemanticException('ERRORTIPO',p.lineno(1),p.lexpos(1))


def p_term_bool_parentesis(p):
    'factor_bool : LPAREN comparacion RPAREN'
    p[0] = ['(' + p[2][0] + ')', 'BOOL']

def p_term_bool_parentesis2(p):
    'factor_bool : LPAREN exp_bool RPAREN'
    p[0] = ['(' + p[2][0] + ')', 'BOOL']

def p_term_bool_bool(p):
    'factor_bool : BOOL'
    p[0] = [str(p[1]), 'BOOL']

def p_term_bool_func(p):
    'factor_bool : func_ret_bool'
    p[0] = [str(p[1][0]), 'BOOL']

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

def p_comparcion(p):
    'comparacion : valores operador_comp valores'
    p[0] = [p[1][0] + p[2][0] + p[3][0], 'BOOL']
    

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
