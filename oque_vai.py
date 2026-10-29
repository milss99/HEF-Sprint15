from crud.crudBase import CrudBase
from core.database import Database

class Oque_vai(CrudBase):
    table = "oque_vai"
    fields = []

#>>>>>>>>>>>>>>>>>>>>>>>>sem parametro<<<<<<<<<<<<<<<<<<

    @classmethod
    def find_all(cls, order_by="id"):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} ORDER BY {order_by}"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

#>>>>>>>>>>>>>>>>>>por parametro(id)<<<<<<<<<<<<<<<<<<<<<<
    @classmethod
    def find_by_id(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE id = %s"
            cursor.execute(sql, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()