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
    p[0] = p[1] + '\n'  + p[2]

def p_programa_coment_pp(p):
    'p : COMENTARIO p'
    p[0] = p[1] + '\n'  + p[2]

def p_programa_ctl_p(p):
    'p : control pp'
    p[0] = p[1] + '\n'  + p[2]

def p_pp_s_pp(p):
    'pp : sentencia pp'
    p[0] = p[1] + '\n'  + p[2]

def p_pp_ctl_pp(p):
    'pp : COMENTARIO pp'
    p[0] = p[1] + '\n'  + p[2]

def p_pp_comentario_p(p):
    'pp : control pp'
    p[0] = p[1] + '\n'  + p[2]

def p_pp_empty(p):
    'pp : empty'
    p[0] = p[1] 

def p_empty(p):
    'empty :'
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
    'loop : WHILE LPAREN valores RPAREN bloque'
    p[0] = 'while('+ p[3] + ')\n' + find_and_replace(p[5])

def p_loop_do(p):
    'loop : DO bloque WHILE LPAREN valores RPAREN PUNTOYCOMA'
    p[0] = 'do\n' + find_and_replace(p[2]) + 'while(' + p[5] + ');' +')\n'

def p_loop_for(p):
    'loop : FOR LPAREN var_asig PUNTOYCOMA valores PUNTOYCOMA exp_arit RPAREN bloque'
    p[0] = 'for(' + p[3] + ';' + p[5] + ';' + p[7] +')\n    ' + find_and_replace(p[9]) + '\n'

def p_ifelse(p):
    'ifelse : IF LPAREN valores RPAREN bloque ELSE bloque'
    p[0] = 'If(' + p[3] + ')\n    ' + find_and_replace(p[5]) + '\n else' + find_and_replace(p[7]) + '\n'

def p_ifSinElse(p):
    'ifelse : IF LPAREN valores RPAREN bloque'
    p[0] = 'If(' + p[3] + ')\n    ' + find_and_replace(p[5]) + '\n'

def p_bloque_s(p):
    'bloque : sentencia'
    p[0] = p[1]

def p_bloque_p(p):
    'bloque : LLAVEIZQ p LLAVEDER'
    p[0] = '{' + p[2] + '}'

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

def p_funcion_ret_cadena(p):
    'func_ret : func_ret_cadena'
    p[0] = p[1]

def p_funcion_ret_bool(p):
    'func_ret : func_ret_bool'
    p[0] = p[1]

def p_funcion_ret_arreglo(p):
    'func_ret : func_ret_arreglo'
    p[0] = p[1]

