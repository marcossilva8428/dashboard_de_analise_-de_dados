import sqlite3
import os

# Criar pasta database se não existir
if not os.path.exists('database'):
    os.makedirs('database')

# Conectar ao banco de dados (cria se não existir)
conn = sqlite3.connect('database/sales_data.db')
cursor = conn.cursor()

# Ler e executar o script schema.sql
with open('database/schema.sql', 'r') as f:
    schema_script = f.read()
    cursor.executescript(schema_script)

# Ler e executar o script seed_data.sql
with open('database/seed_data.sql', 'r') as f:
    seed_script = f.read()
    cursor.executescript(seed_script)

# Confirmar e fechar
conn.commit()
conn.close()

print("Banco de dados criado e populado com sucesso!")