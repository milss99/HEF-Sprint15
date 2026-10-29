'''VALIDAÇÃO POST PEDIDO CLIENTE'''
def validar_nome(nome):
    if len(nome) < 3:
        return {"valida": False, "mensagem": "O nome deve ter pelo menos 3 letras!"}

    possui_numero = True
    for caractere in nome:
        if caractere.isdigit():
            possui_numero = False
            
    if not possui_numero:
        return {"valida": False, "mensagem": "O nome não deve possuir números!"}
    
    contem_espaco = False
    for caractere in nome:
        if caractere.isspace():
            contem_espaco = True
            print("ate aqui")
        
    if not contem_espaco:
        return {"valida": False, "mensagem": "O nome deve conter pelo menos um espaço"}


    return {"valida": True, "mensagem": "Nome válido!!"}

def validar_cpf(cpf):
    print(cpf)
    if len(cpf) < 11:
        return {"valida": False, "mensagem": "CPF inválido!"}

    possui_letra = True
    for caractere in cpf:
        if caractere.isalpha():
            possui_letra = False
        if not possui_letra:
            return {"valida": False, "Mensagem": "Não deve possuir letra!"}

    possui_espaco = True
    for caractere in cpf:
        if caractere.isspace():
            possui_espaco = False
        if not possui_espaco:
            return {"valida": False, "Mensagem": "Não deve possuir espaço!"}
    
    return {"valida": True, "mensagem": "cpf válido!!"}