from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validar

#campos e tabela do banco



class Fornecedor(CrudBase):
    table = "historico_vendas"
    fields = [
        "d_entrega_historico_vendas",
        "d_realizacao_historico_vendas",
        "quantidade_historico_vendas",
        "valor_total_historico_vendas",
        "prazo_final_historico_vendas",
        "d_termino_historico_vendas",
        
    ]

#define valor e parametro
    def __init__(self, d_entrega_historico_vendas=None,d_realizacao_historico_vendas=None,quantidade_historico_vendas=None,valor_total_historico_vendas=None,prazo_final_historico_vendas=None, d_termino_historico_vendas= None):
        self.d_entrega_historico_vendas = d_entrega_historico_vendas
        self.d_realizacao_historico_vendas = d_realizacao_historico_vendas
        self.quantidade_historico_vendas = quantidade_historico_vendas
        self.valor_total_historico_vendas= valor_total_historico_vendas
        self.prazo_final_historico_vendas = prazo_final_historico_vendas
        self.d_termino_historico_vendas = d_termino_historico_vendas


#validando

def validate(self):
        erros = [
            Validator.required(self.d_entrega_historico_vendas, "d_entrega_historico_vendas"),
            Validator.non_negative(self.d_realizacao_historico_vendas, "d_realizacao_historico_vendas"),
            Validator.non_negative(self.quantidade_historico_vendas,  "quantidade_historico_vendas"),
            Validator.non_negative(self.valor_total_historico_vendas, "valor_total_historico_vendas"),
            Validator.non_negative(self.prazo_final_historico_vendas, "prazo_final_historico_vendas"),
            Validator.non_negative(self.d_termino_historico_vendas, "d_termino_historico_vendas")
        ]
        return [erro for erro in erros if erro]


#classe inserir fornecedor  
@classmethod
def inserir_hv(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """INSERT INTO TABLE fornecedor(d_entrega_historico_vendas,d_realizacao_historico_vendas,quantidade_historico_vendas ,valor_total_historico_vendas,prazo_final_historico_vendas, d_termino_historico_vendas) 
            VALUES(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


#Atualizar fornecedor

@classmethod
def atualizacao_hv(cls):
    conexao = Database.connect()
    cursor = conexao.cursor(dictionary=True)
    try:
        sql = """ UPDATE fornecedor
            SET d_entrega_historico_vendas=%s, d_realizacao_historico_vendas=%s, quantidade_historico_vendas=%s, valor_total_historico_vendas=%s, prazo_final_historico_vendas=%s, d_termino_historico_vendas=%s
            WHERE id=%s"""

        cursor.execute(sql, (
            dados.get("d_entrega_historico_vendas"),
            dados.get("d_realizacao_historico_vendas"),
            dados.get("quantidade_historico_vendas"),
            dados.get("valor_total_historico_vendas"),
            dados.get("prazo_final_historico_vendas"),
            dados.get(" d_termino_historico_vendas"),
                id
            ))

        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

#Se tiver alguma função relacionada ao Fornecedor
@classmethod
def related_hv(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM historico_vendas WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

#Deletar fornecedor

@classmethod
def deletar_hv(cls):
    historico_vendas = cls.find_by_id(id)

    if not historico_vendas:
        raise ValueError("Registro de vendas não encontrado.")

    if cls.related_hv(id):
        raise ValueError("Registro de vendas possui pedidos pendentes vinculados.")

        cls.delete(id)



#Selecionar todos os fornecedores

@classmethod
def find_all_hv(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN historico_vendas
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
def find_all_by_id_hv(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN historico_vendas WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

