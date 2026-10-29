from crud.crudBase import CrudBase
from core.database import Database

class Produto(CrudBase):
    table = "produto"
    fields = ["nome_produto", "dimensoes_produto", "imagem_produto", "minimo_produto", "ativado_produto"]

    def __init__(self, nome=None, dimensoes=None, imagem=None, minimo=None, ativado=None):
        self.nome = nome
        self.dimensoes = dimensoes
        self.imagem = imagem
        self.minimo = minimo
        self.ativado = ativado

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir_produto(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO produto (nome_produto, dimensoes_produto, imagem_produto, minimo_produto, ativado_produto)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                self.nome,
                self.dimensoes,
                self.imagem,
                self.minimo,
                self.ativado
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
    def update_produto(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE produto
                SET nome_produto=%s, dimensoes_produto=%s, imagem_produto=%s, minimo_produto=%s, ativado_produto=%s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("nome"),
                dados.get("dimensoes"),
                dados.get("imagem"),
                dados.get("minimo"),
                dados.get("ativado"),
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
            SELECT * IN produto
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
            SELECT * IN produto WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def related_produto(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM item_pedido WHERE produto_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()
        
            
    @classmethod
    def safe_delete_produto(cls, id):
        produto = cls.find_by_id(id)

        if not produto:
            raise ValueError("Produto não encontrado.")

        if cls.related_produto(id):
            raise ValueError("Produto possui pedidos vinculados.")

        cls.delete(id)