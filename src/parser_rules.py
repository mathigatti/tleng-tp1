from lexer_rules import tokens
import ply.yacc as yacc

def find_and_replace(palabra):
    j = 0
    res = ''
    for i in range(len(palabra)):
        if palabra[i] == '\n':
            res = res + palabra[j:i] + '\n    '
            j = i+1
    return res + palabra[j:]

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
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_programa_coment_pp(p):
    'p : COMENTARIO pp'
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_programa_ctl_p(p):
    'p : control p'
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_pp_s_pp(p):
    'pp : sentencia pp'
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_pp_ctl_pp(p):
    'pp : COMENTARIO pp'
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_pp_comentario_p(p):
    'pp : control p'
    p[0] = p[1] + '\n'  + p[2] + '\n'

def p_pp_lamda(p):
    'pp : '
    p[0] = ''

def p_sentencia_var_asig(p):
    'sentencia : var_asig PUNTOYCOMA'
    p[0] = p[1] + ';'

def p_sentencia_func(p):
    'sentencia : funcion PUNTOYCOMA'
    p[0] = p[1] + ';'

#Producciones para estructuras de control
def p_control_ifelse(p):
    'control : ifelse'
    p[0] = p[1]
def p_control_loop(p):
    'control : loop'
    p[0] = p[1]
def p_loop_while(p):
    'loop : WHILE LPAREN exp_bool RPAREN bloque'
    p[0] = 'while('+ p[3] + ')\n' + find_and_replace(p[5])
def p_loop_do(p):
    'loop : DO bloque WHILE LPAREN exp_bool RPAREN PUNTOYCOMA'
    p[0] = 'do\n' + find_and_replace(p[2]) + 'while(' + p[5] + ');' +')\n'

def p_loop_for(p):
    'loop : FOR LPAREN var_asig PUNTOYCOMA exp_bool PUNTOYCOMA exp_mat RPAREN bloque'
    p[0] = 'for(' + p[3] + ';' + p[5] + ';' + p[7] +')\n    ' + find_and_replace(p[9]) + '\n'

def p_ifelse(p):
    'ifelse : IF LPAREN exp_bool RPAREN THEN bloque ELSE bloque'
    p[0] = 'If(' + p[3] + ')\n    ' + find_and_replace(p[6]) + '\n else' + find_and_replace(p[8]) + '\n'


def p_bloque_s(p):
    'bloque : sentencia'
    p[0] = p[1]

def p_bloque_p(p):
    'bloque : LLAVEIZQ p LLAVEDER'
    p[0] = '{' + p[2] + '}'
#Produccion de Comentario
    'comentario : COMENTARIO '
    p[0] = p[1]
#Producciones para funciones
def p_funcion_ret(p):
    'funcion : func_ret'
    p[0] = p[1]
def p_funcion_void(p):
    'funcion : func_void '
    p[0] = p[1]
def p_func_void(p):
    'func_void : PRINT LPAREN valores RPAREN'
    p[0] = 'print(' + p[3] + ')'

def p_funcion_ret_int(p):
    'func_ret : func_ret_int'
    p[0] = p[1]
def p_funcion_ret_int_mult(p):
    'func_ret_int : MULTIPLICACIONESCALAR LPAREN VARIABLE COMA exp_mat COMA VARIABLE RPAREN'
    #Chequear que primer parametro es vector
    p[0] = 'multiplicacionEscalar(' + p[3] + ',' + p[5] + ',' + p[7] + ')'

def p_funcion_ret_int_length(p):
    'func_ret_int : LENGTH LPAREN VARIABLE RPAREN'
    #Verificar que VARIABLE sea cadena o vector
    p[0] = 'length(' + p[3] + ')'

def p_funcion_ret_string(p):
    'func_ret : CAPITALIZAR LPAREN exp_cadena RPAREN'
    p[0] = 'capitalizar(' + p[3] + ')'

