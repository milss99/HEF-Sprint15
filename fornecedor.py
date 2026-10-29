from crud.crudBase import CrudBase
from core.database import Database
from core.validator import Validar

#campos e tabela do banco

class Fornecedor(CrudBase):
    table = "fornecedor"
    fields = [
        "nome_fornecedor",
        "cnpj_fornecedor",
        "tel_fornecedor",
        "email_fornecedor",
        "cep_fornecedor",
        "materia_prima_fornecedor",
        "ativado_fornecedor"
    ]

#define valor e parametro
    def __init__(self, nome_fornecedor=None,cnpj_fornecedor=None,tel_fornecedor=None,email_fornecedor=None,cep_fornecedor=None, materia_prima_fornecedor= None, ativado_fornecedor=None):
        self.nome_fornecedor = nome_fornecedor
        self.cnpj_fornecedor = cnpj_fornecedor
        self.tel_fornecedor = tel_fornecedor
        self.email_fornecedor= email_fornecedor
        self.cep_fornecedor = cep_fornecedor
        self.materia_prima_fornecedor = materia_prima_fornecedor
        self.ativado_fornecedor = ativado_fornecedor


#validando

    def validate(self):
        erros = [
            Validator.required(self.nome_fornecedor, "nome_fornecedor"),
            Validator.non_negative(self.cnpj, "cnpj"),
            Validator.non_negative(self.telefone,  "telefone"),
            Validator.non_negative(self.email, "email"),
            Validator.non_negative(self.cep, "cep"),
            Validator.non_negative(self.materia_prima, "materia_prima"),
        ]
        return [erro for erro in erros if erro]


#classe inserir fornecedor  
@classmethod
def inserir(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """INSERT INTO TABLE fornecedor(nome_fornecedor,cnpj_fornecedor,email_fornecedor ,tel_fornecedor,cep_fornecedor, materia_prima_fornecedor, ativado_fornecedor) 
            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


#Atualizar fornecedor

@classmethod
def atualizacao_fornecedor(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """ UPDATE fornecedor
                SET nome_fornecedor=%s, cnpj_fornecedor=%s, tel_fornecedor=%s, email_fornecedor=%s, cep_fornecedor=%s, ativado_fornecedor=%s
                WHERE id=%s"""

            cursor.execute(sql, (
                dados.get("nome_fornecedor"),
                dados.get("cnpj_fornecedor"),
                dados.get("tel_fornecedor"),
                dados.get("email_fornecedor"),
                dados.get("cep_fornecedor"),
                dados.get("ativado_fornecedor"),
                id
            ))

            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Se tiver alguma função relacionada ao Fornecedor
@classmethod
def related_fornecedor(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM pedido_fornecedor WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

#Deletar fornecedor

@classmethod
def deletar_fornecedor(cls):
        fornecedor = cls.find_by_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado.")

        if cls.related_fornecedor(id):
            raise ValueError("Fornecedor possui pedidos vinculados.")

        cls.delete(id)



#Selecionar todos os fornecedores

@classmethod
def find_all_fornecedor(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN fornecedor
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
@classmethod
def find_all_by_id_fornecedor(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN fornecedor WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

