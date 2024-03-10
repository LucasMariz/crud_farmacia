import sqlite3

def conectar_banco():
    return sqlite3.connect('farmacia.db')