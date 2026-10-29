from crud.crudBase import CrudBase
from core.database import Database
from core.validator import Validar

#campos e tabela do banco

class Login(CrudBase):
    table = "funcionario"
    fields = [
        "senha_funcionario"   
    ]


def update_senha(cls, email, senha):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE funcionario
                SET senha_funcionario =%s
                WHERE email_funcionario=%s
            """

            cursor.execute(sql, (
                dados.get("senha_funcionario")
            ))

            conexao.commit()
            return cursor.rowcount

        finally:
            cursor.close()
            conexao.close()

