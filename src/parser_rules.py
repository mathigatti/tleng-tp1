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

def p_bloque_cb(p):
    'bloque : COMENTARIO bloque'
    p[0] = p[1]

def p_bloque_s(p):
    'bloque : sentencia'
    p[0] = p[1]

def p_bloque_c(p):
    'bloque : control'
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
    'valores : comparacion'
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
    'valores : var_asig_l'
    p[0] = p[1]

def p_exp_arreglo(p):
    'exp_arreglo : LCORCHETE lista_valores RCORCHETE'
    p[0] = '[' + toStrIfInt(p[2]) +  ']'

def p_exp_arreglo_vacio(p):
    'exp_arreglo : LCORCHETE RCORCHETE'
    p[0] = '[]'   

def p_exp_arreglo_mult_escalar(p):
    'exp_arreglo : func_ret_arreglo'
    #Chequear que primer parametro es vector
    p[0] = p[1]

def p_lista_valores_end(p):
    'lista_valores : valores'
    p[0] = p[1]

def p_lista_valores_lista(p):
    'lista_valores : valores COMA lista_valores'
    p[0] = p[1] + ',' + p[3] 


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
def p_var_asig_l_var(p):
    'var_asig_l : VARIABLE'
    p[0] = p[1]

def p_var_asig_l_res(p):
    'var_asig_l : RES'
    p[0] = p[1]

def p_var_asig_l_vec(p):
    'var_asig_l : VARIABLE LCORCHETE exp_arit RCORCHETE'
    p[0] = p[1] + '[' + str(p[3]) +  ']'

def p_var_asig_l_vec1(p):
    'var_asig_l : VARIABLE LCORCHETE VARIABLE RCORCHETE'
    #Chequear tipo de variable sea NAT
    p[0] = p[1] + '[' + p[3] +  ']'

def p_var_asig_l_reg(p):
    'var_asig_l : VARIABLE PUNTO VARIABLE'
    p[0] = p[1] + '.' + p[3] 

def p_var_asig_base_mm(p):
    'var_asig : var_asig_l LESSLESS'
    p[0] = toStrIfInt(p[1]) + '--'

def p_var_asig_mm_base(p):
    'var_asig : LESSLESS var_asig_l'
    p[0] = '--' + toStrIfInt(p[2])

def p_var_asig_base_pp(p):
    'var_asig : var_asig_l MASMAS'
    p[0] = toStrIfInt(p[1]) + '++'

def p_var_asig_pp_base(p):
    'var_asig : MASMAS var_asig_l '
    p[0] = '++' + toStrIfInt(p[2])

def p_var_asig_multipl(p):
    'var_asig : var_asig_l MULTIPL valores'
    p[0] = p[1] + '=*' + toStrIfInt(p[3])

def p_var_asig_dividi(p):
    'var_asig : var_asig_l DIVIDI valores'
    p[0] = p[1] + '=/' + toStrIfInt(p[3])

#def p_var_asig_sigual(p):
#    'var_asig : VARIABLE'
#    p[0] = p[1]

def p_var_asig_agregar(p):
    'var_asig : var_asig_l AGREGAR valores'
    p[0] = p[1] + '+=' + toStrIfInt(p[3])

def p_var_asig_sacar(p):
    'var_asig : var_asig_l SACAR valores'
    p[0] = p[1] + '-=' + toStrIfInt(p[3])

def p_var_asig(p):
    'var_asig : var_asig_l ASIGNACION valores'
    p[0] = p[1] + '=' + toStrIfInt(p[3])

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



def p_oper_var_reg(p):
    'var_oper : VARIABLE PUNTO  VARIABLE'
    p[0] = p[1] + '.' + p[3]

def p_oper_var_vec(p):
    'var_oper : VARIABLE LCORCHETE VARIABLE RCORCHETE'
    p[0] = p[1] + '[' + p[3] + ']'

def p_oper_var_vec2(p):
    'var_oper : VARIABLE LCORCHETE exp_arit RCORCHETE'
    p[0] = p[1] + '[' + p[3] + ']'


#Producciones operaciones binarias con enteros
def p_exp_arit_ept(p):
    'exp_arit : exp_arit PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_epv(p):
    'exp_arit : exp_arit PLUS VARIABLE'
    p[0] = p[1] + ' + ' + p[3]

