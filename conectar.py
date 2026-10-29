

import mysql.connector
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="hefesto"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar1 ao banco de dados: {err}")
        return None
    

    


