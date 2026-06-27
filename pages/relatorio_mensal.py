import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl
from datetime import datetime
from utils.theme import load_css

load_css()
ssl._create_default_https_context = ssl._create_stdlib_context

# ─────────────────────────────────────────────
#  CONEXÃO
# ─────────────────────────────────────────────
ABAS = {
    "Página1": "0",
    "Página2": "1128666635",
    "Página3": "1066751161",
}
conn = st.connection("gsheets", type=GSheetsConnection)

df_raw = conn.read(
    worksheet=ABAS["Página1"],
    ttl=0,
    usecols=["Indice", "Ano", "Mês", "Data Referência", "Igrejas",
             "Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)", "Observações"],
)

# ─────────────────────────────────────────────
#  TIPOS NUMÉRICOS — sempre antes de qualquer cálculo
# ─────────────────────────────────────────────
for col in ["Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)"]:
    df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0)

df_raw["Ano"] = pd.to_numeric(df_raw["Ano"], errors="coerce")
df_raw["Mês"] = pd.to_numeric(df_raw["Mês"], errors="coerce")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def formatar_brl(valor: float) -> str:
    if pd.isna(valor) or valor == 0:
        return "—"
    valor_reais = valor / 100
    return f"R$ {valor_reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def badge(v: float) -> str:
    seta  = "&#9650;" if v >= 0 else "&#9660;"
    bg    = "#E8F7EC" if v >= 0 else "#FDEAEA"
    cor   = "#1E7A3C" if v >= 0 else "#C0392B"
    texto = formatar_brl(v)
    return (
        '<span style="display:inline-block;font-size:0.7rem;font-weight:700;'
        f'padding:2px 8px;border-radius:20px;background:{bg};color:{cor};white-space:nowrap">'
        f'{seta} {texto}</span>'
    )

# ─────────────────────────────────────────────
#  SIDEBAR — FILTROS
# ─────────────────────────────────────────────
igrejas_disp = sorted(df_raw["Igrejas"].dropna().unique())
anos_disp    = sorted(df_raw["Ano"].dropna().unique().astype(int))
meses_disp   = sorted(df_raw["Mês"].dropna().unique().astype(int))

with st.sidebar:
    st.markdown("""
    <div style='font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;
                margin-bottom:1rem;padding-top:3rem;font-weight:700;
                border-bottom:1px solid rgba(255,255,255,0.3);'>Filtros</div>
    """, unsafe_allow_html=True)

    filtro_igrejas = st.multiselect("Igrejas:", options=igrejas_disp, placeholder="Selecione...")
    filtro_ano     = st.multiselect("Ano:",     options=anos_disp,    placeholder="Selecione...")
    filtro_mes     = st.multiselect("Mês:",     options=meses_disp,   placeholder="Selecione...")

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.2); margin:1.5rem 0 1rem;'>
    <div style='text-align:center; padding: 1rem 0'>
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L12 5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M10.5 4H13.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M5 10L12 5L19 10V21H5V10Z" stroke="white" stroke-width="1.7"
                  stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
            <path d="M9 21V15C9 13.3431 10.3431 12 12 12C13.6569 12 15 13.3431 15 15V21"
                  stroke="white" stroke-width="1.7" stroke-linejoin="round"/>
            <rect x="10.5" y="8" width="3" height="3" rx="0.5"
                  stroke="white" stroke-width="1.4" fill="rgba(255,255,255,0.15)"/>
        </svg>
        <div style='font-family:"Playfair Display",serif;font-size:1rem;font-weight:700;margin-top:6px;'>IBF</div>
        <div style='font-size:0.68rem;opacity:0.6;text-transform:uppercase;letter-spacing:.1em;margin-top:2px;'>
            Sistema Financeiro</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  APLICA FILTROS
# ─────────────────────────────────────────────
df = df_raw.copy()
if filtro_igrejas:
    df = df[df["Igrejas"].isin(filtro_igrejas)]
if filtro_ano:
    df = df[df["Ano"].isin(filtro_ano)]
if filtro_mes:
    df = df[df["Mês"].isin(filtro_mes)]