def p_exp_arit_epv2(p):
    'exp_arit : exp_arit PLUS var_oper'
    p[0] = p[1] + ' + ' + p[3]

def p_exp_arit_vpt(p):
    'exp_arit : VARIABLE PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_v2pt(p):
    'exp_arit : var_oper PLUS term'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_vpv(p):
    'exp_arit : VARIABLE PLUS VARIABLE'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_v2pv2(p):
    'exp_arit : var_oper PLUS var_oper'
    p[0] = p[1] + ' + ' + toStrIfInt(p[3])

def p_exp_arit_emt(p):
    'exp_arit : exp_arit MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_emv(p):
    'exp_arit : exp_arit MINUS VARIABLE'
    p[0] = p[1] + ' - ' + p[3]

def p_exp_arit_emv2(p):
    'exp_arit : exp_arit MINUS var_oper'
    p[0] = p[1] + ' - ' + p[3]

def p_exp_arit_vmt(p):
    'exp_arit : VARIABLE MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_v2mt(p):
    'exp_arit : var_oper MINUS term'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_vmv(p):
    'exp_arit : VARIABLE MINUS VARIABLE'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_v2mv2(p):
    'exp_arit : var_oper MINUS var_oper'
    p[0] = p[1] + ' - ' + toStrIfInt(p[3])

def p_exp_arit_term(p):
    'exp_arit : term'
    p[0] = toStrIfInt(p[1])

def p_arit_oper2_times(p):
    'arit_oper_2 : TIMES'

def p_arit_oper2_div(p):
    'arit_oper_2 : DIV'

def p_arit_oper2_mod(p):
    'arit_oper_2 : MODULO'

def p_term_tmf(p):
    'term : term arit_oper_2 factor'
    p[0] = p[1] + p[2] + toStrIfInt(p[3])

def p_term_tmv(p):
    'term : term arit_oper_2 VARIABLE'
    p[0] = p[1] + ' * ' + p[3]

def p_term_tmv2(p):
    'term : term arit_oper_2 var_oper'
    p[0] = p[1] + ' * ' + p[3]

def p_term_vmf(p):
    'term : VARIABLE  arit_oper_2 factor'
    p[0] = p[1] + ' * ' + toStrIfInt(p[3])

def p_term_v2mf(p):
    'term : var_oper arit_oper_2 factor'
    p[0] = p[1] + ' * ' + toStrIfInt(p[3])

def p_term_vmv(p):
    'term : VARIABLE arit_oper_2 VARIABLE'
    p[0] = p[1] + ' * ' + p[3]

def p_term_v2mv2(p):
    'term : var_oper arit_oper_2 var_oper'
    p[0] = p[1] + ' * ' + p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = toStrIfInt(p[1])

def p_factor_base_exp(p):
    'factor : base ELEVADO sigexp'
    p[0] = p[1] + ' ^' + toStrIfInt(p[3])

def p_factor_base_exp(p):
    'factor : VARIABLE ELEVADO sigexp'
    p[0] = p[1] + ' ^' + toStrIfInt(p[3])

def p_factor_base_exp(p):
    'factor : var_oper ELEVADO sigexp'
    p[0] = p[1] + ' ^' + toStrIfInt(p[3])

def p_factor_base(p):
    'factor : base '
    p[0] = toStrIfInt(p[1])

def p_factor_m_base(p):
    'factor : MINUS base '
    p[0] = '-' + toStrIfInt(p[2])

def p_factor_var_mm(p):
    'factor : VARIABLE LESSLESS'
    p[0] = toStrIfInt(p[1]) + '--'

def p_factor_base_mm(p):
    'factor : base LESSLESS'
    p[0] = toStrIfInt(p[1]) + '--'

def p_factor_mm_var(p):
    'factor : LESSLESS VARIABLE'
    p[0] = '--' + toStrIfInt(p[2])

def p_factor_mm_base(p):
    'factor : LESSLESS base '
    p[0] = '--' + toStrIfInt(p[2])

def p_factor_var_pp(p):
    'factor : VARIABLE MASMAS'
    p[0] = toStrIfInt(p[1]) + '++'

def p_factor_base_pp(p):
    'factor : base MASMAS'
    p[0] = toStrIfInt(p[1]) + '++'

