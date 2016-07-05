from lexer_rules import tokens
import ply.yacc as yacc

class ParserException(Exception):
        pass

#Producciones Generales
def p_sentencia_g_s(self,sentencia):
    'g : sentencia'
def p_sentencia_g_ctrl(self,sentencia):
    'g : control'
def p_sentencia_g_s_list(self,sentencia):
    'g : sentencia g'
def p_sentencia_g_ctrl_list(self,sentencia):
    'g : control g'
def p_sentencia_var_op(self,sentencia):
    'sentencia : var_ops PUNTOYCOMA'
def p_sentencia_func(self,p):
    'sentencia : funcion PUNTOYCOMA'
#Producciones para estructuras de control
def p_control_if(self,p):
    'control : if'
def p_control_loop(self,p):
    'control : loop'
def p_loop_while(self,p):
    'loop : WHILE LPAREN exp_bool RPAREN bloque '
def p_loop_do(self,p):
    'loop : DO bloque WHILE LPAREN exp_bool RPAREN PUNTOYCOMA'
def p_loop_for(self,p):
    'loop : FOR LPAREN var_asig PUNTOYCOMA exp_bool PUNTOYCOMA var_ops RPAREN bloque'
def p_if(self,p):
    'if : IF LPAREN exp_bool RPAREN THEN bloque ELSE bloque'
def p_bloque_s(self,p):
    'bloque : sentencia'
def p_bloque_g(self,p):
    'bloque : LLAVEIZQ g LLAVEDER'
#Producciones para funciones
def p_funcion_ret(self,p):
    'funcion : func_ret'
def p_funcion_void(self,p):
    'funcion : PRINT LPAREN valores RPAREN'
def p_funcion_ret_int(self,p):
    'func_ret : func_ret_int'
def p_funcion_ret_int_mult(self,p):
    'func_ret_int : MULTIPLICACIONESCALAR LPAREN vec COMA exp_mat COMA VARIABLE'
def p_funcion_ret_int_length(self,p):
    'func_ret_int : LENGTH'
def p_funcion_ret_string(self,p):
    'func_ret : CAPITALIZAR LPAREN exp_string RPAREN'
def p_funcion_ret_bool(self,p):
    'func_ret : COLINEALES LPAREN vec RPAREN '
#Producciones para vectores y variables
def p_vec(self,p):
    'vec : VARIABLE IGUAL LCORCHETE elem RCORCHETE'
def p_elem_list(self,p):
    'elem : valores COMA elem'
def p_elem(self,p):
    'elem : valores'
def p_vec_val(self,p):
    'vec_val : VARIABLE vec'
def p_var_y_vals_var(self,p):
    'var_y_vals : VARIABLE'
def p_var_y_vals_vec_val(self,p):
    'var_y_vals : vec_val'
def p_valores_exp_mat(self,p):
    'valores : exp_mat'
def p_valores_exp_string(self,p):
    'valores : exp_string'
def p_valores_exp_bool(self,p):
    'valores : exp_bool'
def p_valores_vyv(self,p):
    'valores : var_y_vals'
def p_valores_func_ret(self,p):
    'valores : func_ret'
#Producciones operaciones binarias con enteros
def p_exp_mat_pp(self,p):
    'exp_mat : exp_mat PLUS prod'
def p_exp_mat_mp(self,p):
    'exp_mat : exp_mat MINUS prod'
def p_exp_mat_p(self,p):
    'exp_mat : prod'
def p_prod_pe(self,p):
    'prod : prod MULTIPL exp'
def p_prod_de(self,p):
    'prod : prod DIV exp'
def p_prod_e(self,p):
    'prod : exp'
def p_exp_ei(self,p):
    'exp : exp ELEVADO ising'
def p_exp_i(self,p):
    'exp : ising'
def p_ising_mp(self,p):
    'ising : MINUS paren'
def p_ising_pp(self,p):
    'ising : PLUS paren'
def p_ising_p(self,p):
    'ising : paren'
def p_paren_c(self,p):
    'paren : LCORCHETE exp_mat RCORCHETE'
def p_paren_num(self,p):
    'paren : NUMBER'
def p_paren_vyv(self,p):
    'paren : var_y_vals'
def p_paren_var_ops(self,p):
    'paren : var_ops'
def p_paren_func_ret_int(self,p):
    'paren : func_ret_int'
#Producciones operaciones con Strings
def p_exp_string_concat(self,p):
    'exp_string : exp_string PLUS CADENA'
def p_exp_string_cadena(self,p):
    'exp_string : CADENA'
def p_exp_string_vyv(self,p):#?
    'exp_string : var_y_vals'
def p_exp_string_funct_ret_string(self,p):
    'exp_string : CAPITALIZAR LPAREN exp_string RPAREN'
#Producciones Registros
def p_reg(self,p):
    'reg : LLAVEIZQ reg_item LLAVEDER'
def p_reg_item_list(self,p):
    'reg_item : CADENA DOSPUNTOS valores COMA reg_item' 
def p_reg_item(self,p):
    'reg_item : CADENA DOSPUNTOS valores' 
#Producciones de operadores de variables
def p_var_ops_mm_smm(self,p):
    'var_ops : MINUS MINUS smm' 
def p_var_ops_pp_smm(self,p):
    'var_ops : PLUS PLUS smm' 
def p_var_ops_smm(self,p):
    'var_ops : smm' 
def p_smm_mm(self,p):
    'smm : var_y_vals MINUS MINUS'
def p_smm_pp(self,p):
    'smm : var_y_vals PLUS PLUS'
#Producciones de asignaciones
def p_var_asig_multipl(self,p):
    'var_asig : sigual MULTIPL valores'
def p_var_asig_dividi(self,p):
    'var_asig : sigual DIVIDI valores'
def p_var_asig_sigual(self,p):
    'var_asig : sigual'
def p_sigual_agregar(self,p):
    'sigual : asig AGREGAR'
def p_sigual_sacar(self,p):
    'sigual : asig SACAR'
def p_asig_var_val(self,p):
    'asig : VARIABLE IGUAL valores'
def p_asig_var_var(self,p):
    'asig : VARIABLE IGUAL VARIABLE'
#Producciones de operaciones booleanas
def p_exp_bool_true(self,p):
    'exp_bool : TRUE'
def p_exp_bool_false(self,p):
    'exp_bool : FALSE'
def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)



