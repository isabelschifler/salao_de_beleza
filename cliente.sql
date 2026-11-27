-- 02 - Tabela CLIENTE

USE salao_beleza;

CREATE TABLE IF NOT EXISTS cliente (
    codigo_cliente  INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    email           VARCHAR(100),
    telefone        VARCHAR(20)
);

-- 02 - Dados de teste: CLIENTE
-- (rode UMA vez só; rodar de novo duplica os dados)
USE salao_beleza;

INSERT INTO cliente (nome, data_nascimento, email, telefone) VALUES
('Ana Paula',     '1998-05-12', 'ana@email.com',     '(47) 98888-1111'),
('Juliana Costa', '2000-09-30', 'juliana@email.com', '(47) 98888-2222'),
('Mariana Rocha', '1995-02-20', 'mariana@email.com', '(47) 98888-3333'),
('Larissa Dias',  '2002-11-08', 'larissa@email.com', '(47) 98888-4444');

SELECT * FROM cliente;
