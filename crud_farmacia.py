import sqlite3

class GerenciadorDeBanco:
    def __init__(self, db_path='farmacia.db'):
        self.db_path = db_path
        self.conectar_banco()
        self.criar_tabelas()

    def conectar_banco(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            email TEXT UNIQUE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            quantidade INTEGER,
                            preco DECIMAL)''')
        self.conn.commit()