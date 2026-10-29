from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

#campos e tabela do banco

class Fornecedor(CrudBase):
    table = "estoque_final"
    fields = [
        "barracao_rua_estoque_final",
        "barracao_andar_estoque_final",
        "barracao_num_estoque_final"
    ]

#define valor e parametro
    def __init__(self, barracao_num_estoque_final=None,barracao_andar_estoque_final=None,barracao_rua_estoque_final=None):
        self.barracao_rua_estoque_final = barracao_rua_estoque_final
        self. barracao_andar_estoque_final= barracao_andar_estoque_final
        self.barracao_num_estoque_final = barracao_num_estoque_final
        
 # -------------------------
    # INSERT-Estoque final
    # -------------------------
@classmethod
def inserir_ef(self):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                INSERT INTO estoque_final (barracao_rua_estoque_final, barracao_andar_estoque_final,barracao_num_estoque_final)
                VALUES (%s, %s, %s )
            """

            cursor.execute(sql, (
                self.barracao_rua_estoque_final,
                self.barracao_andar_estoque_final,
                self.barracao_num_estoque_final
              
            ))

            conexao.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            conexao.close()


#update- estoque final
@classmethod
def update_ef(cls, id, dados):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = """
                UPDATE estoque_final
                SET barracao_rua_estoque_final=%s, barracao_andar_estoque_final=%s, barracao_num_estoque_final=%s
                WHERE id=%s
            """

            cursor.execute(sql, (
                dados.get("barracao_rua_estoque_final"),
                dados.get("barracao_andar_estoque_final"),
                dados.get("barracao_num_estoque_final"),
                id
            ))

            conexao.commit()
            return cursor.rowcount

        finally:
            cursor.close()
            conexao.close()


##Se tiver alguma função relacionada ao Fornecedor
@classmethod
def related_ef(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM estoque_final WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

#Deletar fornecedor

@classmethod
def deletar_ef(cls):
    estoque_final= cls.find_by_id(id)

    if not estoque_final:
        raise ValueError("Registro de estoque não encontrado.")

    if cls.related_ef(id):
            raise ValueError("Registro de estoque está vinculado à um dado em processamento.")

    cls.delete(id)



#Selecionar todos os fornecedores

@classmethod
def find_all_ef(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN estoque_final
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#Seleção por id
def find_all_by_id_ef(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = """
            SELECT * IN estoque_final WHERE id= %s
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