# ─────────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="dash-header">
        <h1>Relatório Financeiro IBF</h1>
        <p>Três últimos meses · Gerado em {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RENDER MONTH BLOCK
# ─────────────────────────────────────────────
def render_month_block(label: str, df_mes: pd.DataFrame) -> str:
    # Cálculos ANTES de qualquer formatação
    #df_mes = df_mes.sort_values("Receitas", ascending=False).copy()
    df_mes = df_mes.sort_values("Indice", ascending=True).copy()
    df_mes["Liquido"]     = df_mes["Receitas"] - df_mes["Despesas"]
    df_mes["Saldo Final"] = df_mes["Saldo Inicial"] + df_mes["Liquido"]

    tot_rec = df_mes["Receitas"].sum()
    tot_des = df_mes["Despesas"].sum()
    tot_liq = tot_rec - tot_des
    tot_si  = df_mes["Saldo Inicial"].sum()
    tot_sf  = df_mes["Saldo Final"].sum()
    df_cx   = df_mes[df_mes["Caixa(Templo)"] > 0].sort_values("Caixa(Templo)", ascending=False)
    tot_cx  = df_cx["Caixa(Templo)"].iloc[0] if not df_cx.empty else 0.0

    # Observações — monta como lista de strings e junta com join
    obs_rows = df_mes[["Igrejas", "Observações"]].copy()
    obs_rows = obs_rows[
        obs_rows["Observações"].notna() &
        (obs_rows["Observações"].astype(str).str.strip() != "") &
        (obs_rows["Observações"].astype(str).str.strip() != "—")
    ]

    if not obs_rows.empty:
        partes = []
        for _, row in obs_rows.iterrows():
            igreja = str(row["Igrejas"])
            texto  = str(row["Observações"])
            partes.append(
                '<span style="color:#5A1F05;font-weight:700">' + igreja + ':</span> '
                '<span style="color:#5A3D2B">' + texto + '</span>'
            )
        obs_html = (
            '<div style="padding:6px 16px 8px;background:#FDF6F0;border-top:1px solid #E8D5C8;'
            'font-size:0.75rem;line-height:1.8">'
            '<span style="font-weight:700;text-transform:uppercase;letter-spacing:.08em;'
            'color:#9E7E6A;margin-right:8px">Obs.:</span>'
            + ' &nbsp;·&nbsp; '.join(partes) +
            '</div>'
        )
    else:
        obs_html = ""

    # Pills
    liq_cls  = "mpill-lp" if tot_liq >= 0 else "mpill-ln"
    liq_seta = "&#9650;" if tot_liq >= 0 else "&#9660;"

    # Linhas da tabela
    linhas = []
    for _, row in df_mes.iterrows():
        cx = formatar_brl(row["Caixa(Templo)"]) if row["Caixa(Templo)"] > 0 else "—"
        linhas.append(
            '<tr>'
            '<td class="ch">' + str(row["Igrejas"]) + '</td>'
            '<td class="r">'  + formatar_brl(row["Receitas"])     + '</td>'
            '<td class="r">'  + formatar_brl(row["Despesas"])     + '</td>'
            '<td class="r">'  + badge(row["Liquido"])             + '</td>'
            '<td class="r">'  + formatar_brl(row["Saldo Inicial"])+ '</td>'
            '<td class="r">'  + formatar_brl(row["Saldo Final"])  + '</td>'
            '<td class="r">'  + cx                                + '</td>'
            '</tr>'
        )
    rows_html = "".join(linhas)
    cx_total  = formatar_brl(tot_cx) if tot_cx > 0 else "—"

    return (
        '<div class="month-block">'
          '<div class="month-header">'
            '<h2>' + label + '</h2>'
            '<div class="month-pills">'
              '<span class="mpill mpill-r">Rec: '  + formatar_brl(tot_rec) + '</span>'
              '<span class="mpill mpill-d">Desp: ' + formatar_brl(tot_des) + '</span>'
              '<span class="mpill ' + liq_cls + '">' + liq_seta + ' ' + formatar_brl(tot_liq) + '</span>'
            '</div>'
          '</div>'
          '<div class="month-table-wrap">'
            '<table class="rel">'
              '<thead><tr>'
                '<th>Igreja</th>'
                '<th class="r">Receitas</th>'
                '<th class="r">Despesas</th>'
                '<th class="r">Líquido</th>'
                '<th class="r">Saldo Inicial</th>'
                '<th class="r">Saldo Final</th>'
                '<th class="r">Caixa (Templo)</th>'
              '</tr></thead>'
              '<tbody>' + rows_html + '</tbody>'
              '<tfoot><tr>'
                '<td><strong>Total</strong></td>'
                '<td class="r">' + formatar_brl(tot_rec) + '</td>'
                '<td class="r">' + formatar_brl(tot_des) + '</td>'
                '<td class="r">' + badge(tot_liq)        + '</td>'
                '<td class="r">' + formatar_brl(tot_si)  + '</td>'
                '<td class="r">' + formatar_brl(tot_sf)  + '</td>'
                '<td class="r">' + cx_total              + '</td>'
              '</tr></tfoot>'
            '</table>'
          '</div>'
          + obs_html +
        '</div>'
    )

# ─────────────────────────────────────────────
#  RENDERIZA OS 3 ÚLTIMOS MESES
# ─────────────────────────────────────────────
periodos = (
    df[["Ano", "Mês", "Data Referência"]]
    .drop_duplicates()
    .sort_values(["Ano", "Mês"], ascending=False)
    .head(3)
    .sort_values(["Ano", "Mês"], ascending=True)
    .values.tolist()
)

if not periodos:
    st.info("Nenhum dado encontrado para os filtros selecionados.")
else:
    for ano, mes, label in periodos:
        df_mes = df[(df["Ano"] == ano) & (df["Mês"] == mes)]
        st.markdown(render_month_block(str(label), df_mes), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
#st.markdown(f"""
#<div class="rel-footer">
#    <span>&#9642; IBF — Relatório Financeiro Mensal</span>
#    <span>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</span>
#</div>
#""", unsafe_allow_html=True)