from crud.crudBase import CrudBase
from core.database import Database

class entrega_fornecedor(CrudBase):
    table = "entrega_fornecedor"
    fields = ["valor_total_entrega_fornecedor","valor_unt_entrega_fornecedor","item_pediddo_fornecedor","quantidade_entrega_fornecedor","observacao_entrega_fornecedor","fornecedor_id",]
    def __init__(self, valor_total=None, valor_unt=None,item=None, quantidade=None,observacao=None,): #fornecedor_id=None 
        self.valor_total = valor_total
        self.valor_unt = valor_unt
        self.item = item
        self.quantidade = quantidade
        self.observacao = observacao
        
        # --------------------
        # self.fornecedor_id = fornecedor_id

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO entrega_fornecedor (valor_total_entrega_fornecedor,valor_unt_entrega_fornecedor,item_pediddo_fornecedor,quantidade_entrega_fornecedor,observacao_entrega_fornecedor,fornecedor_id,)
                VALUES (%s, %s, %s, %s, %s,%s)
            """

            cursor.execute(sql, (
                self.valor_total, 
                self.valor_unt,
                self.item, 
                self.quantidade, 
                self.observacao, 
                
            ))

            conexao.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            conexao.close()

    # -------------------------
    # UPDATE
    # -------------------------
    @classmethod
    def update_entrega_fornecedor(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE entrega_fornecedor
                SET d_entrega = %s, d_realizacao = %s, quantidade = %s, item = %s, fornecedor_id =%s, funcionario_id= %s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("valor_total"),
                dados.get("valor_unt"),
                dados.get("item"),
                dados.get("quantidade"),
                dados.get("observacao"),
                dados.get("fornecedor_id"),
                id
            ))

            conexao.commit()
            return cursor.rowcount

        finally:
            cursor.close()
            conexao.close()

    # -------------------------
    # DELETE SEGURO
    # -------------------------
    @classmethod
    def related_entrega_fornecedor(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM entrega_fornecedor WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        entrega_fornecedor = cls.find_by_id(id)

        if not pedido_fornecedor:
            raise ValueError("Registro de entrega do fornecedor não encontrada.")

        if cls.related_pedido_fornecedor(id):
            raise ValueError("Entrega do fornecedor realizada.")

        cls.delete(id)
        
    #Selecionar todos as entrega_fornecedor

    @classmethod
    def find_all(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN entrega_fornecedor
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
@classmethod
def find_all_by_id(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN entrega_fornecedor WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()