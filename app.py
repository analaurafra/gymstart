import streamlit as st
from sqlalchemy import text

# Configuração da página
st.set_page_config(page_title="Gestão Academia", page_icon="🏋️", layout="centered")

# Conexão com o Banco de Dados Neon (lê o secrets.toml automaticamente)

import os

# Tenta pegar a URL do Render, se não achar, usa a string padrão
db_url = os.environ.get("ST_CONNECTIONS_POSTGRESQL_URL") or os.environ.get("STREAMLIT_CONNECTIONS_POSTGRESQL_URL")

if db_url:
    # Passa a conexão diretamente via código (kwargs)
    conn = st.connection("postgresql", type="sql", url=db_url)
else:
    # Fallback para quando você estiver rodando localmente com secrets.toml
    conn = st.connection("postgresql", type="sql")

st.title("🏋️ Painel Administrativo - Academia")
st.markdown("---")

# Criando a interface de cadastro (Frontend)
st.subheader("Cadastrar Novo Aluno")

# Campos que o funcionário vai preencher
nome = st.text_input("Nome Completo do Aluno")
cpf = st.text_input("CPF (Apenas números)")
email = st.text_input("E-mail")
telefone = st.text_input("Telefone de Contato")

# Botão para salvar (Lógica de Backend integrada)
if st.button("Salvar Cadastro"):
    if nome and cpf: # Validação simples para não enviar campos vazios
        try:
            with conn.session as session:
                # Verifica se o CPF já existe para evitar violação de unicidade
                existing = session.execute(
                    text("SELECT 1 FROM alunos WHERE cpf = :cpf"),
                    {"cpf": cpf}
                ).fetchone()

                if existing:
                    st.warning("CPF já cadastrado. Verifique os dados ou use outro CPF.")
                else:
                    query = """
                        INSERT INTO alunos (nome, cpf, email, telefone, status_matricula) 
                        VALUES (:nome, :cpf, :email, :telefone, 'Ativo')
                    """
                    session.execute(text(query), {"nome": nome, "cpf": cpf, "email": email, "telefone": telefone})
                    session.commit()

                    st.success(f"Aluno {nome} cadastrado com sucesso no Neon!")
        except Exception as e:
            st.error("Erro ao salvar no banco de dados.")
            st.exception(e)
    else:
        st.warning("Por favor, preencha pelo menos o Nome e o CPF.")