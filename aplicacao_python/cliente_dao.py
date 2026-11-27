"""
cliente_dao.py - DAO (Data Access Object) da tabela cliente.

PADRÃO DAO: toda a conversa SQL com a tabela cliente fica nesta classe.
O resto do programa chama métodos como buscar_por_id(1) e não precisa
saber SQL.

PREVENÇÃO DE SQL INJECTION: todas as consultas usam parâmetros (%s).
O valor viaja SEPARADO do texto SQL, então o banco o trata sempre como
dado, nunca como comando.
"""


class ClienteDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    # ---------- CREATE ----------
    def inserir(self, nome, data_nascimento, email, telefone):
        """Insere um cliente e devolve o código gerado."""
        sql = """INSERT INTO cliente (nome, data_nascimento, email, telefone)
                 VALUES (%s, %s, %s, %s)"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute(sql, (nome, data_nascimento, email, telefone))
            self.conexao.commit()
            return cursor.lastrowid
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cursor.close()

    # ---------- READ ----------
    def buscar_por_id(self, codigo_cliente):
        sql = "SELECT * FROM cliente WHERE codigo_cliente = %s"
        return self._um(sql, (codigo_cliente,))

    def buscar_por_email(self, email):
        """Versão SEGURA: o e-mail vai como parâmetro."""
        sql = "SELECT * FROM cliente WHERE email = %s"
        return self._varios(sql, (email,))

    def buscar_por_email_inseguro(self, email):
        """
        ATENÇÃO: SÓ PARA DEMONSTRAÇÃO. NUNCA faça isto em um sistema real.
        Aqui o texto digitado é colado dentro do SQL (concatenação), então
        quem digitar  ' OR '1'='1  muda o sentido da consulta.
        """
        sql = "SELECT * FROM cliente WHERE email = '" + email + "'"
        return self._varios(sql, None)

    def listar(self):
        return self._varios("SELECT * FROM cliente ORDER BY nome", None)

    # ---------- UPDATE ----------
    def atualizar_telefone(self, codigo_cliente, novo_telefone):
        """Devolve quantas linhas foram alteradas (0 ou 1)."""
        sql = "UPDATE cliente SET telefone = %s WHERE codigo_cliente = %s"
        return self._alterar(sql, (novo_telefone, codigo_cliente))

    # ---------- DELETE ----------
    def remover(self, codigo_cliente):
        """Devolve quantas linhas foram removidas (0 ou 1)."""
        sql = "DELETE FROM cliente WHERE codigo_cliente = %s"
        return self._alterar(sql, (codigo_cliente,))

    # ---------- auxiliares internos ----------
    def _varios(self, sql, parametros):
        cursor = self.conexao.cursor(dictionary=True)
        try:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            cursor.close()

    def _um(self, sql, parametros):
        linhas = self._varios(sql, parametros)
        return linhas[0] if linhas else None

    def _alterar(self, sql, parametros):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(sql, parametros)
            self.conexao.commit()
            return cursor.rowcount
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cursor.close()
