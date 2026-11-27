"""
main.py - Demonstração da conexão aplicação -> banco (salao_beleza).

Uso:
    python main.py            demonstração segura (não deixa dados novos)
    python main.py --marcar   também marca um atendimento (transação)
    python main.py --pagar    também registra o pagamento do agendamento 3

Antes de rodar: o banco precisa estar criado e populado (arquivos 01 a 08).
"""
import argparse

import mysql.connector

from agendamento_dao import AgendamentoDAO
from cliente_dao import ClienteDAO
from conexao import obter_conexao


def titulo(texto):
    print("\n" + "=" * 60)
    print(texto)
    print("=" * 60)


def demo_crud_cliente(clientes):
    titulo("1) CRUD de cliente com consultas parametrizadas")
    codigo = clientes.inserir("Cliente App", "1999-01-15",
                              "app.teste@email.com", "(47) 90000-0000")
    print("Inserido, código:", codigo)
    print("Buscar por id  :", clientes.buscar_por_id(codigo))
    print("Linhas alteradas no UPDATE:",
          clientes.atualizar_telefone(codigo, "(47) 91111-2222"))
    print("Depois do UPDATE:", clientes.buscar_por_id(codigo)["telefone"])
    print("Total de clientes:", len(clientes.listar()))
    print("Linhas removidas no DELETE:", clientes.remover(codigo))


def demo_sql_injection(clientes):
    titulo("2) SQL injection: versão INSEGURA x versão SEGURA")
    ataque = "' OR '1'='1"
    print("Texto digitado pelo atacante:", ataque)

    vazados = clientes.buscar_por_email_inseguro(ataque)
    print(f"\n[INSEGURA]  devolveu {len(vazados)} clientes (vazou tudo!)")

    protegidos = clientes.buscar_por_email(ataque)
    print(f"[SEGURA]    devolveu {len(protegidos)} clientes "
          "(o texto foi tratado como e-mail, não como comando)")


def demo_agendamentos(agenda):
    titulo("3) Agenda do dia (VIEW) e total (FUNÇÃO)")
    for linha in agenda.listar_agenda_do_dia("2026-10-05"):
        print(linha)
    print("Total do agendamento 1:", agenda.total_do_agendamento(1))


def demo_conflito_trigger(agenda):
    titulo("4) Transação com ROLLBACK: o TRIGGER barra o conflito")
    try:
        # Camila (profissional 1) já atende em 08/10 às 16:00
        agenda.marcar_atendimento("2026-10-08", "16:00:00", "Teste de conflito",
                                  1, 2, [1])
        print("Gravou (não era esperado).")
    except mysql.connector.Error as erro:
        print("Erro do banco:", erro.msg)
        print("Nada foi gravado: o ROLLBACK desfez a transação.")


def demo_marcar(agenda):
    titulo("5) Transação com COMMIT: marcar atendimento")
    try:
        novo = agenda.marcar_atendimento("2026-10-20", "10:00:00",
                                         "Marcado pela aplicação", 1, 1, [1, 2])
        print("Agendamento criado, código:", novo)
        print("Total:", agenda.total_do_agendamento(novo))
    except mysql.connector.Error as erro:
        print("Erro do banco:", erro.msg)


def demo_pagar(agenda):
    titulo("6) PROCEDURE: registrar pagamento do agendamento 3")
    try:
        print(agenda.registrar_pagamento(3, "Pix"))
    except mysql.connector.Error as erro:
        print("Erro do banco:", erro.msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--marcar", action="store_true")
    parser.add_argument("--pagar", action="store_true")
    args = parser.parse_args()

    conexao = obter_conexao()
    try:
        clientes = ClienteDAO(conexao)
        agenda = AgendamentoDAO(conexao)

        demo_crud_cliente(clientes)
        demo_sql_injection(clientes)
        demo_agendamentos(agenda)
        demo_conflito_trigger(agenda)
        if args.marcar:
            demo_marcar(agenda)
        if args.pagar:
            demo_pagar(agenda)
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
