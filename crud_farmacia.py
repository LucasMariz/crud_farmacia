import sqlite3
import logging

class GerenciadorDeBanco:
    def __init__(self, db_path='farmacia.db'):
        self.db_path = db_path
        self.db_connected = False  # atributo para indicar se está conectado
        self.table_names = ['clientes', 'produtos']  # atributo com os nomes das tabelas
        self.last_query = ""  # atributo para armazenar a última query executada
        # Configuração do logger
        self.logger = logging.getLogger('GerenciadorDeBanco')
        logging.basicConfig(level=logging.INFO)
        self.conectar_banco()
        self.criar_tabelas()

    def conectar_banco(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.db_connected = True
            self.logger.info(f"Conectado ao banco de dados {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return self.conn

    def criar_tabelas(self):
        if not self.db_connected:
            self.logger.error("Tentativa de criar tabelas sem conexão com o banco de dados.")
            return
        cursor = self.conn.cursor()
        for tabela in self.table_names:
            if tabela == 'clientes':
                cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nome TEXT NOT NULL,
                                    email TEXT UNIQUE)''')
            elif tabela == 'produtos':
                cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nome TEXT NOT NULL,
                                    quantidade INTEGER,
                                    preco DECIMAL)''')
        self.conn.commit()
        self.logger.info("Tabelas criadas/atualizadas com sucesso.")


class GerenciadorCRUD(GerenciadorDeBanco):
    def inserir(self, tabela, **campos):
        colunas = ', '.join(campos.keys())
        placeholders = ', '.join(['?'] * len(campos))
        sql = f'INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})'
        cursor = self.conn.cursor()
        cursor.execute(sql, list(campos.values()))
        self.conn.commit()

    def listar(self, tabela):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {tabela}')
        return cursor.fetchall()

    def alterar(self, tabela, id, **campos):
        colunas = ', '.join([f"{k} = ?" for k in campos.keys()])
        sql = f'UPDATE {tabela} SET {colunas} WHERE id = ?'
        cursor = self.conn.cursor()
        cursor.execute(sql, list(campos.values()) + [id])
        self.conn.commit()

    def exibir(self, tabela, id):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {tabela} WHERE id = ?', (id,))
        return cursor.fetchone()

    def remover(self, tabela, id):
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {tabela} WHERE id = ?', (id,))
        self.conn.commit()

    def pesquisar_por_nome(self, tabela, nome):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {tabela} WHERE nome LIKE ?', ('%'+nome+'%',))
        return cursor.fetchall()

def main():
    gerenciador = GerenciadorCRUD()

    # Insere clientes e produtos usando a mesma classe
    gerenciador.inserir('clientes', nome='Lucas Santos', email='lucas@example.com')
    gerenciador.inserir('produtos', nome='Dipirona', quantidade=100, preco=9.99)

    # Lista clientes e produtos
    print("\nListando todos os clientes:")
    for cliente in gerenciador.listar('clientes'):
        print(cliente)

    print("\nListando todos os produtos:")
    for produto in gerenciador.listar('produtos'):
        print(produto)

if __name__ == "__main__":
    main()
