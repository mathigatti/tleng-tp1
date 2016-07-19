
semantic_errors =  {
        'INDEX_NOT_NAT' : 'El indice del vector debe ser un numero natural',
        'MATH_ERROR' : 'No esta definida esa operacion matematica',
        'CAPITALIZAR' : 'Argumentos incorrectos, Capitalizar(STRING)',
        'MULTIPLICACIONESCALAR' : 'Argumentos incorrectos, multiplicacionEscalar(VECTOR[NUMBER],NUMBER, BOOL (opcional)]',
        'COLINEALES' : 'Argumentos incorrectos, colineales(VECTOR[NUMBER],VECTOR[NUMBER])',
        'PRINT' : 'Argumentos incorrectos, la funcion print recibe solo un argumento',
        'LENGTH' : 'Argumentos incorrectos, length(STRING) o length(VECTOR)',
        'LISTAINCORRECTA' : 'El vector debe tener todos sus elementos del mismo tipo',
        'OPTERNARIO' : 'El operador ternario debe devolver en ambos casos un elemento del mismo tipo y tener una guarda de tipo BOOL',
        'COMPINVALIDA' : 'Comparacion invalida, error de tipos.',
        'ERRORTIPO' : 'Operacion invalida, error de tipos.',
        'NODEFINIDA' : 'Variable no definida.',
        'REGISTRO' : 'Esta intentando acceder a un valor que no esta en el registro.',
        'LOOP' : 'Error en un ciclo. La guarda no es de tipo BOOL',
        'IF' : 'Error en un IF. La guarda no es de tipo BOOL',
        }

class SemanticException(Exception):
    def __init__(self,msg_id,lineno,lexpos):
        super(SemanticException,self).__init__('Error semantico en la linea ' + str(lineno) + ' posicion ' + str(lexpos) + ". " + semantic_errors.get(msg_id))
