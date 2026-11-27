# Salão de Beleza: Projeto de Banco de Dados

Projeto acadêmico da disciplina de **Banco de Dados**. O sistema controla o dia a dia de um salão de beleza: quem atende, quem é atendido, quais serviços são feitos, quanto custa e se foi pago.

> **Banco:** `salao_beleza` | **SGBD:** MySQL 8.0.16 ou mais novo (necessário por causa do `CHECK`)

---

## Sumário

1. [Visão geral](#1-visão-geral)
2. [Estrutura dos arquivos](#2-estrutura-dos-arquivos)
3. [Item 1: Modelagem conceitual (MER)](#3-item-1-modelagem-conceitual-mer)
4. [Item 2: Modelo relacional](#4-item-2-modelo-relacional)
5. [Item 3: Normalização](#5-item-3-normalização)
6. [Item 4: Álgebra relacional](#6-item-4-álgebra-relacional)
7. [Item 5: DDL](#7-item-5-ddl)
8. [Item 6: DML](#8-item-6-dml)
9. [Item 7: View](#9-item-7-view)
10. [Item 8: Função e procedimento armazenado](#10-item-8-função-e-procedimento-armazenado)
11. [Item 9: Gatilho (trigger)](#11-item-9-gatilho-trigger)
12. [Item 10: Índice](#12-item-10-índice)
13. [Item 11: Transação e ACID](#13-item-11-transação-e-acid)
14. [Checklist dos requisitos](#14-checklist-dos-requisitos)
15. [Como executar](#15-como-executar)
16. [Perguntas que podem aparecer na apresentação](#16-perguntas-que-podem-aparecer-na-apresentação)
17. [Glossário](#17-glossário)

---

## 1. Visão geral

O salão precisa responder perguntas simples do dia a dia:

- Quem atende quem, e em que dia e horário?
- Quais serviços foram feitos em cada atendimento, e por quanto?
- O cliente já pagou?
- Quanto cada profissional faturou?

O banco tem **5 entidades** (profissional, cliente, serviço, agendamento, pagamento) e **6 tabelas**. A sexta tabela, `agendamento_servico`, nasce da relação N:M entre agendamento e serviço.

---

## 2. Estrutura dos arquivos

| Arquivo | Conteúdo |
|---|---|
| criação do banco | `CREATE DATABASE salao_beleza` |
| `01` profissional | tabela `profissional` + dados de teste |
| `02` cliente | tabela `cliente` + dados de teste |
| `03` servico | tabela `servico` (catálogo) + dados de teste |
| `04` agendamento | tabela `agendamento` + dados de teste |
| `05` agendamento_servico | tabela de ligação + dados de teste |
| `06` pagamento | tabela `pagamento` + dados de teste |
| `07` requisitos do projeto | itens 2 a 11 (normalização, álgebra, ALTER TABLE, DML, view, função, procedure, trigger, índice, transação) |

**Ordem de execução:** banco, depois `01` a `06` (nessa ordem, pois as tabelas dependem umas das outras), e por último o `07`.

---

## 3. Item 1: Modelagem conceitual (MER)

O **MER** (Modelo Entidade-Relacionamento) é o desenho que mostra as "coisas" do sistema (entidades), suas informações (atributos) e como se ligam (relacionamentos).

![MER do Salão de Beleza](imagens/mer_salao_de_beleza.drawio.pdf)

> O relacionamento **INCLUI** também tem um atributo próprio: `valor_cobrado`. Ele depende do par (agendamento, serviço), e por isso pertence ao relacionamento, não a uma das entidades.

### Cardinalidades

Cardinalidade responde: "quantos de um lado se ligam a quantos do outro?"

| Relacionamento | Entre | Cardinalidade | Tipo |
|---|---|---|---|
| ATENDE | PROFISSIONAL e AGENDAMENTO | 1:N | uma profissional atende vários agendamentos |
| REALIZA | CLIENTE e AGENDAMENTO | 1:N | uma cliente realiza vários agendamentos |
| GERA | AGENDAMENTO e PAGAMENTO | 1:1 | um agendamento gera no máximo um pagamento |
| INCLUI | AGENDAMENTO e SERVICO | **N:M** | um agendamento tem vários serviços, e um serviço aparece em vários agendamentos |

### Participação

Participação responde: "a entidade é **obrigada** a participar do relacionamento?"

- **Total** (obrigatória): linha **dupla** no desenho.
- **Parcial** (opcional): linha **simples**.

| Relacionamento | Lado | Participação | Motivo |
|---|---|---|---|
| ATENDE | AGENDAMENTO | **Total** | todo agendamento tem uma profissional |
| ATENDE | PROFISSIONAL | Parcial | pode existir profissional sem atendimentos |
| REALIZA | AGENDAMENTO | **Total** | todo agendamento tem uma cliente |
| REALIZA | CLIENTE | Parcial | pode existir cliente que nunca agendou |
| GERA | PAGAMENTO | **Total** | todo pagamento pertence a um agendamento |
| GERA | AGENDAMENTO | Parcial | um agendamento pode ainda não ter pagamento |
| INCLUI | AGENDAMENTO | **Total** | um agendamento precisa ter pelo menos um serviço |
| INCLUI | SERVICO | Parcial | um serviço do catálogo pode nunca ter sido usado |

---

## 4. Item 2: Modelo relacional

O **modelo relacional** é a tradução do MER para tabelas. Aqui aparece quem é **chave primária** (PK, a coluna que identifica cada linha) e **chave estrangeira** (FK, a coluna que aponta para a chave primária de outra tabela).

```
PROFISSIONAL (codigo_profissional [PK], nome, especialidade, email, telefone)

CLIENTE (codigo_cliente [PK], nome, data_nascimento, email, telefone)

SERVICO (codigo_servico [PK], nome, descricao, duracao_minutos, valor)

AGENDAMENTO (codigo_agendamento [PK], data_agendamento, horario, status,
             observacoes,
             codigo_profissional [FK], codigo_cliente [FK])

AGENDAMENTO_SERVICO (codigo_agendamento [PK, FK], codigo_servico [PK, FK],
                     valor_cobrado)

PAGAMENTO (codigo_pagamento [PK], data_pagamento, valor, forma_pagamento,
           status, codigo_agendamento [FK, UNIQUE])
```

### Regras usadas na conversão

1. **Cada entidade virou uma tabela.**
2. **1:N (ATENDE e REALIZA):** a FK vai para o lado do **N** (`agendamento`).
3. **1:1 (GERA):** a FK fica em `pagamento` e recebe `UNIQUE`, para impedir dois pagamentos no mesmo agendamento.
4. **N:M (INCLUI):** vira uma **tabela nova**, `agendamento_servico`. As duas FKs juntas formam a **chave primária composta**, e `valor_cobrado` vira coluna dela.

### De onde veio cada chave estrangeira

| Tabela | FK | Aponta para | Origem |
|---|---|---|---|
| `agendamento` | `codigo_profissional` | `profissional` | ATENDE (1:N) |
| `agendamento` | `codigo_cliente` | `cliente` | REALIZA (1:N) |
| `agendamento_servico` | `codigo_agendamento` | `agendamento` | INCLUI (N:M) |
| `agendamento_servico` | `codigo_servico` | `servico` | INCLUI (N:M) |
| `pagamento` | `codigo_agendamento` | `agendamento` | GERA (1:1) |

---

## 5. Item 3: Normalização

**Normalizar** é organizar as tabelas para não repetir informação e evitar erros. O projeto está na **3ª Forma Normal (3FN)**:

- **1FN:** cada coluna guarda um único valor (nada de listas dentro de uma célula).
- **2FN:** a única chave composta é a de `agendamento_servico`, e `valor_cobrado` depende do par (agendamento, serviço) inteiro.
- **3FN:** em todas as tabelas, cada coluna depende só da chave primária. Por exemplo, o nome da cliente **não** se repete em `agendamento`: fica em `cliente` e é buscado por `JOIN`.

### Decisão de normalização defendida

**Tabela `agendamento_servico`.** O erro a evitar seria guardar os serviços dentro de `agendamento`, em colunas `servico1`, `servico2`, `servico3`. Isso quebra a 1FN: limita a 3 serviços, deixa colunas vazias e complica consultas como "quem fez Manicure?". Com a tabela de ligação, cada serviço é **uma linha**, sem limite e sem desperdício.

**Decisão relacionada:** `valor_cobrado` guarda o **preço do momento**. Se o preço do catálogo (`servico.valor`) mudar, o histórico não muda. Isso é demonstrado no `UPDATE` do item 6.

---

## 6. Item 4: Álgebra relacional

A **álgebra relacional** é a forma matemática de descrever consultas.

| Símbolo | Significa | Equivale a |
|---|---|---|
| σ | seleção | `WHERE` |
| π | projeção | `SELECT` (escolher colunas) |
| ⨝ | junção | `JOIN` |
| γ | agrupamento | `GROUP BY` com `SUM`, `COUNT`... |

### Consulta 1: agenda de um dia

```
π c.nome, a.horario, p.nome, a.status (
  σ a.data_agendamento = '2026-10-05' (
    (Agendamento a ⨝ a.codigo_cliente = c.codigo_cliente Cliente c)
      ⨝ a.codigo_profissional = p.codigo_profissional Profissional p ) )
```

```sql
SELECT c.nome, a.horario, p.nome, a.status
FROM agendamento a
JOIN cliente c      ON a.codigo_cliente = c.codigo_cliente
JOIN profissional p ON a.codigo_profissional = p.codigo_profissional
WHERE a.data_agendamento = '2026-10-05';
```

**Resultado esperado:** Ana Paula | 14:00 | Camila Souza | Concluído

### Consulta 2: receita por profissional, só a partir de 100 (explicada na apresentação)

```
σ receita >= 100 (
  p.codigo_profissional, p.nome γ SUM(asv.valor_cobrado) → receita (
    σ a.status = 'Concluído' (
      (Profissional p ⨝ p.codigo_profissional = a.codigo_profissional Agendamento a)
        ⨝ a.codigo_agendamento = asv.codigo_agendamento AgendamentoServico asv ) ) )
```

**Resultado esperado:** Camila Souza | 140.00

**Explicação passo a passo:**

1. **Junções:** ligam a profissional aos seus agendamentos e aos serviços de cada um. Cada linha vira "profissional + um serviço feito". O agendamento 1 (corte + hidratação) gera 2 linhas.
2. **Seleção (`status = 'Concluído'`):** só atendimento realizado vira receita. Sobram o agendamento 1 (Camila, 80 + 60) e o 2 (Fernanda, 50).
3. **Agrupamento (γ):** soma o `valor_cobrado` por profissional. Camila = 140, Fernanda = 50.
4. **Seleção final (`receita >= 100`):** é o `HAVING`. Vem **depois** do agrupamento porque filtra o resultado da soma. Fernanda sai.

### Consulta 3: clientes com pagamento pendente

```
π c.nome, a.data_agendamento, pg.valor (
  σ pg.status = 'Pendente' (
    (Cliente c ⨝ c.codigo_cliente = a.codigo_cliente Agendamento a)
      ⨝ a.codigo_agendamento = pg.codigo_agendamento Pagamento pg ) )
```

```sql
SELECT c.nome, a.data_agendamento, pg.valor
FROM cliente c
JOIN agendamento a ON a.codigo_cliente = c.codigo_cliente
JOIN pagamento pg  ON pg.codigo_agendamento = a.codigo_agendamento
WHERE pg.status = 'Pendente';
```

**Resultado esperado (dados originais):** Ana Paula | 2026-10-08 | 80.00

---

## 7. Item 5: DDL

**DDL** (Data Definition Language) é a parte do SQL que **define a estrutura**: criar e alterar tabelas.

- **`CREATE TABLE`** (arquivos `01` a `06`): tipos adequados (`INT`, `VARCHAR`, `DATE`, `TIME`, `DECIMAL(10,2)`), `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `DEFAULT` e `UNIQUE` (em `pagamento.codigo_agendamento`).
- **`ALTER TABLE`** (item 5 do arquivo `08`, rodar **uma vez só**): adiciona as regras de negócio.

| Tabela | Restrição | Regra de negócio |
|---|---|---|
| `cliente` | `UNIQUE (email)` | e-mail não se repete (pode ser vazio) |
| `profissional` | `UNIQUE (email)` | idem |
| `servico` | `CHECK (duracao_minutos > 0)` | duração positiva |
| `servico` | `CHECK (valor >= 0)` | valor não negativo |
| `agendamento` | `CHECK (status IN ('Agendado','Concluído','Cancelado'))` | só 3 status |
| `agendamento_servico` | `CHECK (valor_cobrado >= 0)` | valor não negativo |
| `pagamento` | `CHECK (valor > 0)` | valor positivo |
| `pagamento` | `CHECK (status IN ('Pendente','Pago','Cancelado'))` | só 3 status |
| `pagamento` | `CHECK (forma_pagamento IS NULL OR ... IN ('Pix','Cartão','Dinheiro'))` | formas válidas |
| `pagamento` | `CHECK (status <> 'Pago' OR data_pagamento IS NOT NULL)` | pagamento "Pago" exige data |

---

## 8. Item 6: DML

**DML** (Data Manipulation Language) é a parte do SQL que **mexe nos dados**.

| Comando | Onde está |
|---|---|
| `INSERT` (povoamento) | arquivos `01` a `06` (dados de teste de cada tabela) |
| `INSERT` | novo cliente de teste (item 6) |
| `UPDATE ... WHERE` | sobe o preço de "Corte feminino" para 85,00 e depois volta para 80,00 |
| `DELETE ... WHERE` | remove o cliente de teste (ele não tem agendamentos) |
| `SELECT ... WHERE` | serviços com valor maior que 50 |
| `SELECT ... ORDER BY` | serviços do mais caro para o mais barato |
| `SELECT ... JOIN` | agenda de um dia, ligando 3 tabelas |
| `SELECT` com **subconsulta** | serviços acima da média de preço; clientes com atendimento concluído |
| `SELECT ... GROUP BY / HAVING` | receita por profissional, só a partir de 100 |

**Demonstração importante:** depois do `UPDATE` do preço para 85,00, a consulta mostra que o catálogo está em 85,00, mas o agendamento 1 continua com **80,00** em `valor_cobrado`. Isso prova a decisão de normalização do item 3.

---

## 9. Item 7: View

Uma **view** é uma "consulta salva" que se comporta como uma tabela virtual.

**Contexto:** a recepcionista precisa ver a agenda do dia (cliente, profissional, serviços, total e situação do pagamento), mas **não deve ver nem alterar as tabelas originais**. Por isso ela consulta só a view.

**`vw_agenda_recepcao`:**

- Junta **6 tabelas**.
- `GROUP_CONCAT` lista todos os serviços do atendimento **numa linha só**.
- `COALESCE` mostra `'Sem pagamento'` quando não existe pagamento (por isso o `LEFT JOIN` com `pagamento`).

**Usuário `recepcao`:** criado depois da view, com permissão **apenas de `SELECT` na view**:

```sql
CREATE USER IF NOT EXISTS 'recepcao'@'localhost' IDENTIFIED BY 'senha123';
GRANT SELECT ON salao_beleza.vw_agenda_recepcao TO 'recepcao'@'localhost';
```

> A senha é só para demonstração do trabalho. Em um sistema real, use uma senha forte.

**Exemplo de uso:** listar quem ainda precisa pagar (atendimentos não cancelados com pagamento `Pendente` ou `Sem pagamento`).

---

## 10. Item 8: Função e procedimento armazenado

Uma **função** recebe valores e **devolve um resultado**. Uma **stored procedure** executa uma **sequência de ações** guardada dentro do banco.

### Função `fn_total_agendamento`

**Contexto:** calcular o total de um atendimento, somando o `valor_cobrado` de todos os serviços. Devolve `0` se o agendamento não existir ou não tiver serviços.

```sql
SELECT fn_total_agendamento(1) AS total_ag1;   -- 140.00
SELECT fn_total_agendamento(999) AS inexistente; -- 0.00
```

Valores esperados para os agendamentos 1 a 5: **140, 50, 80, 120 e 55**.

### Procedure `sp_registrar_pagamento`

**Contexto:** registrar o pagamento de um agendamento, seguindo as regras do salão.

**Regras:**

- O agendamento precisa existir e **não** pode estar cancelado.
- Precisa ter serviços.
- Não pode já estar pago.
- Se existe pagamento `Pendente`, ele é **quitado**. Se não existe pagamento, ele é **criado**.
- Tudo dentro de uma **transação**: ou grava certo, ou desfaz tudo (`ROLLBACK` automático em qualquer erro).

```sql
CALL sp_registrar_pagamento(3, 'Pix');     -- quita o pendente (80.00)
CALL sp_registrar_pagamento(4, 'Cartão');  -- cria pagamento novo (120.00)
```

**Casos de erro testáveis:**

| Chamada | Mensagem |
|---|---|
| `CALL sp_registrar_pagamento(3, 'Pix');` (de novo) | Este agendamento já foi pago. |
| `CALL sp_registrar_pagamento(5, 'Pix');` | Agendamento cancelado não pode ser pago. |
| `CALL sp_registrar_pagamento(999, 'Pix');` | Agendamento não encontrado. |

---

## 11. Item 9: Gatilho (trigger)

Um **trigger** é um código que o banco executa **sozinho** quando algo acontece (inserir, alterar, apagar).

**`trg_agendamento_sem_conflito`** (`BEFORE INSERT` em `agendamento`)

**Regra de integridade:** ninguém atende duas pessoas ao mesmo tempo. O trigger impede dois atendimentos da **mesma profissional** no **mesmo dia e horário**. Agendamentos cancelados não contam.

**Demonstração:** a Camila já atende dia 08/10 às 16:00 (agendamento 3). Tentar inserir outro nesse horário gera:

```
ERROR 1644 (45000): Conflito: a profissional já tem atendimento neste dia e horário.
```

No mesmo dia, em horário livre (17:00), o `INSERT` funciona.

---

## 12. Item 10: Índice

Um **índice** funciona como o índice de um livro: o banco acha os dados sem ler tudo.

```sql
CREATE INDEX idx_agendamento_data_horario
    ON agendamento (data_agendamento, horario);
```

**Justificativa:** a agenda da recepção filtra por `data_agendamento` e ordena por `horario`. O índice composto já guarda os agendamentos organizados por (data, horário).

**Demonstração com `EXPLAIN`:**

| Situação | Resultado esperado |
|---|---|
| Sem o índice (`IGNORE INDEX`) | `type = ALL`: lê a tabela inteira |
| Com o índice (`FORCE INDEX`) | `type = ref`, `key = idx_agendamento_data_horario` |

> Com poucas linhas, o ganho de tempo não aparece. O que se mostra é a **mudança no plano** (`ALL` para `ref`), que em tabelas grandes faz muita diferença.

---

## 13. Item 11: Transação e ACID

Uma **transação** agrupa vários comandos para que aconteçam **juntos ou não aconteçam**.

**Contexto:** marcar um atendimento exige duas inserções (o agendamento e seus serviços). Se uma falhar, nenhuma pode ficar gravada.

- **(A) `COMMIT`:** insere o agendamento (15/10, 11:00) com Manicure e Pedicure e grava de forma definitiva. Total esperado na view: **105.00**.
- **(B) `ROLLBACK`:** insere um agendamento de teste, confere que o `COUNT` subiu **+1** (só nesta conexão) e desfaz tudo. O `COUNT` final volta ao valor de antes.

### Propriedades ACID

| Letra | Propriedade | Como aparece no projeto |
|---|---|---|
| **A** | Atomicidade | agendamento e serviços entram juntos ou nenhum entra; no caso (B), o `ROLLBACK` desfaz o agendamento de teste inteiro |
| **C** | Consistência | ao fim do `COMMIT` o banco continua válido: chaves estrangeiras, `CHECK`s e o trigger de conflito continuam respeitados |
| **I** | Isolamento | enquanto a transação não termina, o "+1" no `COUNT` só aparece nesta conexão; outros usuários não veem o agendamento pela metade |
| **D** | Durabilidade | depois do `COMMIT`, os dados ficam gravados mesmo que o servidor desligue em seguida |

---

## 14. Checklist dos requisitos

| # | Requisito | Onde está | Situação |
|---|---|---|---|
| 1 | MER (entidades, atributos, relacionamentos, cardinalidades, participação, 1:N e N:M) | seção 3 e desenho no draw.io | Atendido |
| 2 | Modelo relacional com PK e FK | seção 4 | Atendido |
| 3 | Normalização até a 3FN, com justificativa | seção 5 | Atendido |
| 4 | Três consultas em álgebra relacional, uma explicada | seção 6 | Atendido |
| 5 | DDL com tipos, PK, FK, NOT NULL, UNIQUE, CHECK e ALTER TABLE | seção 7 | Atendido |
| 6 | DML: INSERT, UPDATE, DELETE, WHERE, ORDER BY, JOIN, subconsulta, GROUP BY/HAVING | seção 8 | Atendido |
| 7 | View com contexto e código | seção 9 | Atendido |
| 8 | Função e stored procedure | seção 10 | Atendido |
| 9 | Trigger | seção 11 | Atendido |
| 10 | Índice com `EXPLAIN` | seção 12 | Atendido |
| 11 | Transação com `COMMIT`, `ROLLBACK` e ACID | seção 13 | Atendido |

---

## 15. Como executar

1. Abra o **MySQL Workbench** (ou o cliente `mysql`). Os blocos com `DELIMITER` (função, procedure e trigger) precisam de um deles.
2. Rode a criação do banco: `CREATE DATABASE IF NOT EXISTS salao_beleza;`
3. Rode os arquivos das tabelas **na ordem `01` a `06`**. Cada arquivo de dados de teste deve rodar **uma vez só**: rodar de novo duplica dados ou dá erro de chave duplicada.
4. Rode o arquivo `08`. O `ALTER TABLE` (item 5) também roda **uma vez só**.
5. Se quiser testar do zero, apague o banco com `DROP DATABASE salao_beleza;` e repita os passos.

> **Atenção aos resultados esperados:** eles valem para os **dados originais**. Depois que a procedure paga os agendamentos 3 e 4, alguns resultados mudam. Por exemplo, a consulta 3 da álgebra só mostra a Ana Paula com pendência antes dessa procedure rodar.

---

## 16. Perguntas que podem aparecer na apresentação

**Por que o N:M virou uma tabela?**
Porque uma célula não pode guardar vários serviços (quebraria a 1FN). A tabela `agendamento_servico` guarda um serviço por linha, sem limite, e ainda carrega o `valor_cobrado`.

**Por que `valor_cobrado` e não usar o valor do catálogo?**
Para o histórico não mudar. Se o preço do corte subir hoje, os atendimentos de ontem continuam com o valor que foi cobrado na época.

**O `pagamento.valor` não é calculável? Isso não fere a 3FN?**
Ele registra o valor **efetivamente cobrado** naquele momento (por exemplo, com desconto). Hoje a procedure o preenche com o total dos serviços.

**O trigger cobre alteração de horário?**
Hoje ele atua só no `INSERT`. Um `BEFORE UPDATE` com a mesma lógica fecharia essa brecha (melhoria possível).

**O índice ajuda com poucas linhas?**
No tempo, não. O que se demonstra é a mudança do `EXPLAIN` de `ALL` (lê tudo) para `ref` (usa o índice).

**O `ROLLBACK` desfaz o número do ID?**
Os dados são desfeitos, mas o contador do `AUTO_INCREMENT` não volta. O próximo agendamento pode "pular" um número, e isso é normal.

---

## 17. Glossário

| Termo | Significado simples |
|---|---|
| **Entidade** | uma "coisa" do sistema (cliente, serviço...) |
| **Atributo** | uma informação da entidade (nome, valor...) |
| **Relacionamento** | como duas entidades se ligam |
| **Cardinalidade** | quantos de um lado se ligam a quantos do outro (1:1, 1:N, N:M) |
| **Participação** | se a entidade é obrigada (total) ou não (parcial) a participar do relacionamento |
| **Chave primária (PK)** | coluna que identifica cada linha de forma única |
| **Chave estrangeira (FK)** | coluna que aponta para a chave primária de outra tabela |
| **Normalização** | organizar as tabelas para não repetir informação |
| **View** | consulta salva que funciona como tabela virtual |
| **Stored procedure** | sequência de comandos guardada no banco |
| **Trigger** | código que roda sozinho quando algo acontece na tabela |
| **Índice** | estrutura que acelera buscas, como o índice de um livro |
| **Transação** | grupo de comandos que acontecem juntos ou não acontecem |
| **ACID** | as 4 garantias de uma transação: Atomicidade, Consistência, Isolamento e Durabilidade |
