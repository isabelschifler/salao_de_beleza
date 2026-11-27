-- 04 - Tabela AGENDAMENTO

USE salao_beleza;

CREATE TABLE IF NOT EXISTS agendamento (
    codigo_agendamento  INT AUTO_INCREMENT PRIMARY KEY,
    data_agendamento    DATE NOT NULL,
    horario             TIME NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'Agendado',
    observacoes         VARCHAR(255),
    codigo_profissional INT NOT NULL,   -- FK: quem atende
    codigo_cliente      INT NOT NULL,   -- FK: quem foi atendida
    FOREIGN KEY (codigo_profissional) REFERENCES profissional(codigo_profissional),
    FOREIGN KEY (codigo_cliente)      REFERENCES cliente(codigo_cliente)
);

-- 04 - Dados de teste: AGENDAMENTO
-- Precisa que profissional e cliente já tenham dados.
-- (rode UMA vez só; rodar de novo duplica os dados)
USE salao_beleza;

INSERT INTO agendamento (data_agendamento, horario, status, observacoes, codigo_profissional, codigo_cliente) VALUES
('2026-10-05', '14:00:00', 'Concluído', 'Primeira vez no salão', 1, 1),
('2026-10-06', '10:30:00', 'Concluído', NULL,                    2, 2),
('2026-10-08', '16:00:00', 'Agendado',  NULL,                    1, 1),
('2026-10-09', '09:00:00', 'Agendado',  'Pele sensível',         3, 3),
('2026-10-10', '15:00:00', 'Cancelado', 'Cliente desmarcou',     2, 3);

SELECT * FROM agendamento;
