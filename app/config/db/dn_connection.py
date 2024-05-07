import mysql.connector

class MysqlConnection:
    def __init__(self, host,port, user, password,base):
        self.cnx = mysql.connector.connect(host=host, user=user, password=password, database=base,port=port)

    def close(self):
        self.cnx.close()

    def get_row_by_table_and_id(self, id,table_name):
        cursor = self.cnx.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE id={id}')
        row = cursor.fetchone()
        return row