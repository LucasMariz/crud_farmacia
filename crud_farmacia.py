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

def main():
    gerenciador = GerenciadorDeClientes()

    # Inserir alguns clientes
    print("Inserindo clientes...")
    gerenciador.inserir_cliente('Alice Santos', 'alice@example.com')
    gerenciador.inserir_cliente('Bob Marley', 'bob@example.com')

    # Listar todos os clientes
    print("\nListando todos os clientes...")
    clientes = gerenciador.listar_clientes()
    for cliente in clientes:
        print(cliente)

    # Atualizar cliente
    print("\nAtualizando cliente...")
    gerenciador.alterar_cliente(1, 'Alice Albuquerque', 'alice@example.com')
    print(gerenciador.exibir_cliente(1))

    # Pesquisar cliente por nome
    print("\nPesquisando cliente por nome 'Bob'...")
    resultado = gerenciador.pesquisar_cliente_por_nome('Bob')
    for cliente in resultado:
        print(cliente)

    # Exibir um cliente específico
    print("\nExibindo cliente de ID 1...")
    print(gerenciador.exibir_cliente(1))

    # Remover um cliente
    print("\nRemovendo cliente de ID 2...")
    gerenciador.remover_cliente(2)
    print("Listando todos os clientes após remoção...")
    clientes = gerenciador.listar_clientes()
    for cliente in clientes:
        print(cliente)

if __name__ == "__main__":
    main()