-- 05 - Tabela AGENDAMENTO_SERVICO (tabela de ligação)
-- Depende de: agendamento (INCLUI) e servico (REFERE)
-- A chave primária é COMPOSTA: o par (agendamento, serviço)

USE salao_beleza;

CREATE TABLE IF NOT EXISTS agendamento_servico (
    codigo_agendamento INT NOT NULL,
    codigo_servico     INT NOT NULL,
    valor_cobrado      DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (codigo_agendamento, codigo_servico),
    FOREIGN KEY (codigo_agendamento) REFERENCES agendamento(codigo_agendamento),
    FOREIGN KEY (codigo_servico)     REFERENCES servico(codigo_servico)
);

-- 05 - Dados de teste: AGENDAMENTO_SERVICO
-- Precisa que agendamento e servico já tenham dados.
-- (rode UMA vez só; rodar de novo dá erro de chave duplicada)
USE salao_beleza;

INSERT INTO agendamento_servico (codigo_agendamento, codigo_servico, valor_cobrado) VALUES
(1, 1,  80.00),
(1, 2,  60.00),
(2, 3,  50.00),
(3, 1,  80.00),
(4, 5, 120.00),
(5, 4,  55.00);

SELECT * FROM agendamento_servico;
