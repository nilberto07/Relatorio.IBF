import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl
from utils.theme import load_css

load_css()

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
    if valor == 0: return "—"
    valor_reais = valor / 100
    return f"R$ {valor_reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 


df_exibicao = df.copy()
# Aplica a formatação BR nas colunas de valores
for col in ["Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)"]:
    df_exibicao[col] = df_exibicao[col].apply(
        lambda v: formatar_brl(v) if pd.notna(v) else "—"
    )

df_exibicao["Observações"] = df_exibicao["Observações"] if df_exibicao["Observações"].notnull().any() else "—"

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
    st.markdown("""
    <div style='
                font-size:0.68rem; 
                text-transform:uppercase; 
                letter-spacing:0.12em; 
                margin-bottom:1rem; 
                padding-top:3rem;
                font-weight:700;
                border-bottom: 1px solid rgba(255,255,255,255);
                '>Filtros
                </div>
    """, unsafe_allow_html=True)

    filtro_igrejas = st.multiselect(label="Igrejas:", options=igrejas_disp, placeholder="Todas as igrejas")
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

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,255); margin-bottom:1.5rem;'>
    <div style='text-align:center; padding: 2rem 0 1.5rem;'>
        <div style='margin-bottom:0.5rem; display:flex; justify-content:center;'>
            <svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="opacity:0.95">
                <path d="M12 2L12 5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
                <path d="M10.5 4H13.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
                <path d="M5 10L12 5L19 10V21H5V10Z" stroke="white" stroke-width="1.7" stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
                <path d="M9 21V15C9 13.3431 10.3431 12 12 12C13.6569 12 15 13.3431 15 15V21" stroke="white" stroke-width="1.7" stroke-linejoin="round"/>
                <rect x="10.5" y="8" width="3" height="3" rx="0.5" stroke="white" stroke-width="1.4" fill="rgba(255,255,255,0.15)"/>
            </svg>
        </div>
        <div style='font-family:"Playfair Display",serif; font-size:1.1rem; font-weight:700; letter-spacing:0.04em;'>IBF</div>
        <div style='font-size:0.7rem; opacity:0.6; text-transform:uppercase; letter-spacing:0.1em; margin-top:2px;'>Sistema Financeiro</div>
    </div>
    """, unsafe_allow_html=True)

# ── Cards de Totais ──────────────────────────────────────────
total_rec  = df["Receitas"].sum()
total_desp = df["Despesas"].sum()
saldo_ini  = df["Saldo Inicial"].sum()
#caixa_tmp  = df["Caixa(Templo)"].sum()
liquido    = total_rec - total_desp
badge_class = "badge-pos" if liquido >= 0 else "badge-neg"
badge_sign  = "▲" if liquido >= 0 else "▼"
saldo_fim   = saldo_ini + liquido

df_caixa  = df[df["Caixa(Templo)"] > 0].sort_values(["Ano","Mês"], ascending=False)
caixa_tmp = df_caixa["Caixa(Templo)"].iloc[0] if not df_caixa.empty else 0.0

# EXPLICAÇÃO DO svg ESTA NO ARQUIVO NOTAS.TXT
SVG_RECEITAS = '''
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <path
            d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"
            stroke="#BF5223"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        />
    </svg>'''
SVG_DESPESAS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17 8 12 3 7 8" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="3" x2="12" y2="15" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round"/></svg>'
SVG_SALDO    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="#5A1F05" stroke-width="1.8"/><path d="M16 3H8a2 2 0 0 0-2 2v2h12V5a2 2 0 0 0-2-2Z" stroke="#5A1F05" stroke-width="1.8"/><circle cx="12" cy="14" r="2" stroke="#5A1F05" stroke-width="1.8"/></svg>'
SVG_CAIXA    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/><polyline points="9 22 9 12 15 12 15 22" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/></svg>'


st.markdown(f"""
<div class="dash-header">
    <h1>Dashboard Financeiro</h1>
    <p>Relatório · Assembleia Geral</p>
