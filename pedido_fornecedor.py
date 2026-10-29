from crud.crudBase import CrudBase
from core.database import Database

class PedidoFornecedor(CrudBase):
    table = "pedido_fornecedor"
    fields = ["d_entrega_pediddo_fornecedor","d_realizacao_pediddo_fornecedor","quantidade_pediddo_fornecedor","item_pediddo_fornecedor","fornecedor_id", "funcionario_id"]
    def __init__(self, d_entrega=None, d_realizacao=None, quantidade=None,item=None,): #fornecedor_id=None, funcionario_id=None 
        self.d_entrega = d_entrega
        self.d_realizacao = d_realizacao
        self.quantidade = quantidade
        self.item = item
        
        # --------------------
        # self.fornecedor_id = fornecedor_id
         # self.funcionario_id = funcionario_id

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO pedido_fornecedor (d_entrega_pediddo_fornecedor,d_realizacao_pediddo_fornecedor,quantidade_pediddo_fornecedor,item_pediddo_fornecedor,fornecedor_id, funcionario_id)
                VALUES (%s, %s, %s, %s, %s,%s)
            """

            cursor.execute(sql, (
                self.d_entrega, 
                self.d_realizacao, 
                self.quantidade, 
                self.item, 
                
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
    def update_pedido_fornecedor(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE pedido_fornecedor
                SET d_entrega = %s, d_realizacao = %s, quantidade = %s, item = %s, fornecedor_id =%s, funcionario_id= %s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("d_entrega"),
                dados.get("d_realizacao"),
                dados.get("quantidade"),
                dados.get("item"),
                dados.get("fornecedor_id"),
                dados.get("funcionario_id"),
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
    def related_pedido_fornecedor(cls, id):
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

    @classmethod
    def safe_delete(cls, id):
        pedido_fornecedor = cls.find_by_id(id)

        if not pedido_fornecedor:
            raise ValueError("Pedido ao fornecedor não encontrada.")

        if cls.related_pedido_fornecedor(id):
            raise ValueError("Pedido ao fornecedor realizado.")

        cls.delete(id)
        
    #Selecionar todos as pedido_fornecedor

    @classmethod
    def find_all(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN pedido_fornecedor
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
            SELECT * IN pedido_fornecedor WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()