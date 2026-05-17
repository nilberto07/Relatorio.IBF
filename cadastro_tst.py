import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Cadastro Financeiro", layout="wide")

st.title("Cadastro Financeiro - Google Sheets")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=0)
def carregar_dados():
    return conn.read()

# Carrega dados atuais
df = carregar_dados()

with st.form("form_cadastro"):
    st.subheader("Novo Lançamento")

    col1, col2, col3 = st.columns(3)

    with col1:
        ano = st.number_input("Ano", min_value=2000, max_value=2100, value=date.today().year)
        mes = st.selectbox(
            "Mês",
            ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        )
        data_referencia = st.date_input("Data Referência", value=date.today())

    with col2:
        igrejas = st.text_input("Igrejas")
        receitas = st.number_input("Receitas", min_value=0.0, format="%.2f")
        despesas = st.number_input("Despesas", min_value=0.0, format="%.2f")

    with col3:
        saldo_inicial = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f")
        caixa_templo = st.number_input("Caixa (Templo)", min_value=0.0, format="%.2f")
        observacoes = st.text_area("Observações")

    submitted = st.form_submit_button("Salvar")

if submitted:
    if not igrejas.strip():
        st.error("O campo 'Igrejas' é obrigatório.")
    else:
        nova_linha = pd.DataFrame([
            {
                "Ano": int(ano),
                "Mês": mes,
                "Data Referência": data_referencia.strftime("%Y-%m-%d"),
                "Igrejas": igrejas,
                "Receitas": receitas,
                "Despesas": despesas,
                "Saldo Inicial": saldo_inicial,
                "Caixa(Templo)": caixa_templo,
                "Observações": observacoes
            }
        ])

        df_atualizado = pd.concat([df, nova_linha], ignore_index=True)

        conn.update(
            data=df_atualizado
        )

        st.success("Registro salvo com sucesso!")
        st.cache_data.clear()
        st.rerun()

st.divider()
st.subheader("Dados Cadastrados")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum registro encontrado.")