def p_factor_pp_var(p):
    'factor : MASMAS VARIABLE'
    p[0] = '++' + toStrIfInt(p[2])

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

def p_base_func_ret_int(p):
    'base : func_ret_int'
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

def p_exp_var(p):
    'exp : var_oper'
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

def p_exp_cadena_concat_1(p):
    'exp_cadena : VARIABLE PLUS term_cadena'
    p[0] = p[1] + ' + ' +  p[3]

def p_exp_cadena_concat_2(p):
    'exp_cadena : exp_cadena PLUS VARIABLE'
    p[0] = p[1] + ' + ' +  p[3]

def p_exp_cadena_term(p):
    'exp_cadena : term_cadena'
    p[0] = p[1] 

def p_exp_cadena_cadena(p):
    'term_cadena : CADENA'
    p[0] = p[1] 


def p_exp_cadena_funct_ret_string(p):
    'term_cadena : CAPITALIZAR LPAREN valores RPAREN'
    p[0] = 'capitalizar(' + p[1] + ')'

def p_exp_cadena_parent(p):
    'term_cadena : LPAREN exp_cadena RPAREN'
    p[0] = '(' + p[1] + ')'



#Producciones de operaciones booleanas
def p_comparacionarision_igual(p):
    'comparacion : comparacion IGUAL exp_bool'
    p[0] = p[1] + ' == ' + p[3]

def p_comparacionarision_dis(p):
    'comparacion : comparacion DISTINTO exp_bool'
    p[0] = p[1] + ' != ' + p[3]

def p_comparacionarision_bool_exp(p):
    'comparacion : exp_bool'
    p[0] = p[1]  

def p_bool_expr_eat(p):
    'exp_bool : exp_bool AND term_bool'
    p[0] = p[1] + ' and '  + p[3]

def p_bool_expr_vaf(p):
    'exp_bool : VARIABLE AND term_bool'
    p[0] = p[1] + ' and '  + p[3]

def p_bool_expr_eav(p):
    'exp_bool : exp_bool AND VARIABLE'
    p[0] = p[1] + ' and '  + p[3]

def p_bool_expr_vav(p):
    'exp_bool : VARIABLE AND VARIABLE'
    p[0] = p[1] + ' and '  + p[3]

def p_bool_expr_term(p):
    'exp_bool : term_bool'
    p[0] = p[1] 

def p_bool_tof(p):
    'term_bool : term_bool OR factor_bool'
    p[0] = p[1] + ' or ' + p[3]

def p_bool_tov(p):
    'term_bool : term_bool OR VARIABLE'
    p[0] = p[1] + ' or ' + p[3]

def p_bool_vof(p):
    'term_bool : VARIABLE OR factor_bool'
    p[0] = p[1] + ' or ' + p[3]

def p_bool_vov(p):
    'term_bool : VARIABLE OR VARIABLE'
    p[0] = p[1] + ' or ' + p[3]

def p_bool_term_factor(p):
    'term_bool : factor_bool'
    p[0] = p[1] 

#def p_term_bool_var(p):
#    'term_bool : VARIABLE'
#    p[0] = str(p[1])

def p_term_bool_bool(p):
    'factor_bool : BOOL'
    p[0] = str(p[1])

def p_term_bool_func(p):
    'factor_bool : func_ret_bool'
    p[0] = str(p[1])

#def p_bool_expr_comparacion(p):
#    'factor_bool : comparacion'
#    p[0] = p[1] 

def p_operador_comparacion_igual(p):
    'operador_comp : IGUAL'
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

def p_comparcion_exp_arit(p):
    'comparacion : exp_arit operador_comp exp_arit'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_acv(p):
    'comparacion : exp_arit operador_comp VARIABLE'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_vca(p):
    'comparacion : VARIABLE operador_comp exp_arit'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_exp_cadena(p):
    'comparacion : exp_cadena operador_comp exp_cadena'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_exp_vcc(p):
    'comparacion : VARIABLE operador_comp exp_cadena'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_exp_ccv(p):
    'comparacion : exp_cadena operador_comp VARIABLE'
    p[0] = p[1] + p[2] + p[3]

def p_comparcion_exp_vcv(p):
    'comparacion : VARIABLE operador_comp VARIABLE'
    p[0] = p[1] + p[2] + p[3]




def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



