from crud.crudBase import CrudBase
from core.database import Database

class Cliente(CrudBase):
    table = "cliente"
    fields = ["nome_cliente", "cnpj_cliente", "email_cliente", "tel_cliente", "cep_cliente", "ativado_cliente"]

    def __init__(self, nome_cliente=None, cnpj_cliente=None, email_cliente=None,tel_cliente=None,  cep_cliente=None, ativado_cliente=None ):
        self.nome_cliente = nome_cliente
        self.cnpj_cliente = cnpj_cliente
        self.email_cliente = email_cliente
        self.tel_cliente = tel_cliente
        self.cep_cliente = cep_cliente
        self.ativado_cliente = ativado_cliente

#------------------------------
#INSERT
#------------------------------
    @classmethod
    def inserir(cls,dados):

        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO cliente (nome_cliente, cnpj_cliente, email_cliente, tel_cliente, cep_cliente, ativado_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                dados.get("nome_cliente"),
                dados.get("cnpj_cliente"),
                dados.get("email_cliente"),
                dados.get("tel_cliente"),
                dados.get("cep_cliente"),
                dados.get("ativado_cliente")
            ))

            conexao.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            conexao.close()


#----------------------------
#VALIDAÇÃO
#----------------------------
    @classmethod
    def valida_cliente(self):
        erro_cliente = Validator.validar_cnpj(self.cliente_id, "cliente")
        if erro_produto:
            erros.append(erro_produto)

        return erros


    # -------------------------
    # UPDATE
    # -------------------------
    @classmethod
    def update_cliente(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE cliente
                SET nome_cliente=%s, cnpj_cliente=%s, email_cliente=%s, tel_cliente=%s, cep_cliente=%s, ativado_cliente=%s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("nome_cliente"),
                dados.get("cnpj_cliente"),
                dados.get("email_cliente"),
                dados.get("tel_cliente"),
                dados.get("cep_cliente"),
                dados.get("ativado_cliente"),
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
    def related_cliente(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM cliente WHERE cliente_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete_cliente(cls, id):
        cliente = cls.find_by_id(id)

        if not cliente:
            raise ValueError("Cliente não encontrado.")

        if cls.related_cliente(id):
            raise ValueError("Cliente possui pedidos vinculados.")

        cls.delete(id)

        #Selecionar todos os fornecedores

    @classmethod
    def find_all_cliente(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * FROM cliente ORDER BY id
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
@classmethod
def find_all_by_id_cliente(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * FROM cliente WHERE id = %s
            """
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

