import sqlite3
import os

class SqlToDb:
    directory: str = "db"
    suffix: str = ".db"

    def __init__(self, file, sql_file):
        # Verzeichnis erstellen, falls es nicht existiert
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        self.path_file = f"{os.path.abspath(os.getcwd())}/{self.directory}/{file}{self.suffix}"
        print(file)
        print(sql_file)
        print(self.path_file)

        self.conn = sqlite3.connect(self.path_file)
        c = self.conn.cursor()

        with open(sql_file, 'r') as sql_file:
            sql_script = sql_file.read()

        c.executescript(sql_script)
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    # print(os.path.abspath(os.getcwd()))
    sqlToDb = SqlToDb("ETL_uebung", "/home/dev/projects/draw_io_to_sql/files/sql/ETL_uebung.sql")

    conn = sqlite3.connect('/home/dev/projects/draw_io_to_sql/db/ETL_uebung.db')
    cursor = conn.cursor()

    # Funktion zum Überprüfen, ob eine Tabelle existiert
    def check_table_exists(table_name):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        return cursor.fetchone() is not None

    # Tabellen, die überprüft werden sollen
    tables = ['tb_dim_customer', 'tb_dim_article_category', 'tb_dim_store']

    # Überprüfung der Tabellen
    for table in tables:
        if check_table_exists(table):
            print(f"Tabelle {table} existiert.")
        else:
            print(f"Tabelle {table} existiert nicht.")

    # Verbindung schließen
    conn.close()
