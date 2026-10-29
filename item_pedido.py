from crud.crudBase import CrudBase
from core.database import Database

class Item_pedido(CrudBase):
    table = "item_pedido"
    fields = ["ativado_item_pedido", "especificacoes_item_pedido"]

    def __init__(self, ativado=None, especificacoes_item_pedido=None):
        self.ativado = ativado
        self.especificacoes = especificacoes


    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir_item_pedido(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO item_pedido (ativado_item_pedido, especificacoes_item_pedido)
                VALUES (%s, %s)
            """

            cursor.execute(sql, (
                self.ativado,
                self.especificacoes
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
    def update_item_pedido(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE item_pedido
                SET ativado_item_pedido=%s, especificacoes_item_pedido=%s WHERE id=%s
                """

            cursor.execute(sql, (
                dados.get("ativado"),
                dados.get("especificacoes"),
                id
            ))

            conexao.commit()
            return cursor.rowcount

        finally:
            cursor.close()
            conexao.close()

    #---------------------
    #Select
    # -------------------


    @classmethod
    def find_all(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN item_pedido
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def find_all_by_id(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN item_pedido WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()


    @classmethod
    def related_item_pedido(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM item_pedido_item_pedido WHERE item_pedido_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()
        
            
    @classmethod
    def safe_delete_item_pedido(cls, id):
        item_pedido = cls.find_by_id(id)

        if not item_pedido:
            raise ValueError("Item pedido não encontrado.")

        if cls.related_item_pedido(id):
            raise ValueError("Item pedido possui pedidos vinculados.")

        cls.delete(id)