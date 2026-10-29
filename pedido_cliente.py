from crud.crudBase import CrudBase
from core.database import Database

class PedidoCliente(CrudBase):
    table = "cliente"
    fields = ["d_realizacao_pedido_cliente", "quantidade_pedido_cliente", "valor_unt_pedido_cliente", "valor_total_pedido_cliente", "prazo_final_pedido_cliente", "op_pedido_cliente"]

    def __init__(self, d_realizacao=None, quantidade=None, valor_unt=None, valor_total=None, prazo_final=None, op=None, ):
        self.d_realizacao = d_realizacao
        self.quantidade = quantidade
        self.valor_unt = valor_unt
        self.valor_total = valor_total
        self.prazo_final = prazo_final
        self.op = op

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO cliente (d_realizacao_pedido_cliente, quantidade_pedido_cliente, valor_unt_pedido_cliente, valor_total_pedido_cliente, prazo_final_pedido_cliente, op_pedido_cliente)
                VALUES (%s, %s, %s, %s, %s,%s)
            """

            cursor.execute(sql, (
                self.d_realizacao,
                self.quantidade,
                self.valor_unt,
                self.valor_total, 
                self.prazo_final,
                self.op 

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
    def update_pedido_cliente(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE pedido_cliente
                SET d_realizacao_pedido_cliente=%s, quantidade_pedido_cliente=%s, valor_unt_pedido_cliente=%s, valor_total_pedido_cliente, prazo_final_pedido_cliente=%s, op_pedido_cliente=%s)
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("d_realizacao_pedido_cliente"),
                dados.get(" quantidade_pedido_cliente"),
                dados.get("valor_unt_pedido_cliente"),
                dados.get(" valor_total_pedido_cliente"),
                dados.get("prazo_final_pedido_cliente"),
                dados.get("op_pedido_cliente"),
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
    def related_pedido_cliente(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM pedido_cliente WHERE cliente_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        pedido_cliente = cls.find_by_id(id)

        if not pedido_cliente:
            raise ValueError("O pedido do cliente não foi encontrado.")

        if cls.related_pedido_cliente(id):
            raise ValueError(" O pedido cliente possui pedidos vinculados.")

        cls.delete(id)

        #Selecionar todos os fornecedores

    @classmethod
    def find_all(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN pedido_cliente
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
            SELECT * IN pedido_cliente WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

