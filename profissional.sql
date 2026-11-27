-- 01 - Tabela PROFISSIONAL

USE salao_beleza;

CREATE TABLE IF NOT EXISTS profissional (
    codigo_profissional INT AUTO_INCREMENT PRIMARY KEY,
    nome                VARCHAR(100) NOT NULL,
    especialidade       VARCHAR(80),
    email               VARCHAR(100),
    telefone            VARCHAR(20)
);

-- 01 - Dados de teste: PROFISSIONAL
-- (rode UMA vez só; rodar de novo duplica os dados)
USE salao_beleza;

INSERT INTO profissional (nome, especialidade, email, telefone) VALUES
('Camila Souza',  'Cabeleireira', 'camila@salao.com',   '(47) 99999-1111'),
('Fernanda Lima', 'Manicure',     'fernanda@salao.com', '(47) 99999-2222'),
('Beatriz Alves', 'Esteticista',  'beatriz@salao.com',  '(47) 99999-3333');

SELECT * FROM profissional;
