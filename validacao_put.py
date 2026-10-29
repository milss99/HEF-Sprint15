import re

def atualizar_prod (indice, dados, livro):
    livro[indice].update(dados)

def atualizar_cliente (indice,info,cliente):
    cliente[indice].update(info)

def atualizar_fornecedor (indice, att, fornecedor):
    fornecedor[indice].update(att)

def atualizar_itens (indice, att, itens):
    itens[indice].update(att)

def atualizar_producao (indice, att, processo):
    processo[indice].update(att)

def atualizar_materiais (indice, att, materiais):
    materiais[indice].update(att)

def atualizar_pagamentos (indice, att, pagamento):
    pagamento[indice].update(att)

def atualizar_funcionarios (indice, att, funcionarios):
    funcionarios[indice].update(att)

def atualizar_pedidocliente (indice, att, ped_clientes):
   ped_clientes[indice].update(att)

def atualizar_pedido_fornecedor (indice, dados, pedido_fornecedor):
    pedido_fornecedor[indice].update(dados)

"""--10/03--"""
def atualizar_oque_vai (indice, att, oque_vai):
   oque_vai[indice].update(att)

def atualizar_item_pedido (indice, att, item_pedido):
   item_pedido[indice].update(att)



#VALIDAÇÕES

import urllib.parse
import requests

def extcep(api, token):#manda para verifição pela api

    print("valor dos dados: ", ipa)#só para testar
    base_url = "https://api.invertexto.com/v1/cep"
    #codifica o cep para garantir que a URL fique correta
    cep_encoded = urllib.parse.quote(ipa)
    #Monta a URL com o cep na rota
    url = f"{base_url}/{cep_encoded}"
    #parâmetro da query string (nesse caso, apenas o token)
    params = {"token": token}
 
    try:
        #Envia a requisição GET com os parâmetros
        response = requests.get(url, params=params)
        response.raise_for_status( ) #Levanta exceção para status HTTP de erro
        #Converte a resposta para JSON
        data =  response.json()
        return data
    
    #lista de erros
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:",errc)
    except requests.exceptions.TimeoutError as errt:
        print("Timeout:",errt)
    except requests.exceptions.RequestExcention as err:
        print("Erro:", err)

    return None

def extemail(pia, token):

    #URL base da API de validação de e-mail
    base_url ="https://api.invertexto.com/v1/email-validator"
    #codifica o e-mail para garantir que a URL fique correta
    email_encoded = urllib.parse.quote(pia)
    #Monta a URL com o e-mail na rota
    url = f"{base_url}/{email_encoded}"
    #parâmetro da query string (nesse caso, apenas o token)
    params = {"token": token}

    try:

        #Realiza a requisição do GET,passando os parâmetros na URL
        response = requests.get(url,params=params)
        response.raise_for_status() #Levanta exceção para status HTTP de erro 
        #converte a resposta para JSON
        data =  response.json()
        return data
    
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:",errc)
    except requests.exceptions.TimeoutError as errt:
        print("Timeout:",errt)
    except requests.exceptions.RequestException as err:
        print("Erro:", err)

    return None

def extcnpj(api,token):

    print("valor dos dados: ", api)#só para testar
    base_url = "https://api.invertexto.com/v1/validator"
    #codifica o cnpj para garantir que a URL fique correta
    cnpj_encoded = urllib.parse.quote(api)
    #Monta a URL com o cnpj na rota
    url = f"{base_url}/{cnpj_encoded}"
    #parâmetro da query string (nesse caso, apenas o token)
    params = {"token": token}

    try:
        #Envia a requisição GET com os parâmetros
        response = requests.get(url, params=params)
        response.raise_for_status( ) #Levanta exceção para status HTTP de erro
        #Converte a resposta para JSON
        data =  response.json()
        return data
    
    #lista de erros
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:",errc)
    except requests.exceptions.TimeoutError as errt:
        print("Timeout:",errt)
    except requests.exceptions.RequestExcention as err:
        print("Erro:", err)

    return None

def validar_cpf(iap, token):
    #URL base da API
    url = "https://api.invertexto.com/v1/validator"

    #parâmetro que serão enviados via query string
    params = {
        "token": token,
        "value": iap #No exemplo, 'value' representa o CPF
    }

    try:
        #Envia a requisição GET com os parâmetros
        response = requests.get(url, params=params)
        response.raise_for_status( ) #Levanta exceção para status HTTP de erro

        #Converte a resposta para JSON
        data =  response.json()
        return data
    
    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:",errc)
    except requests.exceptions.TimeoutError as errt:
        print("Timeout:",errt)
    except requests.exceptions.RequestExcention as err:
        print("Erro:", err)

    return None