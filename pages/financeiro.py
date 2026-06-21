import streamlit as st
from sqlalchemy import text

st.set_page_config(page_title="Financeiro", page_icon="💰", layout="wide")

# conn = st.connection("postgresql", type="sql")

import os
import streamlit as st

# Pega a URL configurada no Render ou local
db_url = os.environ.get("STREAMLIT_CONNECTIONS_POSTGRESQL_URL") or os.environ.get("ST_CONNECTIONS_POSTGRESQL_URL")

if db_url:
    conn = st.connection("postgresql", type="sql", url=db_url)
else:
    conn = st.connection("postgresql", type="sql")

st.title("💰 Gestão Financeira")
st.markdown("Fluxo de caixa: Registro de mensalidades recebidas e despesas da unidade.")
st.markdown("---")

aba_pagamentos, aba_compras = st.tabs(["💵 Receber Mensalidade", "📉 Registrar Despesa/Compra"])

# ----------------- ABA 1: PAGAMENTOS DE ALUNOS -----------------
with aba_pagamentos:
    c_cad, c_list = st.columns([1, 2])
    
    with c_cad:
        st.subheader("💳 Novo Recebimento")
        try:
            # Busca os alunos existentes para colocar num campo de seleção (Selectbox)
            alunos_df = conn.query("SELECT id, nome FROM alunos ORDER BY nome;", ttl="0")
            lista_alunos = {row['nome']: row['id'] for _, row in alunos_df.iterrows()}
            
            if lista_alunos:
                aluno_selecionado = st.selectbox("Selecione o Aluno", list(lista_alunos.keys()))
                aluno_id = lista_alunos[aluno_selecionado]
                
                valor = st.number_input("Valor Pago (R$)", min_value=0.0, value=120.00)
                metodo = st.selectbox("Método", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
                referencia = st.text_input("Mês/Ano de Referência (Ex: 06/2026)", value="06/2026")
                
                if st.button("Confirmar Pagamento"):
                    with conn.session as session:
                        query = text("""
                            INSERT INTO pagamentos (aluno_id, valor_pago, metodo_pagamento, referencia_mes_ano)
                            VALUES (:aluno_id, :valor, :metodo, :ref);
                        """)
                        session.execute(query, {"aluno_id": aluno_id, "valor": valor, "metodo": metodo, "ref": referencia})
                        session.commit()
                    st.success("Pagamento registrado!")
                    st.rerun()
            else:
                st.warning("Cadastre um aluno primeiro antes de receber pagamentos.")
        except Exception as e:
            st.error("Erro na seção de pagamentos.")

    with c_list:
        st.subheader("📊 Histórico de Mensalidades")
        try:
            dados_pag = conn.query("""
                SELECT p.id, a.nome as aluno, p.valor_pago, p.data_pagamento, p.referencia_mes_ano 
                FROM pagamentos p 
                JOIN alunos a ON p.aluno_id = a.id 
                ORDER BY p.id DESC;
            """, ttl="0")
            st.dataframe(dados_pag, use_container_width=True, hide_index=True)
        except:
            st.info("Nenhum pagamento registrado.")

# ----------------- ABA 2: COMPRAS E DESPESAS -----------------
with aba_compras:
    c_cad_compra, c_list_compra = st.columns([1, 2])
    
    with c_cad_compra:
        st.subheader("📉 Nova Despesa")
        descricao = st.text_input("Descrição da Compra (Ex: Conta de Luz, Novos Halteres)")
        valor_total = st.number_input("Valor Total (R$)", min_value=0.0, value=50.0)
        categoria = st.selectbox("Categoria", ["Equipamentos", "Infraestrutura", "Suplementos", "Limpeza", "Outros"])
        
        if st.button("Salvar Despesa"):
            if descricao:
                try:
                    with conn.session as session:
                        query = text("""
                            INSERT INTO compras (descricao, valor_total, categoria)
                            VALUES (:desc, :valor, :cat);
                        """)
                        session.execute(query, {"desc": descricao, "valor": valor_total, "cat": categoria})
                        session.commit()
                    st.success("Despesa registrada!")
                    st.rerun()
                except Exception as e:
                    st.error("Erro ao salvar despesa.")
            else:
                st.warning("Insira uma descrição.")

    with c_list_compra:
        st.subheader("📊 Histórico de Compras/Gastos")
        try:
            dados_comp = conn.query("SELECT id, descricao, valor_total, data_compra, categoria FROM compras ORDER BY id DESC;", ttl="0")
            st.dataframe(dados_comp, use_container_width=True, hide_index=True)
        except:
            st.info("Nenhuma despesa registrada.")