from lexer_rules import tokens
import ply.yacc as yacc

class ParserException(Exception):
        pass

#Producciones Generales
def p_sentencia_g_s(sentencia):
    'g : sentencia'
def p_sentencia_g_ctrl(sentencia):
    'g : control'
def p_sentencia_g_s_list(sentencia):
    'g : sentencia g'
def p_sentencia_g_ctrl_list(sentencia):
    'g : control g'
def p_sentencia_var_op(sentencia):
    'sentencia : var_ops PUNTOYCOMA'
def p_sentencia_func(p):
    'sentencia : funcion PUNTOYCOMA'
#Producciones para estructuras de control
def p_control_if(p):
    'control : if'
def p_control_loop(p):
    'control : loop'
def p_loop_while(p):
    'loop : WHILE LPAREN exp_bool RPAREN bloque '
def p_loop_do(p):
    'loop : DO bloque WHILE LPAREN exp_bool RPAREN PUNTOYCOMA'
def p_loop_for(p):
    'loop : FOR LPAREN var_asig PUNTOYCOMA exp_bool PUNTOYCOMA var_ops RPAREN bloque'
def p_if(p):
    'if : IF LPAREN exp_bool RPAREN THEN bloque ELSE bloque'
def p_bloque_s(p):
    'bloque : sentencia'
def p_bloque_g(p):
    'bloque : LLAVEIZQ g LLAVEDER'
#Producciones para funciones
def p_funcion_ret(p):
    'funcion : func_ret'
def p_funcion_void(p):
    'funcion : PRINT LPAREN valores RPAREN'
def p_funcion_ret_int(p):
    'func_ret : func_ret_int'
def p_funcion_ret_int_mult(p):
    'func_ret_int : MULTIPLICACIONESCALAR LPAREN vec COMA exp_mat COMA VARIABLE'
def p_funcion_ret_int_length(p):
    'func_ret_int : LENGTH'
def p_funcion_ret_string(p):
    'func_ret : CAPITALIZAR LPAREN exp_string RPAREN'
def p_funcion_ret_bool(p):
    'func_ret : COLINEALES LPAREN vec RPAREN '
#Producciones para vectores y variables
def p_vec(p):
    'vec : VARIABLE IGUAL LCORCHETE elem RCORCHETE'
def p_elem_list(p):
    'elem : valores COMA elem'
def p_elem(p):
    'elem : valores'
def p_vec_val(p):
    'vec_val : VARIABLE vec'
def p_var_y_vals_var(p):
    'var_y_vals : VARIABLE'
def p_var_y_vals_vec_val(p):
    'var_y_vals : vec_val'
def p_valores_exp_mat(p):
    'valores : exp_mat'
def p_valores_exp_string(p):
    'valores : exp_string'
def p_valores_exp_bool(p):
    'valores : exp_bool'
def p_valores_vyv(p):
    'valores : var_y_vals'
def p_valores_func_ret(p):
    'valores : func_ret'
#Producciones operaciones binarias con enteros
def p_exp_mat_pp(p):
    'exp_mat : exp_mat PLUS prod'
def p_exp_mat_mp(p):
    'exp_mat : exp_mat MINUS prod'
def p_exp_mat_p(p):
    'exp_mat : prod'
def p_prod_pe(p):
    'prod : prod MULTIPL exp'
def p_prod_de(p):
    'prod : prod DIV exp'
def p_prod_e(p):
    'prod : exp'
def p_exp_ei(p):
    'exp : exp ELEVADO ising'
def p_exp_i(p):
    'exp : ising'
def p_ising_mp(p):
    'ising : MINUS paren'
def p_ising_pp(p):
    'ising : PLUS paren'
def p_ising_p(p):
    'ising : paren'
def p_paren_c(p):
    'paren : LCORCHETE exp_mat RCORCHETE'
def p_paren_num(p):
    'paren : NUMBER'
def p_paren_vyv(p):
    'paren : var_y_vals'
def p_paren_var_ops(p):
    'paren : var_ops'
def p_paren_func_ret_int(p):
    'paren : func_ret_int'
#Producciones operaciones con Strings
def p_exp_string_concat(p):
    'exp_string : exp_string PLUS CADENA'
def p_exp_string_cadena(p):
    'exp_string : CADENA'
def p_exp_string_vyv(p):#?
    'exp_string : var_y_vals'
def p_exp_string_funct_ret_string(p):
    'exp_string : CAPITALIZAR LPAREN exp_string RPAREN'
#Producciones Registros
def p_reg(p):
    'reg : LLAVEIZQ reg_item LLAVEDER'
def p_reg_item_list(p):
    'reg_item : CADENA DOSPUNTOS valores COMA reg_item' 
def p_reg_item(p):
    'reg_item : CADENA DOSPUNTOS valores' 
#Producciones de operadores de variables
def p_var_ops_mm_smm(p):
    'var_ops : MINUS MINUS smm' 
def p_var_ops_pp_smm(p):
    'var_ops : PLUS PLUS smm' 
def p_var_ops_smm(p):
    'var_ops : smm' 
def p_smm_mm(p):
    'smm : var_y_vals MINUS MINUS'
def p_smm_pp(p):
    'smm : var_y_vals PLUS PLUS'
#Producciones de asignaciones
def p_var_asig_multipl(p):
    'var_asig : sigual MULTIPL valores'
def p_var_asig_dividi(p):
    'var_asig : sigual DIVIDI valores'
def p_var_asig_sigual(p):
    'var_asig : sigual'
def p_sigual_agregar(p):
    'sigual : asig AGREGAR'
def p_sigual_sacar(p):
    'sigual : asig SACAR'
def p_asig_var_val(p):
    'asig : VARIABLE IGUAL valores'
def p_asig_var_var(p):
    'asig : VARIABLE IGUAL VARIABLE'
#Producciones de operaciones booleanas
def p_exp_bool_true(p):
    'exp_bool : TRUE'
def p_exp_bool_false(p):
    'exp_bool : FALSE'
def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