def p_funcion_ret_arreglo_3(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores COMA valores RPAREN'
    #Chequear que primer parametro es vector
    p[0] = 'multiplicacionEscalar(' + p[3] + ',' + p[5] + ',' + p[7] + ')'

def p_funcion_ret_arreglo_2(p):
    'func_ret_arreglo : MULTIPLICACIONESCALAR LPAREN valores COMA valores RPAREN'
    #Chequear que primer parametro es vector
    p[0] = 'multiplicacionEscalar(' + p[3] + ',' + p[5] + ')'

def p_funcion_ret_int_length(p):
    'func_ret_int : LENGTH LPAREN valores RPAREN'
    #Verificar que VARIABLE sea cadena o vector
    p[0] = 'length(' + p[3] + ')'

def p_funcion_ret_string(p):
    'func_ret_cadena : CAPITALIZAR LPAREN valores RPAREN'
    #validar parametro tipo cadena 
    p[0] = 'capitalizar(' + p[3] + ')'

def p_funcion_ret_bool_f(p):
    'func_ret_bool : COLINEALES LPAREN valores COMA valores RPAREN '
    #verificar valores son  vector
    p[0] = 'colineales(' + p[3] + ',' + p[5] + ')'

#Producciones para vectores y variables
def p_valores_exp_arit(p):
    'valores : exp_arit'
    p[0] = toStrIfInt(p[1])

def p_valores_exp_bool(p):
    'valores : exp_bool'
    p[0] = p[1]

def p_valores_exp_cadena(p):
    'valores : exp_cadena'
    p[0] = p[1]

def p_valores_exp_arreglo(p):
    'valores : exp_arreglo'
    p[0] = p[1]

def p_valores_reg(p):
    'valores : reg'
    p[0] = p[1]

def p_valores_variables(p):
    'valores : VARIABLE'
    p[0] = p[1]

def p_valores_suma_var(p):
    'valores : suma_var'
    p[0] = p[1]

def p_exp_arreglo(p):
    'exp_arreglo : LCORCHETE valores exp_arreglo RCORCHETE'
    p[0] = '[' + toStrIfInt(p[2]) + ' ' + toStrIfInt(p[3]) + ']'

def p_exp_arreglo_vacio(p):
    'exp_arreglo : LCORCHETE RCORCHETE'
    p[0] = '[]'   

def p_exp_arreglo_mult_escalar(p):
    'exp_arreglo : func_ret_arreglo'
    #Chequear que primer parametro es vector
    p[0] = p[1]

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
def p_var_asig_base_mm(p):
    'var_asig : VARIABLE LESSLESS'
    p[0] = toStrIfInt(p[1]) + '--'

def p_var_asig_mm_base(p):
    'var_asig : LESSLESS VARIABLE'
    p[0] = '--' + toStrIfInt(p[2])

def p_var_asig_base_pp(p):
    'var_asig : VARIABLE MASMAS'
    p[0] = toStrIfInt(p[1]) + '++'

def p_var_asig_pp_base(p):
    'var_asig : MASMAS VARIABLE '
    p[0] = '++' + toStrIfInt(p[2])

def p_var_asig_multipl(p):
    'var_asig : VARIABLE MULTIPL valores'
    p[0] = p[1] + '=*' + toStrIfInt(p[3])

def p_var_asig_dividi(p):
    'var_asig : VARIABLE DIVIDI valores'
    p[0] = p[1] + '=/' + toStrIfInt(p[3])

def p_var_asig_sigual(p):
    'var_asig : VARIABLE'
    p[0] = p[1]

def p_var_asig_agregar(p):
    'var_asig : VARIABLE AGREGAR valores'
    p[0] = p[1] + '+=' + toStrIfInt(p[3])

def p_var_asig_sacar(p):
    'var_asig : VARIABLE SACAR valores'
    p[0] = p[1] + '-=' + toStrIfInt(p[3])

def p_var_asig(p):
    'var_asig : VARIABLE ASIGNACION valores'
    p[0] = p[1] + '=' + toStrIfInt(p[3])

def p_var_asig_vec1(p):
    'var_asig : VARIABLE LCORCHETE NUMBER RCORCHETE ASIGNACION valores'
    p[0] = p[1] + '[' + str(p[3]) +  '] =' + p[6]

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
    'operador_ternario : LPAREN exp_bool RPAREN INTERROGACION exp_arit DOSPUNTOS exp_arit'
    p[0] = '(' + p[2] + ')? ' + toStrIfInt(p[5]) + ':' + p[7] 

def p_operador_ternarioret_cadena(p):
    'operador_ternario : LPAREN exp_cadena RPAREN INTERROGACION exp_bool DOSPUNTOS exp_cadena'
    p[0] = '(' + p[2] + ')? ' + p[5] + ':' + p[7] 

def p_suma_var_1(p):
    'suma_var : VARIABLE PLUS VARIABLE'
    p[0] = p[1] + ' + ' + p[3]

def p_suma_var_2(p):
    'suma_var : suma_var PLUS VARIABLE'
    p[0] = p[1] + ' + ' + p[3]

#Producciones operaciones binarias con enteros
def p_exp_arit_ept(p):
    'exp_arit : exp_arit PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_epv(p):
    'exp_arit : exp_arit PLUS VARIABLE'
    p[0] = p[1] + ' + ' + p[3]

def p_exp_arit_vps(p):
    'exp_arit : exp_arit PLUS suma_var'
    p[0] = p[1] + ' + ' + p[3]

def p_exp_arit_vpt(p):
    'exp_arit : VARIABLE PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_emt(p):
    'exp_arit : exp_arit MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_emv(p):
    'exp_arit : exp_arit MINUS VARIABLE'
    p[0] = p[1] + ' - ' + p[3]

def p_exp_arit_vmt(p):
    'exp_arit : VARIABLE MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_vmv(p):
    'exp_arit : VARIABLE MINUS VARIABLE'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_term(p):
    'exp_arit : term'
    p[0] = toStrIfInt(p[1])

def p_term_tmf(p):
    'term : term TIMES factor'
    p[0] = p[1] + ' * ' + toStrIfInt(p[3])

def p_term_tmv(p):
    'term : term TIMES VARIABLE'
    p[0] = p[1] + ' * ' + p[3]

def p_term_vmf(p):
    'term : VARIABLE  TIMES factor'
    p[0] = p[1] + ' * ' + toStrIfInt(p[3])

def p_term_vmv(p):
    'term : VARIABLE TIMES VARIABLE'
    p[0] = p[1] + ' * ' + p[3]

def p_term_tdf(p):
    'term : term DIV factor'
    p[0] = p[1] + ' / ' + toStrIfInt(p[3])

def p_term_tdv(p):
    'term : term DIV VARIABLE'
    p[0] = p[1] + ' / ' + p[3]

def p_term_vdf(p):
    'term : VARIABLE DIV factor'
    p[0] = p[1] + ' / ' + toStrIfInt(p[3])

def p_term_vdv(p):
    'term : VARIABLE DIV VARIABLE'
    p[0] = p[1] + ' / ' + p[3]

def p_term_tmodf(p):
    'term : term MODULO factor'
    p[0] = p[1] + ' % ' + toStrIfInt(p[3])

def p_term_tmodv(p):
    'term : term MODULO VARIABLE'
    p[0] = p[1] + ' % ' + p[3]

def p_term_vmodf(p):
    'term : VARIABLE MODULO factor'
    p[0] = p[1] + ' % ' + toStrIfInt(p[3])

def p_term_vmodv(p):
    'term : VARIABLE MODULO VARIABLE'
    p[0] = p[1] + ' % ' + p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = toStrIfInt(p[1])

def p_factor_base_exp(p):
    'factor : base ELEVADO sigexp'
    p[0] = p[1] + ' ^' + toStrIfInt(p[3])

def p_factor_base(p):
    'factor : base '
    p[0] = toStrIfInt(p[1])

def p_factor_m_base(p):
    'factor : MINUS base '
    p[0] = '-' + toStrIfInt(p[2])

def p_factor_base_mm(p):
    'factor : base LESSLESS'
    p[0] = toStrIfInt(p[1]) + '--'

def p_factor_mm_base(p):
    'factor : LESSLESS base '
    p[0] = '--' + toStrIfInt(p[2])

def p_factor_base_pp(p):
    'factor : base MASMAS'
    p[0] = toStrIfInt(p[1]) + '++'

def p_factor_pp_base(p):
    'factor : MASMAS base '
    p[0] = '++' + toStrIfInt(p[2])

def p_base_expr(p):
    'base : LPAREN exp_arit RPAREN'
    p[0] = '(' + toStrIfInt(p[2]) + ')'

def p_base_valor(p):
    'base : NUMBER'
    #chequear que el valor sea numerico
    p[0] =  toStrIfInt(p[1]) 

#def p_base_var(p):
#    'base : VARIABLE'
    #chequear que el valor sea numerico
#    p[0] =  p[1] 

def p_sigexp_m(p):
    'sigexp : MINUS exp'
    p[0] = '-' + p[2]

def p_sigexp_exp(p):
    'sigexp : exp'
    p[0] = toStrIfInt(p[1])

def p_exp_var(p):
    'exp : VARIABLE'
    #chequear que el valor sea numerico
    p[0] =  p[1] 

def p_exp_valor(p):
    'exp : NUMBER'
    #chequear que el valor sea numerico
    p[0] =  toStrIfInt(p[1]) 

def p_exp__expr(p):
    'exp : LPAREN exp_arit RPAREN'
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

def p_bool_expr_comparacion(p):
    'exp_bool : comparacion'
    p[0] = p[1] 

def p_bool_expr_term(p):
    'exp_bool : term_bool'
    p[0] = p[1] 

def p_bool_expr_not_term(p):
    'exp_bool : NOT term_bool'
    p[0] = 'not ' +  p[2] 

def p_term_bool_paren(p):
    'term_bool : LPAREN exp_bool RPAREN'
    p[0] = '(' + p[2] + ')'

#def p_term_bool_var(p):
#    'term_bool : VARIABLE'
#    p[0] = str(p[1])

def p_term_bool_bool(p):
    'term_bool : BOOL'
    p[0] = str(p[1])

def p_operador_comparacion_igual(p):
    'comparacion : IGUAL'
    p[0] = ' == '

def p_operador_comparacion_mayor(p):
    'operador_comp : MAYOR'
    p[0] = ' > '

def p_operador_comparacion_menor(p):
    'operador_comp : MENOR'
    p[0] = ' < '

def p_operador_comparacion_dif(p):
    'operador_comp : DISTINTO'
    p[0] = ' != '

def p_comparcion_cadenas(p):
    'comparacion : exp_cadena operador_comp exp_cadena'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_exp_arit(p):
    'comparacion : exp_arit operador_comp exp_arit'
    p[0] = toStrIfInt(p[1]) + p[2] + toStrIfInt(p[3])

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



