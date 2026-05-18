import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

# Abas da planilha (gid obtido pela URL do Google Sheets)
ABAS = {
    "Página1": "0",
    "Página2": "1128666635",
    "Página3": "1066751161",
}
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet=ABAS["Página1"],
    ttl=0,       # sem cache, força releitura
    usecols=["Ano", "Mês", "Data Referência", "Igrejas",
              "Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)", "Observações"],
)

# Função para formatar valores monetários em BRL
def formatar_brl(valor: float) -> str:
    valor_reais = valor / 100
    return f"R$ {valor_reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


df_exibicao = df.copy()
# Aplica a formatação BR nas colunas de valores
for col in ["Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)"]:
    df_exibicao[col] = df_exibicao[col].apply(
        lambda v: formatar_brl(v) if pd.notna(v) else ""
    )

# Converte para numérico (erros viram NaN, que o sum() ignora)
df["Receitas"]      = pd.to_numeric(df["Receitas"],      errors="coerce")
df["Despesas"]      = pd.to_numeric(df["Despesas"],      errors="coerce")
df["Saldo Inicial"] = pd.to_numeric(df["Saldo Inicial"], errors="coerce")
df["Caixa(Templo)"] = pd.to_numeric(df["Caixa(Templo)"], errors="coerce")

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

    "Observações": st.column_config.TextColumn(
        "Observações",
        help="Observações sobre a Assembleia Geral",
    ),
}


# Para Filtro: lista de opções ordenadas e sem valores nulos
igrejas_disp = sorted(df["Igrejas"].dropna().unique()) if "Igrejas" in df.columns else []
anos_disp = sorted(df["Ano"].dropna().unique().astype(int)) if "Ano" in df.columns else []
meses_disp = sorted(df["Mês"].dropna().unique().astype(int)) if "Mês" in df.columns else []

# Sidebar
with st.sidebar:
    st.header("🔎 Filtros")

    filtro_igrejas = st.multiselect(label="Igrejas:", options=igrejas_disp, placeholder="Selecione uma ou mais igrejas")
    filtro_ano = st.multiselect("Ano:", options=anos_disp, placeholder="Todos os anos")
    filtro_mes = st.multiselect("Mês:", options=meses_disp, placeholder="Todos os meses")

    if filtro_igrejas:
        df_exibicao, df = df_exibicao[
            df_exibicao["Igrejas"].isin(filtro_igrejas)
        ], df[
            df["Igrejas"].isin(filtro_igrejas)
        ]
    if filtro_ano:
        df_exibicao, df = df_exibicao[
            df_exibicao["Ano"].isin(filtro_ano)
        ], df[
            df["Ano"].isin(filtro_ano)
        ]
    if filtro_mes:
        df_exibicao, df = df_exibicao[
            df_exibicao["Mês"].isin(filtro_mes)
        ], df[
            df["Mês"].isin(filtro_mes)
        ]


st.markdown("#### Relatório Assembleia Geral", text_alignment="center")

# ── Cards de Totais ──────────────────────────────────────────
st.space(size="small")
st.subheader("📊 Resumo Financeiro", divider="blue")

total_receitas      = df["Receitas"].sum()
total_despesas      = df["Despesas"].sum()
total_liquido       = df["Receitas"].sum() - df["Despesas"].sum()
total_saldo_inicial = df["Saldo Inicial"].sum()
total_caixa         = df["Caixa(Templo)"].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="📈 Receitas", value=formatar_brl(total_receitas))

with col2:
    st.metric(label="📉 Despesas", value=formatar_brl(total_despesas), 
              delta="Liquido: " + formatar_brl(total_liquido), delta_arrow="off", delta_color="blue"
            )

with col3:
    st.metric(label="🏦 Saldo Inicial", value=formatar_brl(total_saldo_inicial))

with col4:
    st.metric(label="🏛️ Caixa(Templo)", value=formatar_brl(total_caixa))

st.space(size="medium")
# ── Tabela ───────────────────────────────────────────────────
st.subheader("➡️ Tabela Detalhada", divider="blue")
st.dataframe(
    df_exibicao,
    width="stretch",
    hide_index=True,
    column_config=column_configuration,
)

