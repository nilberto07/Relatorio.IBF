import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

st.header("Relatório Assembleia Geral")

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

column_configuration = {
    "Ano": st.column_config.NumberColumn(
        "Ano",
        help="Ano da Assembleia Geral",
    ),

    "Mês": st.column_config.NumberColumn(
        "Mês",
        help="Mês da Assembleia Geral",
    ),

    "Data Referência": st.column_config.DateColumn(
        "Data Referência",
        help="Data de referência da Assembleia Geral",
        format="MMM/YYYY"
    ),

    "Igrejas": st.column_config.TextColumn(
        "Igrejas",
        help="Igreja participante da Assembleia Geral",
    ),

    "Receitas": st.column_config.NumberColumn(
        "Receitas",
        help="Valor das receitas da Assembleia Geral",
        format="R$ %.3f",
        min_value=0,
    ),

    "Despesas": st.column_config.NumberColumn(
        "Despesas",
        help="Valor das despesas da Assembleia Geral",
        format="R$ %.3f",
        min_value=0,
        step=0.01,
    ),

    "Saldo Inicial": st.column_config.NumberColumn(
        "Saldo Inicial",
        help="Valor do saldo inicial da Assembleia Geral",
        format="R$ %.3f",
        min_value=0,
        step=0.01,
    ),

    "Caixa(Templo)": st.column_config.NumberColumn(
        "Caixa(Templo)",
        help="Valor do saldo em caixa do templo",
        format="R$ %.3f",
        min_value=0,
        step=0.01,
    ),

    "Observações": st.column_config.TextColumn(
        "Observações",
        help="Observações sobre a Assembleia Geral",
    ),
}


# Colunas:
# Lista de opções ordenadas e sem valores nulos
opcoes_igrejas = sorted(df["Igrejas"].dropna().unique())

# Sidebar
with st.sidebar:
    st.header("🔎 Filtros")

    filtro_igrejas = st.multiselect(
        label="Igrejas:",
        options=opcoes_igrejas,
        placeholder="Selecione uma ou mais igrejas"
    )

    if filtro_igrejas:
        df = df[
            df["Igrejas"].isin(filtro_igrejas)
        ]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config=column_configuration,
)


pivolt_tb = df.pivot_table(index="Ano", columns="Igrejas", values="Receitas")
st.dataframe(
    pivolt_tb,
    use_container_width=True,
    hide_index=True,
    column_config=column_configuration,
)