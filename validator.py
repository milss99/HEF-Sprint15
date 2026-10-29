import re
class Validar():

   

#====================validação- CARAC. ESPECIAL =====================

   
    def val_especial(dados):
        insert= len(dados) #recebe o dado inserido
        modifica =  re.search ("[!@#$%¨&*()_+=?/-:;<>]", insert) #procura nos dados os caracteres indicados
        if modifica == True: #condicao: se for achado...
            flash(erro, "Os dados não devem incluir caracteres especiais", "warning")
            return True

        else:
            flash("Cadastro concluido com sucesso", "success")
        return False

#=======================validação - NUMEROS ==========================

         
    def validar_numero():
        try:
            float(valor)  # aceita inteiro e decimal
            return True
        except ValueError:
            return False

#==========================validação - QUANTIDADE=======================


 
    def validar_quantidade(dados):

        if not qtd.isdigit():
            return False

        if qtd <= 0:
            return False

        return True


#==============================validação - TEXTO=======================

        

 
#converte tudo pra letra
    def val_texto_letra(dados):
        tem_letra = False

        for caractere in texto:
            if caractere.isalpha(): #transforma em letra
                tem_letra = True

        return tem_letra

#Validar quantidade max e min de caracters 
    def val_texto_minmax(dados):

        texto = texto.strip()

        return 1 <= len(texto) <= 50

#validar se tem espaço
    def val_texto_espaco(dados):
        
        possui_espaco = True

        for caractere in dados:
            if caractere.isspace():
                possui_espaco = False

            if not possui_espaco:
                flash ("cadastro concluído com sucesso", "success")
                return False
            return True

        return True



    def val_maiusculo(dados):

        return texto.isupper()


        try:
            response = requests.get(url, params=params)   #Envia a requisição GET com os parâmetros
            response.raise_for_status( ) #Levanta exceção para status HTTP de erro
            data =  response.json()#Converte a resposta para JSON
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
            
        

   
       
  