def p_funcion_ret_bool(p):
    'func_ret : COLINEALES LPAREN VARIABLE COMA VARIABLE RPAREN '
    #verificar variables son  vector
    p[0] = 'colineales(' + p[3] + ',' + p[5] + ')'

#Producciones para vectores y variables
def p_valores_exp_mat(p):
    'valores : exp_mat'
    if isinstance( p[1], int ):
        p[0] = str(p[1])
    else:
        p[0] = p[1]

def p_valores_exp_bool(p):
    'valores : exp_bool'
    p[0] = p[1]

def p_valores_exp_cadena(p):
    'valores : exp_cadena'
    p[0] = p[1]

def p_valores_variables(p):
    'valores : VARIABLE'
    p[0] = p[1]

def p_valores_exp_arreglo(p):
    'valores : exp_arreglo'
    p[0] = p[1]

def p_valores_reg(p):
    'valores : reg'
    p[0] = p[1]

def p_exp_arreglo(p):
    'exp_arreglo : LCORCHETE valores exp_arreglo RCORCHETE'
    p[0] = '[' + p[2]  
    if isinstance( p[2], int ):
        p[0] += str(p[2])
    else:
        p[0] += p[2]
    p[0] +=' ' + p[3] + ']' 

def p_exp_arreglo_vacio(p):
    'exp_arreglo : LCORCHETE RCORCHETE'
    p[0] = '[]'   

def p_exp_arreglo_mult_escalar(p):
    'exp_arreglo : MULTIPLICACIONESCALAR LPAREN VARIABLE COMA exp_mat COMA VARIABLE RPAREN'
    #Chequear que primer parametro es vector
    p[0] = 'multiplicacionEscalar(' + p[3] + ',' + p[5] + ',' + p[7] + ')'

#Producciones Registros
def p_reg(p):
    'reg : LLAVEIZQ reg_item LLAVEDER'
    p[0] = '{' + p[1] + '}'

def p_reg_item_list(p):
    'reg_item : CADENA DOSPUNTOS valores COMA reg_item' 
    p[0] = p[1] + ":" + toStrIfInt(p[3]) + ',' + p[5]

def p_reg_item(p):
    'reg_item : CADENA DOSPUNTOS valores' 
    p[0] = p[1] + ":" + toStrIfInt(p[3])

#Producciones de asignaciones
def p_var_asig_multipl(p):
    'var_asig : VARIABLE MULTIPL valores'
    p[0] = p[1] + '*' + p[3]

def p_var_asig_dividi(p):
    'var_asig : VARIABLE DIVIDI valores'
    p[0] = p[1] + '/' + p[3]

def p_var_asig_sigual(p):
    'var_asig : VARIABLE'
    p[0] = p[1]

def p_var_asig_agregar(p):
    'var_asig : VARIABLE AGREGAR valores'
    p[0] = p[1] + '+=' + p[3]

def p_var_asig_sacar(p):
    'var_asig : VARIABLE SACAR valores'
    p[0] = p[1] + '+=' + p[3]

def p_var_asig(p):
    'var_asig : VARIABLE ASIGNACION valores'
    p[0] = p[1] + '=' + p[3]

def p_var_asig_vec1(p):
    'var_asig : VARIABLE LCORCHETE NUMBER RCORCHETE ASIGNACION valores'
    p[0] = p[1] + '[' + str(p[3]) +  '] =' + p[6]

def p_var_asig_vec2(p):
    'var_asig : VARIABLE LCORCHETE CADENA RCORCHETE ASIGNACION valores'
    p[0] = p[1] + '[' + p[3] +  '] =' + p[6]

def p_var_asig_reg(p):
    'var_asig : VARIABLE PUNTO VARIABLE ASIGNACION valores'
    p[0] = p[1] + '.' + p[3] +  ' = ' + p[5]

def p_var_asig_oper_ternario(p):
    'var_asig : VARIABLE ASIGNACION operador_ternario'
    p[0] = p[1] + '=' + p[3]

