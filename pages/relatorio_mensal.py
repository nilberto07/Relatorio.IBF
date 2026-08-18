import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl
from relatorio_impressao import botao_download_relatorio
from datetime import datetime
from utils.theme import load_css

load_css()
ssl._create_default_https_context = ssl._create_stdlib_context

# ─────────────────────────────────────────────
#  CONEXÃO
# ─────────────────────────────────────────────
ABAS = {"Página1": "0", "Página2": "1128666635", "Página3": "1066751161"}
conn   = st.connection("gsheets", type=GSheetsConnection)
df_raw = conn.read(
    worksheet=ABAS["Página1"],
    ttl=0,
    usecols=["Indice", "Ano", "Mês", "Data Referência", "Igrejas",
             "Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)", "Observações"],
)

for col in ["Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)", "Ano", "Mês"]:
    df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def formatar_brl(valor: float) -> str:
    if pd.isna(valor) or valor == 0:
        return "—"
    return f"R$ {valor / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def badge(v: float) -> str:
    seta = "&#9650;" if v >= 0 else "&#9660;"
    bg   = "#E8F7EC" if v >= 0 else "#FDEAEA"
    cor  = "#1E7A3C" if v >= 0 else "#C0392B"
    return (
        f'<span style="display:inline-block;font-size:0.7rem;font-weight:700;'
        f'padding:2px 8px;border-radius:20px;background:{bg};color:{cor};white-space:nowrap">'
        f'{seta} {formatar_brl(v)}</span>'
    )

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;
                margin-bottom:1rem;padding-top:3rem;font-weight:700;
                border-bottom:1px solid rgba(255,255,255,0.3);'>Filtros</div>
    """, unsafe_allow_html=True)

    filtro_igrejas = st.multiselect("Igrejas:", options=sorted(df_raw["Igrejas"].dropna().unique()),         placeholder="Selecione...")
    filtro_ano     = st.multiselect("Ano:",     options=sorted(df_raw["Ano"].dropna().unique().astype(int)), placeholder="Selecione...")
    filtro_mes     = st.multiselect("Mês:",     options=sorted(df_raw["Mês"].dropna().unique().astype(int)), placeholder="Selecione...")

    botao_download_relatorio(df_raw)

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.2);margin:1.5rem 0 1rem;'>
    <div style='text-align:center;padding:1rem 0'>
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
#  FILTROS
# ─────────────────────────────────────────────
df = df_raw.copy()
if filtro_igrejas:
    df = df[df["Igrejas"].isin(filtro_igrejas)]
if filtro_ano:
    df = df[df["Ano"].isin(filtro_ano)]
if filtro_mes:
    df = df[df["Mês"].isin(filtro_mes)]

# ─────────────────────────────────────────────
#  HEADER
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
#  KPI CARDS — totais gerais do período filtrado
# ─────────────────────────────────────────────
total_rec  = df["Receitas"].sum()
total_desp = df["Despesas"].sum()
liquido    = total_rec - total_desp
badge_class = "badge-pos" if liquido >= 0 else "badge-neg"
badge_sign  = "▲" if liquido >= 0 else "▼"

df_caixa  = df[df["Caixa(Templo)"] > 0].sort_values(["Ano", "Mês"], ascending=False)
caixa_tmp = df_caixa["Caixa(Templo)"].iloc[0] if not df_caixa.empty else 0.0

# Média mensal — acumulado do ano até o mês mais recente ÷ número do mês
if not df.empty and df["Mês"].notna().any():
    ano_ref_kpi = int(df["Ano"].max())
    mes_ref_kpi = int(df[df["Ano"] == ano_ref_kpi]["Mês"].max())
    df_acum_kpi = df[(df["Ano"] == ano_ref_kpi) & (df["Mês"] <= mes_ref_kpi)]
    liq_acum_kpi = df_acum_kpi["Receitas"].sum() - df_acum_kpi["Despesas"].sum()
    media_kpi    = liq_acum_kpi / mes_ref_kpi if mes_ref_kpi > 0 else 0.0
else:
    mes_ref_kpi = 0
    media_kpi   = 0.0

med_sign  = "▲" if media_kpi >= 0 else "▼"
med_class = "badge-pos" if media_kpi >= 0 else "badge-neg"

SVG_RECEITAS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" stroke="#BF5223" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_DESPESAS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17 8 12 3 7 8" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="3" x2="12" y2="15" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round"/></svg>'
SVG_SALDO    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="#5A1F05" stroke-width="1.8"/><path d="M16 3H8a2 2 0 0 0-2 2v2h12V5a2 2 0 0 0-2-2Z" stroke="#5A1F05" stroke-width="1.8"/><circle cx="12" cy="14" r="2" stroke="#5A1F05" stroke-width="1.8"/></svg>'
SVG_MEDIA    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><line x1="18" y1="20" x2="18" y2="10" stroke="#BF5223" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="20" x2="12" y2="4" stroke="#BF5223" stroke-width="1.8" stroke-linecap="round"/><line x1="6" y1="20" x2="6" y2="14" stroke="#BF5223" stroke-width="1.8" stroke-linecap="round"/><line x1="3" y1="12" x2="21" y2="12" stroke="#7D0911" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="2 2"/></svg>'
SVG_CAIXA    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/><polyline points="9 22 9 12 15 12 15 22" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/></svg>'

st.markdown(f"""
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
    <!--<div class="kpi-card saldo">
        <div class="kpi-inner">
            <div class="kpi-icon saldo">{SVG_SALDO}</div>
            <div class="kpi-body">
                <div class="kpi-label">Saldo Líquido</div>
                <div class="kpi-value">{badge_sign} {formatar_brl(liquido)}</div>
                <div class="kpi-sub">Receitas x Despesas</div>
            </div>
        </div>
    </div>-->
    <div class="kpi-card receitas">
        <div class="kpi-inner">
            <div class="kpi-icon receitas">{SVG_MEDIA}</div>
            <div class="kpi-body">
                <div class="kpi-label">Média Mensal</div>
                <div class="kpi-value">{med_sign} {formatar_brl(media_kpi)}</div>
                <div class="kpi-sub">Líquido acum. ÷ mês {mes_ref_kpi if mes_ref_kpi else "—"}</div>
            </div>
        </div>
    </div>
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
#  RENDER MONTH BLOCK
# ─────────────────────────────────────────────
def render_month_block(label: str, df_mes: pd.DataFrame) -> str:
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

    liq_cls  = "mpill-lp" if tot_liq >= 0 else "mpill-ln"
    liq_seta = "&#9650;"  if tot_liq >= 0 else "&#9660;"

    # Média do mês = acumulado líquido do ano até o mês atual ÷ número do mês
    mes_ref  = int(df_mes["Mês"].iloc[0])   # ex: 4
    ano_ref  = int(df_mes["Ano"].iloc[0])
    # Filtra df com todos os meses de 1 até mes_ref do mesmo ano (respeitando filtros de igreja)
    df_acum  = df[(df["Ano"] == ano_ref) & (df["Mês"] <= mes_ref)]
    liq_acum = df_acum["Receitas"].sum() - df_acum["Despesas"].sum()
    media_liq = liq_acum / mes_ref if mes_ref > 0 else 0.0

    med_cls  = "mpill-lp" if media_liq >= 0 else "mpill-ln"

    # Média por igreja = acumulado líquido da igreja até o mês atual ÷ número do mês
    medias_ig = {}
    for igr in df_mes["Igrejas"].unique():
        df_ig_acum   = df_acum[df_acum["Igrejas"] == igr]
        liq_ig_acum  = df_ig_acum["Receitas"].sum() - df_ig_acum["Despesas"].sum()
        medias_ig[igr] = liq_ig_acum / mes_ref if mes_ref > 0 else 0.0

    # Observações
    obs_rows = df_mes[
        df_mes["Observações"].notna() &
        (df_mes["Observações"].astype(str).str.strip() != "") &
        (df_mes["Observações"].astype(str).str.strip() != "—")
    ][["Igrejas", "Observações"]]

    if not obs_rows.empty:
        partes = [
            '<span style="color:#5A1F05;font-weight:700">' + str(r["Igrejas"]) + ':</span> '
            '<span style="color:#5A3D2B">' + str(r["Observações"]) + '</span>'
            for _, r in obs_rows.iterrows()
        ]
        obs_html = (
            '<div style="padding:6px 16px 8px;background:#FDF6F0;border-top:1px solid #E8D5C8;'
            'font-size:0.75rem;line-height:1.8">'
            '<span style="font-weight:700;text-transform:uppercase;letter-spacing:.08em;'
            'color:#9E7E6A;margin-right:8px">Obs.:</span>'
            + ' &nbsp;·&nbsp; '.join(partes) + '</div>'
        )
    else:
        obs_html = ""

    # Linhas
    linhas = []
    for _, row in df_mes.iterrows():
        cx = formatar_brl(row["Caixa(Templo)"]) if row["Caixa(Templo)"] > 0 else "—"
        linhas.append(
            '<tr>'
            '<td class="ch">' + str(row["Igrejas"])               + '</td>'
            '<td class="r">'  + formatar_brl(row["Receitas"])     + '</td>'
            '<td class="r">'  + formatar_brl(row["Despesas"])     + '</td>'
            '<td class="r">'  + badge(row["Liquido"])             + '</td>'
            '<td class="r">'  + formatar_brl(row["Saldo Inicial"])+ '</td>'
            '<td class="r">'  + formatar_brl(row["Saldo Final"])  + '</td>'
            '<td class="r">'  + cx                                + '</td>'
            '<td class="r">'  + badge(medias_ig.get(str(row["Igrejas"]), 0.0)) + '</td>'
            '</tr>'
        )

    cx_total = formatar_brl(tot_cx) if tot_cx > 0 else "—"

    return (
        '<div class="month-block">'
          '<div class="month-header">'
            '<h2>' + label + '</h2>'
            '<div class="month-pills">'
              '<span class="mpill mpill-r">Rec: '  + formatar_brl(tot_rec) + '</span>'
              '<span class="mpill mpill-d">Desp: ' + formatar_brl(tot_des) + '</span>'
              '<span class="mpill ' + liq_cls + '">' + liq_seta + ' ' + formatar_brl(tot_liq) + '</span>'
              '<span class="mpill ' + med_cls + '">Média/Ano: ' + formatar_brl(media_liq) + '</span>'
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
                '<th class="r">Média/Ano</th>'
              '</tr></thead>'
              '<tbody>' + "".join(linhas) + '</tbody>'
              '<tfoot><tr>'
                '<td><strong>Total</strong></td>'
                '<td class="r">' + formatar_brl(tot_rec) + '</td>'
                '<td class="r">' + formatar_brl(tot_des) + '</td>'
                '<td class="r">' + badge(tot_liq)        + '</td>'
                '<td class="r">' + formatar_brl(tot_si)  + '</td>'
                '<td class="r">' + formatar_brl(tot_sf)  + '</td>'
                '<td class="r">' + cx_total              + '</td>'
                '<td class="r">' + badge(media_liq)      + '</td>'
              '</tr></tfoot>'
            '</table>'
          '</div>'
          + obs_html +
        '</div>'
    )

# ─────────────────────────────────────────────
#  PERÍODOS E RENDERIZAÇÃO
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