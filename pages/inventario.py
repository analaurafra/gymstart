import streamlit as st
import os
from sqlalchemy import text

st.set_page_config(page_title="Inventário", page_icon="🏋️", layout="wide")

# conn = st.connection("postgresql", type="sql")


# Pega a URL configurada no Render ou local
db_url = os.environ.get("STREAMLIT_CONNECTIONS_POSTGRESQL_URL") or os.environ.get("ST_CONNECTIONS_POSTGRESQL_URL")

if db_url:
    conn = st.connection("postgresql", type="sql", url=db_url)
else:
    conn = st.connection("postgresql", type="sql")

st.title("🏋️ Inventário de Equipamentos")
st.markdown("Controle de máquinas, halteres e status de manutenção.")
st.markdown("---")

col_cadastro, col_lista = st.columns([1, 2])

with col_cadastro:
    st.subheader("📦 Adicionar ao Inventário")
    
    nome_equipamento = st.text_input("Nome do Equipamento (Ex: Esteira X)")
    quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
    status_conservacao = st.selectbox("Status Inicial", ["Bom", "Precisa de Manutenção", "Quebrado"])
    
    if st.button("Registrar Equipamento"):
        if nome_equipamento:
            try:
                with conn.session as session:
                    query = text("""
                        INSERT INTO inventario (nome_equipamento, quantidade, data_aquisicao, status_conservacao)
                        VALUES (:nome, :qtd, CURRENT_DATE, :status);
                    """)
                    session.execute(query, {"nome": nome_equipamento, "qtd": quantidade, "status": status_conservacao})
                    session.commit()
                st.success(f"📦 {nome_equipamento} adicionado!")
                st.rerun()
            except Exception as e:
                st.error("Erro ao salvar.")
                st.exception(e)
        else:
            st.warning("O nome do equipamento é obrigatório.")

with col_lista:
    st.subheader("🔍 Itens Cadastrados")
    try:
        dados = conn.query("SELECT id, nome_equipamento, quantidade, status_conservacao FROM inventario ORDER BY id DESC;", ttl="0")
        if not dados.empty:
            st.dataframe(dados, use_container_width=True, hide_index=True)
        else:
            st.info("Inventário vazio.")
    except Exception as e:
        st.error("Erro ao carregar inventário.")