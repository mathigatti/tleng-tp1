
semantic_errors =  {
        'INDEX_NOT_NAT' : 'Vector index must be a natural number'
        }

class SemanticException(Exception):
    def __init__(self,msg_id,lineno):
        super(SemanticException,self).__init__('Semantic Error:' + str(lineno) + ":" + semantic_errors.get(msg_id))
