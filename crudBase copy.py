from core.database import Database

class CrudBase:
    table = ""
    fields = []

##################READ####################

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
###################DELETE###############################
    @classmethod
    def delete(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            sql = f"DELETE FROM {cls.table} WHERE id = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

####################INSERT##################

    def insert(self,id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            colunas = ", ".join(self.fields)
            marcadores = ", ".join(["%s"] * len(self.fields))
            valores = tuple(getattr(self, campo, "erro codigo") for campo in self.fields)
            sql = f"INSERT INTO {self.table} ({colunas}) VALUES ({marcadores})"
            print(valores)
    
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

#####################UPDATE##############################

    def update(self, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{campo} = %s" for campo in self.fields])
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id,)
            sql = f"UPDATE {self.table} SET {campos} WHERE id = %s"
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    def count(self):
        conexao = connect()
        cursor = conexao.cursor(dictionary=True)

        sql = f"SELECT COUNT(*) AS total FROM {self.tabela}"

        cursor.execute(sql)
        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        return resultado["total"]