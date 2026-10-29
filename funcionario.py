from crud.crudBase import CrudBase
from core.database import Database
from core.security import verificar_senha, gerar_hash_senha

class Funcionario(CrudBase):
    table = "funcionario"
    fields = ["nome_funcionario", "tel_funcionario", "email_funcionario", "cpf_funcionario", "classificacao_funcionario", "cep_funcionario","foto_nome", "foto_localizacao", "foto_blob","num_clt_funcionario","senha_funcionario", "ativado_funcionario" ]

    def __init__(self, nome_funcionario=None, tel_funcionario=None, email_funcionario=None, cpf_funcionario=None, classificacao_funcionario=None, cep_funcionario=None, foto_nome=None, foto_localizacao = None, foto_blob=None, num_clt_funcionario=None, senha_funcionario=None, ativado_funcionario=None):
            
            self.nome_funcionario = nome_funcionario
            self.tel_funcionario = tel_funcionario
            self.email_funcionario = email_funcionario
            self.cpf_funcionario = cpf_funcionario
            self.classificacao_funcionario = classificacao_funcionario
            self.cep_funcionario = cep_funcionario
            self.foto_nome = foto_nome
            self.foto_localizacao= foto_localizacao
            self.foto_blob = foto_blob
            self.num_clt_funcionario = num_clt_funcionario
            self.senha_funcionario = senha_funcionario
            self.ativado_funcionario = ativado_funcionario

            super().__init__() #adicionado

    @staticmethod
    def autenticar(email_funcionario, senha_funcionario):
        """
        Verifica se o usuário existe e se a senha está correta.
        """
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM funcionario
                WHERE email_funcionario = %s
                AND ativado_funcionario = 0
            """
            cursor.execute(sql, (email_funcionario,))
            usuario = cursor.fetchone()

            if usuario is None:
                return None

            senha_banco = usuario.get("senha_funcionario")
            if not senha_banco:
                return None

            if verificar_senha(senha_funcionario, senha_banco):
                return usuario

            return None
        finally:
            cursor.close()
            conexao.close()

    # -------------------------
    # INSERT
    # -------------------------
    @classmethod
    def inserir(cls,dados):

        # insere o usuario com senha criptografada
            senha_texto = dados.get("senha_funcionario")
            dados["senha_funcionario"] = gerar_hash_senha(senha_texto)
            print("inserir")

            return cls(**dados).insert()
    
    @classmethod
    def listar_com_imagem(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM funcionario
                ORDER BY nome_funcionario
            """
            cursor.execute(sql)
            funcionarios = cursor.fetchall()
            return funcionarios
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_id_com_imagem(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM funcionario
                WHERE id = %s
            """
            cursor.execute(sql, (id,))
            funcionario = cursor.fetchone()
            return funcionario
        finally:
            cursor.close()
            conexao.close()

    # -------------------------
        # UPDATE
        # -------------------------
    @classmethod
    def update_funcionario(cls, id, dados):
            conexao = Database.connect()
            cursor = conexao.cursor()

            try:
                sql = """
                    UPDATE funcionario
                    SET nome_funcionario=%s, tel_funcionario=%s, email_funcionario=%s, cpf_funcionario=%s, classificacao_funcionario=%s, cep_funcionario=%s, foto_nome=%s, foto_localizacao=%s, foto_blob=%s, num_clt_funcionario=%s, senha_funcionario=%s, ativado_funcionario=%s
                    WHERE id=%s
                """

                cursor.execute(sql, (
                    dados.get("nome_funcionario"),
                    dados.get("tel_funcionario"),
                    dados.get("email_funcionario"),
                    dados.get("cpf_funcionario"),
                    dados.get("classificacao_funcionario"),
                    dados.get("cep_funcionario"),
                    dados.get("foto_nome"),
                    dados.get("foto_localizacao"),
                    dados.get("foto_blob"),
                    dados.get("num_clt_funcionario"),
                    dados.get("senha_funcionario"),
                    dados.get("ativado_funcionario"),
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
    def related_funcionario(cls, id):
            conexao = Database.connect()
            cursor = conexao.cursor()

            try:
                sql = "SELECT COUNT(*) FROM producao WHERE funcionario_id = %s"
                cursor.execute(sql, (id,))
                total = cursor.fetchone()[0]

                return total > 0

            finally:
                cursor.close()
                conexao.close()

    @classmethod
    def safe_delete(cls, id):
        funcionario = cls.find_by_id(id)

        if not funcionario:
            raise ValueError("funcionario não encontrado.")

        if cls.related_funcionario(id):
            raise ValueError("funcionario possui pedidos vinculados.")

        cls.delete(id)

    @classmethod
    def find_all(cls):
            conexao = Database.connect()
            cursor = conexao.cursor(dictionary=True)
            try:
                sql = "SELECT * FROM funcionario"
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
            sql = "SELECT * FROM funcionario WHERE id = %s"
            cursor.execute(sql, (id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

