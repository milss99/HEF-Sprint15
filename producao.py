from crud.crudBase import CrudBase
from core.database import Database


class Producao(CrudBase):
    table = "producao"
    fields = ["etapa_producao", "status_producao", "acontecimento_producao"]
    def __init__(self, etapa_producao=None, status_producao=None, acontecimento=None ):
        self.etapa_producao = etapa_producao
        self.status_producao = status_producao
        self.acontecimento = acontecimento

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO cliente (etapa_producao, status_producao, acontecimento_producao)
                VALUES (%s, %s, %s)
            """


            conexao.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            conexao.close()

    # -------------------------
    # UPDATE
    # -------------------------
    @classmethod
    def update_producao(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE producao
                SET etapa_producao=%s, status_producao=%s, acontecimento_producao=%s)
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("etapa_producao"),
                dados.get("status_producao"),
                dados.get("acontecimento_producao")
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
    def related_pedido_cliente(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM producao WHERE producao_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        producao = cls.find_by_id(id)

        if not producao:
            raise ValueError("O lote não está em produção.")

        if cls.related_pedido_cliente(id):
            raise ValueError(" O lote está em produção.")

        cls.delete(id)

        #Selecionar todos os fornecedores

    @classmethod
    def find_all(cls):
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)
            try:
                sql = """
                SELECT * IN producao
                """
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                cursor.close()
                conexao.close()

#Seleção por id
    def find_all_by_id(cls):
                conexao = Database.connect()
                cursor = conexao.cursor(dictionary=True)
                try:
                    sql = """
                    SELECT * IN producao WHERE id= %s
                    """
                    cursor.execute(sql)
                    return cursor.fetchall()
                finally:
                    cursor.close()
                    conexao.close()


