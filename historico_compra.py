from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validar

#campos e tabela do banco



class historico_compra(CrudBase):
    table = "historico_compra"
    fields = [
        "d_entrega_historico_compra",
        "d_realizacao_historico_compra",
    ]

#define valor e parametro
    def __init__(self, d_entrega_historico_compra=None,d_realizacao_historico_compra=None):
        self.d_entrega_historico_compra = d_entrega_historico_compra
        self.d_realizacao_historico_compra = d_realizacao_historico_compra

#validando

    def validate(self):
        erros = [
            Validator.required(self.d_entrega_historico_compra, "d_entrega_historico_compra"),
            Validator.non_negative(self.d_realizacao_historico_compra, "d_realizacao_historico_compra"),
        ]
        return [erro for erro in erros if erro]


#classe inserir fornecedor  
    @classmethod
    def inserir_hc(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """INSERT INTO TABLE historico_compra(d_entrega_historico_compra,d_realizacao_historico_compra) 
            VALUES(%s,%s,)"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


#Atualizar fornecedor

    @classmethod
    def atualizacao_hc(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """ UPDATE historico_compra
                SET d_entrega_historico_compra=%s, d_realizacao_historico_compra=%s
                WHERE id=%s"""

            cursor.execute(sql, (
                dados.get("d_entrega_historico_compra"),
                dados.get("d_realizacao_historico_compra"),
                id
            ))

            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            cursor.close()
            conexao.close()

#Se tiver alguma função relacionada ao Fornecedor
    @classmethod
    def related_hc(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM historico_compra WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

#Deletar fornecedor

    @classmethod
    def deletar_hc(cls):
        historico_vendas = cls.find_by_id(id)

        if not historico_compra:
            raise ValueError("Registro de compra não encontrado.")

        if cls.related_hc(id):
            raise ValueError("Registro de compra possui pedidos pendentes vinculados.")

        cls.delete(id)



#Selecionar todos os fornecedores

    @classmethod
    def find_all_hc(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN historico_compra
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
@classmethod
def find_all_by_id_hc(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN historico_compra WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()