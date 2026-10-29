class val:
    
    @staticmethod
    def valid(value, field,id):
        try:
            if id == len(field):
                return f" {id}, {field}, {value}"
        except (TypeError, ValueError):
            return f"O id {id} não corresponde a tabela "
        return None