import streamlit as st
import os
from sqlalchemy import text


st.set_page_config(page_title="Gerenciar Funcionários", page_icon="💼", layout="wide")

# conn = st.connection("postgresql", type="sql")


# Pega a URL configurada no Render ou local
db_url = os.environ.get("STREAMLIT_CONNECTIONS_POSTGRESQL_URL") or os.environ.get("ST_CONNECTIONS_POSTGRESQL_URL")

if db_url:
    conn = st.connection("postgresql", type="sql", url=db_url)
else:
    conn = st.connection("postgresql", type="sql")

st.title("💼 Gestão de Funcionários")
st.markdown("Cadastre novos membros da equipe ou consulte os colaboradores ativos.")
st.markdown("---")

col_cadastro, col_lista = st.columns([1, 2])

with col_cadastro:
    st.subheader("📝 Cadastrar Funcionário")
    
    nome = st.text_input("Nome Completo")
    cpf = st.text_input("CPF")
    email = st.text_input("E-mail")
    cargo = st.selectbox("Cargo", ["Instrutor", "Recepção", "Gerente", "Limpeza"])
    
    if st.button("Salvar Colaborador"):
        if nome and cpf and email:
            try:
                with conn.session as session:
                    query = text("""
                        INSERT INTO funcionarios (nome, cpf, email, cargo, ativo)
                        VALUES (:nome, :cpf, :email, :cargo, TRUE);
                    """)
                    session.execute(query, {"nome": nome, "cpf": cpf, "email": email, "cargo": cargo})
                    session.commit()
                st.success(f"✅ {nome} cadastrado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error("Erro ao salvar no banco.")
                st.exception(e)
        else:
            st.warning("Preencha Nome, CPF e E-mail.")

with col_lista:
    st.subheader("🔍 Equipe Atual")
    try:
        dados = conn.query("SELECT id, nome, email, cargo, ativo FROM funcionarios ORDER BY id DESC;", ttl="0")
        if not dados.empty:
            st.dataframe(dados, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum funcionário registrado.")
    except Exception as e:
        st.error("Erro ao carregar lista.")