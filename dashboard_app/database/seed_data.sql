-- Dados de exemplo para o dashboard de vendas

-- Inserir produtos
INSERT INTO products (name, category, price) VALUES
('Notebook Dell XPS', 'Eletrônicos', 8999.99),
('Monitor LG 24"', 'Eletrônicos', 1299.99),
('Teclado Mecânico', 'Periféricos', 349.99),
('Mouse Sem Fio', 'Periféricos', 129.99),
('SSD 1TB', 'Armazenamento', 699.99),
('HD Externo 2TB', 'Armazenamento', 499.99),
('Memória RAM 16GB', 'Componentes', 399.99),
('Processador Intel i7', 'Componentes', 1899.99),
('Placa de Vídeo RTX 3060', 'Componentes', 2499.99),
('Cadeira Gamer', 'Móveis', 1199.99),
('Mesa para Escritório', 'Móveis', 899.99),
('Fone de Ouvido Bluetooth', 'Áudio', 349.99),
('Caixa de Som JBL', 'Áudio', 499.99),
('Webcam HD', 'Periféricos', 299.99),
('Roteador WiFi', 'Redes', 299.99);

-- Inserir clientes
INSERT INTO customers (name, email, region) VALUES
('João Silva', 'joao.silva@email.com', 'Sudeste'),
('Maria Oliveira', 'maria.oliveira@email.com', 'Sudeste'),
('Pedro Santos', 'pedro.santos@email.com', 'Sul'),
('Ana Costa', 'ana.costa@email.com', 'Nordeste'),
('Lucas Pereira', 'lucas.pereira@email.com', 'Centro-Oeste'),
('Fernanda Almeida', 'fernanda.almeida@email.com', 'Norte'),
('Carlos Eduardo', 'carlos.eduardo@email.com', 'Sudeste'),
('Patricia Lima', 'patricia.lima@email.com', 'Nordeste'),
('Rafael Souza', 'rafael.souza@email.com', 'Sul'),
('Juliana Ferreira', 'juliana.ferreira@email.com', 'Centro-Oeste');

-- Inserir vendas (últimos 6 meses)
-- Janeiro
INSERT INTO sales (date, product_id, customer_id, quantity, amount) VALUES
('2025-01-05', 1, 2, 1, 8999.99),
('2025-01-10', 3, 1, 2, 699.98),
('2025-01-15', 5, 3, 1, 699.99),
('2025-01-20', 8, 4, 1, 1899.99),
('2025-01-25', 10, 5, 1, 1199.99);

-- Fevereiro
INSERT INTO sales (date, product_id, customer_id, quantity, amount) VALUES
('2025-02-03', 2, 6, 2, 2599.98),
('2025-02-08', 4, 7, 1, 129.99),
('2025-02-13', 6, 8, 1, 499.99),
('2025-02-18', 9, 9, 1, 2499.99),
('2025-02-23', 11, 10, 1, 899.99);

-- Março (mês atual)
INSERT INTO sales (date, product_id, customer_id, quantity, amount) VALUES
('2025-03-02', 12, 1, 1, 349.99),
('2025-03-07', 13, 2, 1, 499.99),
('2025-03-12', 14, 3, 2, 599.98),
('2025-03-14', 7, 4, 2, 799.98),
('2025-03-16', 15, 5, 1, 299.99);

-- Adicionar mais alguns dados distribuídos nas regiões
INSERT INTO sales (date, product_id, customer_id, quantity, amount) VALUES
-- Sudeste (mais vendas)
('2025-01-12', 2, 1, 1, 1299.99),
('2025-01-22', 4, 2, 2, 259.98),
('2025-02-05', 7, 7, 1, 399.99),
('2025-02-19', 10, 1, 1, 1199.99),
('2025-03-05', 13, 7, 1, 499.99),

-- Sul
('2025-01-08', 3, 3, 1, 349.99),
('2025-02-11', 8, 9, 1, 1899.99),
('2025-03-09', 5, 3, 2, 1399.98),

-- Nordeste
('2025-01-18', 12, 4, 1, 349.99),
('2025-02-15', 6, 8, 1, 499.99),
('2025-03-08', 9, 4, 1, 2499.99),

-- Centro-Oeste
('2025-01-28', 14, 5, 1, 299.99),
('2025-02-21', 1, 10, 1, 8999.99),
('2025-03-04', 11, 5, 1, 899.99),

-- Norte (menos vendas)
('2025-01-14', 15, 6, 1, 299.99),
('2025-02-25', 4, 6, 1, 129.99);