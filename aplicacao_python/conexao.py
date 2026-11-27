"""
conexao.py - Abre a conexão com o banco salao_beleza.

Este é o único arquivo que sabe COMO conectar. Os DAOs só recebem a
conexão pronta, então se o servidor ou a senha mudarem, só este arquivo muda.

Configuração por variáveis de ambiente (assim a senha NÃO fica escrita no código):
    DB_HOST (padrão: localhost)   DB_PORT (padrão: 3306)
    DB_USER (padrão: root)        DB_PASSWORD (se faltar, o programa pergunta)
    DB_NAME (padrão: salao_beleza)
"""
import os
from getpass import getpass

import mysql.connector


def obter_conexao():
    """Devolve uma conexão aberta com o MySQL. Quem chama deve fechá-la."""
    senha = os.getenv("DB_PASSWORD")
    if senha is None:
        senha = getpass("Senha do MySQL: ")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=senha,
        database=os.getenv("DB_NAME", "salao_beleza"),
        charset="utf8mb4",
    )