</div>
<div class="section-title">Resumo Financeiro</div>
<div class="kpi-grid">
    <div class="kpi-card receitas">
        <div class="kpi-inner">
            <div class="kpi-icon receitas">{SVG_RECEITAS}</div>
            <div class="kpi-body">
                <div class="kpi-label">Receitas</div>
                <div class="kpi-value">{formatar_brl(total_rec)}</div>
                <div class="kpi-sub">Entradas no período</div>
            </div>
        </div>
    </div>
    <div class="kpi-card despesas">
        <div class="kpi-inner">
            <div class="kpi-icon despesas">{SVG_DESPESAS}</div>
            <div class="kpi-body">
                <div class="kpi-label">Despesas</div>
                <div class="kpi-value">{formatar_brl(total_desp)}</div>
                <span class="kpi-badge {badge_class}">{badge_sign} Líquido: {formatar_brl(liquido)}</span>
            </div>
        </div>
    </div>
    <div class="kpi-card saldo">
        <div class="kpi-inner">
            <div class="kpi-icon saldo">{SVG_SALDO}</div>
            <div class="kpi-body">
                <div class="kpi-label">Saldo Líquido</div>
                <div class="kpi-value">{badge_sign} {formatar_brl(liquido)}</div>
                <div class="kpi-sub">Receita x Despesas</div>
            </div>
        </div>
    </div>
    <!--<div class="kpi-card saldo">
        <div class="kpi-inner">
            <div class="kpi-icon saldo">{SVG_SALDO}</div>
            <div class="kpi-body">
                <div class="kpi-label">Saldo Inicial</div>
                <div class="kpi-value">{formatar_brl(saldo_ini)}</div>
                <div class="kpi-sub">Patrimônio acumulado</div>
            </div>
        </div>
    </div>-->
    <div class="kpi-card caixa">
        <div class="kpi-inner">
            <div class="kpi-icon caixa">{SVG_CAIXA}</div>
            <div class="kpi-body">
                <div class="kpi-label">Caixa (Templo)</div>
                <div class="kpi-value">{formatar_brl(caixa_tmp)}</div>
                <div class="kpi-sub">Reserva para obras</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABLES
# ─────────────────────────────────────────────
## Resumo por Igreja
st.markdown('<div class="section-title">Resumo por Igreja</div>', unsafe_allow_html=True)
### Agrupa por igreja e soma os valores
df_sum = df.groupby("Igrejas").agg(
    Receitas=("Receitas","sum"), 
    Despesas=("Despesas","sum"),
    Saldo_Inicial=("Saldo Inicial","sum"), 
    #Caixa_Templo=("Caixa(Templo)","sum"),
    Caixa_Templo=("Caixa(Templo)", "last"), 
).reset_index()
### Soma o agregado para mostrar um total geral
df_sum["Líquido"] = df_sum["Receitas"] - df_sum["Despesas"]
df_sum["Saldo_Final"] = df_sum["Saldo_Inicial"] + df_sum["Líquido"]
### Ordena pela receita total (pode ser alterado para outro critério, como despesas ou saldo)
df_sum = df_sum.sort_values("Receitas", ascending=False).reset_index(drop=True)

for col in ["Receitas","Despesas","Saldo_Inicial","Caixa_Templo","Líquido","Saldo_Final"]:
    df_sum[col] = df_sum[col].apply(formatar_brl)
st.dataframe(
    df_sum.rename(columns={"Saldo_Inicial":"Saldo Inicial","Caixa_Templo":"Caixa (Templo)","Saldo_Final":"Saldo Final"}),
    column_order=["Igrejas","Receitas","Despesas","Líquido","Saldo Inicial","Saldo Final","Caixa (Templo)"],
    use_container_width=True, hide_index=True,
)

## Tabela Detalhada
st.markdown('<div class="section-title">Tabela Detalhada</div>', unsafe_allow_html=True)
st.dataframe(
    df_exibicao.rename(columns={"Data Referência":"Referência"}),
    use_container_width=True, 
    hide_index=True, 
    height=320,
    column_config=column_configuration,
)


st.space(size="medium")
