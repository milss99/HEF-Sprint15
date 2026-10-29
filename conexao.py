import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.conect(
            host= "localhost",
            user= "root",
            password= "123456",
            database= "hefesto",
            auth_plugin ="mysql_native_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao connectar ao banco de dados: {err}")
        return None