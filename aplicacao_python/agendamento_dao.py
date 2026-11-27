"""
agendamento_dao.py - DAO dos agendamentos.

Aproveita o que já foi criado no banco:
  - vw_agenda_recepcao        (view, item 7)
  - fn_total_agendamento      (função, item 8)
  - sp_registrar_pagamento    (procedure, item 8)
  - trg_agendamento_sem_conflito (trigger, item 9: dispara no INSERT)
  - transação com COMMIT/ROLLBACK (item 11)

Todas as consultas são parametrizadas (%s).
"""


class AgendamentoDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def listar_agenda_do_dia(self, data):
        """Lê a VIEW da recepção. 'data' no formato AAAA-MM-DD."""
        sql = """SELECT codigo_agendamento, horario, cliente, profissional,
                        servicos, total_atendimento,
                        status_agendamento, status_pagamento
                   FROM vw_agenda_recepcao
                  WHERE data_agendamento = %s
                  ORDER BY horario"""
        cursor = self.conexao.cursor(dictionary=True)
        try:
            cursor.execute(sql, (data,))
            return cursor.fetchall()
        finally:
            cursor.close()

    def total_do_agendamento(self, codigo_agendamento):
        """Chama a FUNÇÃO do banco."""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT fn_total_agendamento(%s)", (codigo_agendamento,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def registrar_pagamento(self, codigo_agendamento, forma_pagamento):
        """
        Chama a PROCEDURE do banco. Ela valida as regras e faz sua própria
        transação. Se uma regra for violada, o MySQL levanta um erro com a
        mensagem (ex.: 'Este agendamento já foi pago.').
        Devolve o pagamento registrado (dicionário).
        """
        cursor = self.conexao.cursor()
        try:
            cursor.callproc("sp_registrar_pagamento",
                            (codigo_agendamento, forma_pagamento))
            pagamento = None
            for resultado in cursor.stored_results():
                colunas = [c[0] for c in resultado.description]
                linha = resultado.fetchone()
                if linha:
                    pagamento = dict(zip(colunas, linha))
            return pagamento
        finally:
            cursor.close()

    def marcar_atendimento(self, data, horario, observacoes,
                           codigo_profissional, codigo_cliente, codigos_servicos):
        """
        TRANSAÇÃO: grava o agendamento e seus serviços JUNTOS.
        Se qualquer passo falhar (inclusive o trigger de conflito de horário),
        o ROLLBACK desfaz tudo. Devolve o código do novo agendamento.
        """
        if not codigos_servicos:
            raise ValueError("Informe ao menos um serviço.")

        sql_agendamento = """INSERT INTO agendamento
            (data_agendamento, horario, status, observacoes,
             codigo_profissional, codigo_cliente)
            VALUES (%s, %s, 'Agendado', %s, %s, %s)"""

        # Só a QUANTIDADE de %s é montada aqui; os valores seguem como parâmetros.
        marcadores = ", ".join(["%s"] * len(codigos_servicos))
        sql_servicos = f"""INSERT INTO agendamento_servico
            (codigo_agendamento, codigo_servico, valor_cobrado)
            SELECT %s, codigo_servico, valor
              FROM servico
             WHERE codigo_servico IN ({marcadores})"""

        cursor = self.conexao.cursor()
        try:
            self.conexao.start_transaction()
            cursor.execute(sql_agendamento,
                           (data, horario, observacoes,
                            codigo_profissional, codigo_cliente))
            novo = cursor.lastrowid
            cursor.execute(sql_servicos, (novo, *codigos_servicos))
            self.conexao.commit()
            return novo
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cursor.close()
