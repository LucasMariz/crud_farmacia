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

class GerenciadorDeClientes(GerenciadorDeBanco):
    def inserir_cliente(self, nome, email):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, email) VALUES (?, ?)', (nome, email))
        self.conn.commit()

    def listar_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clientes')
        return cursor.fetchall()

    def alterar_cliente(self, id, nome, email):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE clientes SET nome = ?, email = ? WHERE id = ?', (nome, email, id))
        self.conn.commit()

    def pesquisar_cliente_por_nome(self, nome):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE nome LIKE ?', ('%'+nome+'%',))
        return cursor.fetchall()

    def exibir_cliente(self, id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
        return cursor.fetchone()

    def remover_cliente(self, id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
        self.conn.commit()