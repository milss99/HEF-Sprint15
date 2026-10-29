from crud.crudBase import CrudBase
from core.database import Database


class Materia_prima(CrudBase):
    table = "materia_prima"
    fields = ["nome_materia_prima", "d_validade_materia_prima", "estoque_materia_prima", "min_estoque_materia_prima", "d_ult_reposicao_materia_prima", "descricao_materia_prima", "barracao_rua_materia_primacol", "barracao_andar_materia_prima", "barracao_num_materia_prima", "ativado_materia_prima", "pedido_fornecedor_id"]

    def __init__(self, nome_materia_prima=None, d_validade_materia_prima=None, estoque_materia_prima=None, min_estoque_materia_prima=None, d_ult_reposicao_materia_prima=None, descricao_materia_prima=None, barracao_rua_materia_primacol=None, barracao_andar_materia_prima=None, barracao_num_materia_prima=None, ativado_materia_prima=None, pedido_fornecedor_id=None):
        self.nome_materia_prima = nome_materia_prima
        self.d_validade_materia_prima = d_validade_materia_prima
        self.estoque_materia_prima = estoque_materia_prima
        self.min_estoque_materia_prima = min_estoque_materia_prima
        self.d_ult_reposicao_materia_prima = d_ult_reposicao_materia_prima
        self.descricao_materia_prima = descricao_materia_prima
        self.barracao_rua_materia_primacol = barracao_rua_materia_primacol
        self.barracao_andar_materia_prima = barracao_andar_materia_prima
        self.barracao_num_materia_prima = barracao_num_materia_prima
        self.ativado_materia_prima = ativado_materia_prima
        self.pedido_fornecedor_id = pedido_fornecedor_id

    @classmethod
    def inserir(cls, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO materia_prima (
                    nome_materia_prima,
                    d_validade_materia_prima,
                    estoque_materia_prima,
                    min_estoque_materia_prima,
                    d_ult_reposicao_materia_prima,
                    descricao_materia_prima,
                    barracao_rua_materia_primacol,
                    barracao_andar_materia_prima,
                    barracao_num_materia_prima,
                    ativado_materia_prima,
                    pedido_fornecedor_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                dados.get("nome_materia_prima"),
                dados.get("d_validade_materia_prima"),
                dados.get("estoque_materia_prima"),
                dados.get("min_estoque_materia_prima"),
                dados.get("d_ult_reposicao_materia_prima"),
                dados.get("descricao_materia_prima"),
                dados.get("barracao_rua_materia_primacol"),
                dados.get("barracao_andar_materia_prima"),
                dados.get("barracao_num_materia_prima"),
                dados.get("ativado_materia_prima"),
                dados.get("pedido_fornecedor_id")
            ))

            conexao.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def update_materia_prima(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE materia_prima
                SET nome_materia_prima = %s,
                    d_validade_materia_prima = %s,
                    estoque_materia_prima = %s,
                    min_estoque_materia_prima = %s,
                    d_ult_reposicao_materia_prima = %s,
                    descricao_materia_prima = %s,
                    barracao_rua_materia_primacol = %s,
                    barracao_andar_materia_prima = %s,
                    barracao_num_materia_prima = %s,
                    ativado_materia_prima = %s,
                    pedido_fornecedor_id = %s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("nome_materia_prima"),
                dados.get("d_validade_materia_prima"),
                dados.get("estoque_materia_prima"),
                dados.get("min_estoque_materia_prima"),
                dados.get("d_ult_reposicao_materia_prima"),
                dados.get("descricao_materia_prima"),
                dados.get("barracao_rua_materia_primacol"),
                dados.get("barracao_andar_materia_prima"),
                dados.get("barracao_num_materia_prima"),
                dados.get("ativado_materia_prima"),
                dados.get("pedido_fornecedor_id"),
                id
            ))

            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def related_materia_prima(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM materia_prima WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        materia_prima = cls.find_by_id(id)

        if not materia_prima:
            raise ValueError("Matéria-prima não encontrada.")

        if cls.related_materia_prima(id):
            raise ValueError("Matéria-prima possui pedidos vinculados.")

        cls.delete(id)

    @classmethod
    def find_all(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM materia_prima"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_all_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM materia_prima WHERE id = %s"
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def count_itens(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT COUNT(*) AS total
                FROM materia_prima
                WHERE estoque_materia_prima > 0
            """
            cursor.execute(sql)
            resultado = cursor.fetchone()
            return resultado["total"] if resultado else 0
        finally:
            cursor.close()
            conexao.close()