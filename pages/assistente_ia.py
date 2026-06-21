import streamlit as st
import google.generativeai as genai
from sqlalchemy import text
import re
import os

st.set_page_config(page_title="Assistente IA", page_icon="🤖", layout="wide")

st.title("🤖 Assistente de Inteligência Artificial")
st.markdown("Faça perguntas em linguagem natural sobre os dados da academia (ex: *'Quantos alunos ativos temos?'* ou *'Qual o faturamento?'*).")
st.markdown("---")

# >>> O BLOCO ANTIGO QUE ESTAVA AQUI FOI REMOVIDO PARA NÃO TRAVAR O RENDER <<<

# =====================================================================
# 1. CONFIGURAÇÃO DO BANCO DE DADOS (PostgreSQL)
# =====================================================================
db_url = os.environ.get("STREAMLIT_CONNECTIONS_POSTGRESQL_URL") or os.environ.get("ST_CONNECTIONS_POSTGRESQL_URL")

if db_url:
    conn = st.connection("postgresql", type="sql", url=db_url)
else:
    conn = st.connection("postgresql", type="sql")


# =====================================================================
# 2. CONFIGURAÇÃO DA INTELIGÊNCIA ARTIFICIAL (Gemini)
# =====================================================================
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash') # Ou 'gemini-2.5-flash' se preferir manter o mais novo
    except Exception as e:
        st.error(f"Erro ao inicializar o SDK do Gemini: {e}")
else:
    st.error("Chave GEMINI_API_KEY não foi encontrada no Render (Environment) nem no secrets.toml local.")

# 2. O SYSTEM PROMPT: Explicando as tabelas e regras de segurança para a IA
SCHEMA_SISTEMA = """
Você é um assistente especialista em banco de dados PostgreSQL para uma academia.
Sua única tarefa é ler a pergunta do usuário e gerar um comando SQL puro, válido e de APENAS LEITURA (SELECT) que responda à pergunta baseando-se nas tabelas abaixo:

Tabela 'funcionarios': id, nome, cpf, email, cargo, data_contratacao, ativo (BOOLEAN)
Tabela 'alunos': id, nome, cpf, email, telefone, data_cadastro, status_matricula ('Ativo', 'Inativo')
Tabela 'inventario': id, nome_equipamento, quantidade, data_aquisicao, status_conservacao ('Bom', 'Precisa de Manutenção', 'Quebrado')
Tabela 'pagamentos': id, aluno_id, valor_pago, data_pagamento, metodo_pagamento, referencia_mes_ano
Tabela 'compras': id, descricao, valor_total, data_compra, categoria

Regras Estritas:
1. Retorne APENAS o código SQL puro dentro de um bloco de código markdown, começando com ```sql e terminando com ```. Nenhum texto explicativo antes ou depois.
2. Nunca gere comandos de escrita como INSERT, UPDATE, DELETE ou DROP.
3. Se o usuário pedir algo fora do escopo do banco de dados, retorne apenas o texto: "FORA_DE_ESCOPO".
"""

# 3. Interface de Chat no Streamlit
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Exibe o histórico de mensagens na tela
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

# Entrada do usuário
if pergunta_usuario := st.chat_input("Como posso ajudar na gestão hoje?"):
    
    # Exibe a pergunta do funcionário no chat
    with st.chat_message("user"):
        st.write(pergunta_usuario)
    st.session_state.historico_chat.append({"role": "user", "content": pergunta_usuario})
    
    # Processamento da resposta
    with st.chat_message("assistant"):
        with st.spinner("Analisando dados do Neon..."):
            try:
                # Junta o Schema do sistema com a pergunta real do usuário
                prompt_final = f"{SCHEMA_SISTEMA}\n\nPergunta do Usuário: {pergunta_usuario}"
                resposta_ia = model.generate_content(prompt_final).text
                
                # Se a IA identificar que a pergunta foge do escopo ou tenta burlar o sistema
                if "FORA_DE_ESCOPO" in resposta_ia:
                    resposta_final = "Desculpe, só posso responder perguntas administrativas sobre as tabelas da academia."
                    st.write(resposta_final)
                else:
                    # Extrai o comando SQL gerado de dentro dos blocos de markdown ```sql ... ```
                    match = re.search(r'```sql\s*(.*?)\s*```', resposta_ia, re.DOTALL)
                    if match:
                        sql_gerado = match.group(1).strip()
                        
                        # Executa o comando gerado pela IA diretamente no Neon de forma segura
                        dados_busca = conn.query(sql_gerado, ttl="0")
                        
                        if not dados_busca.empty:
                            st.success("Dados encontrados:")
                            st.dataframe(dados_busca, use_container_width=True, hide_index=True)
                            resposta_final = f"Consulta executada com sucesso! Gerada a partir de: `{sql_gerado}`"
                        else:
                            resposta_final = "Nenhum registro correspondente foi encontrado no banco de dados."
                            st.info(resposta_final)
                    else:
                        resposta_final = "Não consegui estruturar uma consulta válida para essa pergunta."
                        st.warning(resposta_final)
                
                st.session_state.historico_chat.append({"role": "assistant", "content": resposta_final})
                
            except Exception as e:
                st.error("Ocorreu um erro ao processar a requisição inteligente.")
                st.exception(e)