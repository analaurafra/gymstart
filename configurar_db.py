import psycopg2

# ⚠️ COLE AQUI A SUA URL DE CONEXÃO DO NEON (A mesma do secrets.toml)
# DB_URL = "postgresql://usuario:senha@ep-string-do-neon.neon.tech/neondb?sslmode=require"
DB_URL = "postgresql://neondb_owner:npg_UQwfR9Iz7JxT@ep-wandering-bird-ad44f77r.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
sql_script = """
CREATE TABLE IF NOT EXISTS funcionarios (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    data_contratacao DATE DEFAULT CURRENT_DATE,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS alunos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    data_cadastro DATE DEFAULT CURRENT_DATE,
    status_matricula VARCHAR(20) DEFAULT 'Ativo'
);

CREATE TABLE IF NOT EXISTS inventario (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_equipamento VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    data_aquisicao DATE,
    status_conservacao VARCHAR(50) DEFAULT 'Bom'
);

CREATE TABLE IF NOT EXISTS pagamentos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    aluno_id INT,
    valor_pago DECIMAL(10, 2) NOT NULL,
    data_pagamento DATE DEFAULT CURRENT_DATE,
    metodo_pagamento VARCHAR(30) NOT NULL, 
    referencia_mes_ano VARCHAR(7) NOT NULL,
    CONSTRAINT fk_aluno FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compras (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    data_compra DATE DEFAULT CURRENT_DATE,
    categoria VARCHAR(50) NOT NULL
);
"""

try:
    print("Conectando ao Neon...")
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    
    print("Criando tabelas...")
    cursor.execute(sql_script)
    conn.commit()
    
    print("✅ Todas as tabelas foram criadas com sucesso no Neon!")
    
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Erro ao criar as tabelas:")
    print(e)