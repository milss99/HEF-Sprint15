from models.clientes import Cliente
def validar(dados):
    print("contagem dados recebidos: ", len(dados))#só pra conferir
    if len(dados) >= 1 :
        return {"mensagem": "feito"}
    return
    
def non_negative(value, field_name):
        try:
            if float(value) < 0:
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None

#>>>>>>>>>>>>VALIDAÇÃO - CLIENTE<<<<<<<<<<<<

#cnpj

def validar_cnpj(cnpj_cliente):
    print(cnpj_cliente)
    if len(cnpj_cliente) < 14:
        return { "CNPJ inválido!"}
        print (f" {e} CNPJ inválido")

    possui_letra = True
    for caractere in cnpj_cliente:
        if caractere.isalpha():
            possui_letra = False
        if not possui_letra:
            print("tem letra")
        return {" CNPJ Não deve possuir letra!"}
           

    possui_espaco = True
    for caractere in cnpj_cliente:
        if caractere.isspace():
            possui_espaco = False
        if not possui_espaco:
            print("tem espaco")
            return {"CNPJ Não deve possuir espaço!"}

    print("valido")
    return {"cnpj válido!!"}