def p_operador_ternarioret_bool(p):
    'operador_ternario : LPAREN exp_bool RPAREN INTERROGACION exp_bool DOSPUNTOS exp_bool'
    p[0] = '(' + p[2] + ')? ' + p[5] + ':' + p[7] 

def p_operador_ternarioret_mat(p):
    'operador_ternario : LPAREN exp_bool RPAREN INTERROGACION exp_mat DOSPUNTOS exp_mat'
    p[0] = '(' + p[2] + ')? ' + p[5] + ':' + p[7] 
    if isinstance( p[5], int ):
        p[0] += str(p[5])
    else:
        p[0] += p[5]
    p[0] += ':'
    if isinstance( p[7], int ):
        p[0] += str(p[7])
    else:
        p[0] += p[7]

def p_operador_ternarioret_cadena(p):
    'operador_ternario : LPAREN exp_cadena RPAREN INTERROGACION exp_bool DOSPUNTOS exp_cadena'
    p[0] = '(' + p[2] + ')? ' + p[5] + ':' + p[7] 

#Producciones operaciones binarias con enteros
def p_exp_mat_ept(p):
    'exp_mat : exp_mat PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_mat_emt(p):
    'exp_mat : exp_mat MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_mat_term(p):
    'exp_mat : term'
    p[0] = toStrIfInt(p[1])

def p_term_tmf(p):
    'term : term MULTIPL factor'
    p[0] = p[1] + ' * ' + toStrIfInt(p[3])

def p_term_tdf(p):
    'term : term DIV factor'
    p[0] = p[1] + ' / ' + toStrIfInt(p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = toStrIfInt(p[1])

def p_factor_base_exp(p):
    'factor : base ELEVADO exp'
    p[0] = p[1] + ' ^ ' + toStrIfInt(p[3])

def p_factor_base(p):
    'factor : base '
    p[0] = toStrIfInt(p[1])

def p_base_expr(p):
    'base : LPAREN exp_mat RPAREN'
    p[0] = '(' + toStrIfInt(p[2]) + ')'

def p_base_valor(p):
    'base : NUMBER'
    #chequear que el valor sea numerico
    p[0] =  toStrIfInt(p[2]) 

def p_exp_valor(p):
    'exp : NUMBER'
    #chequear que el valor sea numerico
    p[0] =  toStrIfInt(p[2]) 

def p_exp__expr(p):
    'exp : LPAREN exp_mat RPAREN'
    p[0] = '(' + toStrIfInt(p[2]) + ')'


#Producciones operaciones con Strings
def p_exp_cadena_concat(p):
    'exp_cadena : exp_cadena PLUS term_cadena'
    p[0] = p[1] + ' + ' +  p[3]

def p_exp_cadena_term(p):
    'exp_cadena : term_cadena'
    p[0] = p[1] 

def p_exp_cadena_cadena(p):
    'term_cadena : CADENA'
    p[0] = p[1] 


def p_exp_cadena_funct_ret_string(p):
    'term_cadena : CAPITALIZAR LPAREN exp_cadena RPAREN'
    p[0] = 'capitalizar(' + p[1] + ')'

def p_exp_cadena_parent(p):
    'term_cadena : LPAREN exp_cadena RPAREN'
    p[0] = '(' + p[1] + ')'



#Producciones de operaciones booleanas
def p_bool_operator_and(p):
    'bool_operator : AND '
    p[0] = 'and'

def p_bool_operator_or(p):
    'bool_operator : OR'
    p[0] = 'or'

def p_bool_operator_igual(p):
    'bool_operator : IGUAL'
    p[0] = '=='

def p_bool_expr_oper(p):
    'exp_bool : exp_bool bool_operator term_bool'
    p[0] = p[1] + p[2] + p[3]

def p_bool_expr_term(p):
    'exp_bool : term_bool'
    p[0] = p[1] 

def p_term_bool_paren(p):
    'term_bool : LPAREN exp_bool RPAREN'
    p[0] = '(' + p[2] + ')'

def p_term_bool_bool(p):
    'term_bool : BOOL'
    p[0] = str(p[1])
    
def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



