-- 06 - Tabela PAGAMENTO

USE salao_beleza;

CREATE TABLE IF NOT EXISTS pagamento (
    codigo_pagamento   INT AUTO_INCREMENT PRIMARY KEY,
    data_pagamento     DATE,
    valor              DECIMAL(10,2) NOT NULL,
    forma_pagamento    VARCHAR(30),
    status             VARCHAR(20) NOT NULL DEFAULT 'Pendente',
    codigo_agendamento INT NOT NULL UNIQUE,   -- FK
    FOREIGN KEY (codigo_agendamento) REFERENCES agendamento(codigo_agendamento)
);

-- 06 - Dados de teste: PAGAMENTO
-- Precisa que agendamento já tenha dados.
-- (rode UMA vez só; rodar de novo dá erro de valor duplicado)
USE salao_beleza;

INSERT INTO pagamento (data_pagamento, valor, forma_pagamento, status, codigo_agendamento) VALUES
('2026-10-05', 140.00, 'Pix',      'Pago',     1),
('2026-10-06',  50.00, 'Cartão',   'Pago',     2),
(NULL,          80.00, 'Dinheiro', 'Pendente', 3);

SELECT * FROM pagamento;
