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
ABAS = {"Página1": "0", "Página2": "1128666635", "Página3": "1066751161"}
conn = st.connection("gsheets", type=GSheetsConnection)

df_raw = conn.read(
    worksheet=ABAS["Página1"],
    ttl=0,
    usecols=["Indice", "Ano", "Mês", "Data Referência", "Igrejas",
             "Receitas", "Despesas", "Saldo Inicial", "Caixa(Templo)", "Observações"],
)

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
    seta = "&#9650;" if v >= 0 else "&#9660;"
    bg   = "#E8F7EC" if v >= 0 else "#FDEAEA"
    cor  = "#1E7A3C" if v >= 0 else "#C0392B"
    # Valor sem "R$ " para economizar espaço na coluna
    av = abs(v) / 100
    txt = f"{av:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    return (
        f'<span style="display:inline-block;font-size:0.58rem;font-weight:700;'
        f'padding:1px 4px;border-radius:4px;background:{bg};color:{cor};'
        f'white-space:nowrap;max-width:100%;">{seta} {txt}</span>'
    )

# ─────────────────────────────────────────────
#  CSS — tela + print
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600;700&display=swap');

/* ── Reset geral ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background: #fff;
}
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
footer                    { display: none !important; }
.main .block-container {
    padding: 0 0.5rem 0.5rem !important;
    max-width: 100% !important;
}
        
.st-emotion-cache-19ehcf5 table {
    margin-bottom: 0 !important;
}

/* ── Botão de impressão ── */
.print-btn-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
    gap: 10px;
}
.print-btn {
    background: #5A1F05;
    color: #fff;
    border: none;
    padding: 8px 20px;
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    font-family: 'Source Sans 3', sans-serif;
    letter-spacing: .05em;
    display: flex;
    align-items: center;
    gap: 6px;
}
.print-btn:hover { background: #7D0911; }

/* ── Layout de panfleto duplo ── */
.panfleto-page {
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 0;
    margin-bottom: 2rem;
    page-break-after: always;
    align-items: start;
}
.divisor {
    width: 1px;
    background: #E8D5C8;
    margin: 0 14px;
}
.panfleto-col {
    padding: 0 3px;
    min-width: 0;
}

/* ── Cabeçalho do panfleto ── */
.pf-header {
    display: flex;
    align-items: center;
    gap: 7px;
    justify-content: center;
}
.pf-logo {
    width: 26px; height: 26px; flex-shrink: 0;
    background: transparent;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
}
.pf-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.20rem;
    font-weight: 700;
    color: #5A1F05;
    margin: 0 0 1px;
    line-height: 1.1;
}
.pf-header p {
    font-size: 0.54rem;
    color: #9E7E6A;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: .07em;
    font-weight: 600;
}

/* ── Bloco de mês ── */
.pf-month {
    margin-bottom: 3px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #E8D5C8;
}
.pf-month-header {
    background: linear-gradient(90deg, #5A1F05, #7D0911);
    padding: 0px 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4px;
    flex-wrap: nowrap;
}
.pf-month-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    white-space: nowrap;
}
.pf-pills { display: flex; gap: 3px; flex-wrap: nowrap; }
.pf-pill {
    font-size: 0.52rem;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 20px;
    white-space: nowrap;
}
.pf-pill-r  { background: rgba(255,255,255,.18); color: #fff; }
.pf-pill-d  { background: rgba(255,255,255,.1);  color: rgba(255,255,255,.85); }
.pf-pill-lp { background: #E8F7EC; color: #1E7A3C; }
.pf-pill-ln { background: #FDEAEA; color: #C0392B; }

/* ── Tabela do panfleto ── */
table.pft {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.75rem;        /* compacto para caber horizontal */
    table-layout: fixed;       /* distribui colunas igualmente */
}
table.pft thead tr { background: #FDF6F0; }
table.pft thead th {
    padding: 3px 4px;
    text-align: left;
    font-size: 0.64rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
    color: #9E7E6A;
    border-bottom: 1.5px solid #E8D5C8;
    white-space: nowrap;
    overflow: hidden;
}
table.pft thead th.r { text-align: right; }
/* Coluna Líquido (4a) — largura controlada */
table.pft th:nth-child(4),
table.pft td:nth-child(4) {
    max-width: 80px;
    overflow: hidden;
}
/* Igreja (1a) — menor */
table.pft th:nth-child(1),
table.pft td:nth-child(1) { width: 42px; }
table.pft tbody tr  { border-bottom: 1px solid #F0E8E0; }
table.pft tbody tr:nth-child(even) { background: #FDFAF8; }
table.pft tbody td  { padding: 3px 4px; white-space: nowrap; overflow: hidden; color: #1A0A02; }
table.pft tbody td.r  { text-align: right; font-variant-numeric: tabular-nums; }
table.pft tbody td.ch { font-weight: 700; color: #5A1F05; }
table.pft tfoot tr  { background: #5A1F05; }
table.pft tfoot td  {
    padding: 3px 4px;
    font-weight: 700;
    font-size: 0.75rem;
    color: #fff;
    white-space: nowrap;
}
table.pft tfoot td.r { text-align: right; font-variant-numeric: tabular-nums; }

/* ── Obs compacta ── */
.pf-obs {
    padding: 0px 8px 0px;
    background: #FDF6F0;
    border-top: 1px solid #E8D5C8;
    font-size: 0.62rem;
    line-height: 1.6;
    color: #5A3D2B;
}
.pf-obs-label {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #9E7E6A;
    margin-right: 4px;
}

/* ── Rodapé do panfleto ── */
.pf-footer {
    margin-top: 4px;
    padding-top: 3px;
    border-top: 1px solid #E8D5C8;
    font-size: 0.50rem;
    color: #9E7E6A;
    text-align: center;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .05em;
}

/* ══════════════════════════════════════
   PRINT — A4 paisagem, dois panfletos
   ══════════════════════════════════════ */
@media print {
    @page { size: A4 landscape; margin: 4mm 4mm; }

    /* Oculta tudo do Streamlit */
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"],
    section[data-testid="stSidebar"],
    iframe,
    footer,
    .stDeployButton { display: none !important; }

    /* Zera absolutamente todos os espaços do Streamlit */
    html, body { margin: 0 !important; padding: 0 !important; }
    .main,
    .main > div,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"],
    .block-container,
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        gap: 0 !important;
    }

    .panfleto-page {
        width: 100%;
        page-break-inside: avoid;
        page-break-after: avoid;
        margin: 0;
        gap: 0;
    }

    .panfleto-col { padding: 0 4px; }
    .divisor { margin: 0 6px; }

    /* Cabeçalho ultra-compacto */
    .pf-header      { padding-bottom: 4px; margin-bottom: 5px; }
    .pf-header h1   { font-size: 0.95rem; }
    .pf-header p    { font-size: 0.57rem; }
    .pf-logo        { width: 22px; height: 22px; border-radius: 4px; }

    /* Mês header */
    .pf-month           { margin-bottom: 4px; border-radius: 4px; }
    .pf-month-header    { padding: 2px 6px; }
    .pf-month-header h2 { font-size: 0.72rem; }
    .pf-pill            { font-size: 0.56rem; padding: 0px 4px; }

    /* Tabela máxima compactação */
    table.pft           { font-size: 0.62rem; }
    table.pft thead th  { font-size: 0.59rem; padding: 2px 2px; }
    table.pft tbody td  { padding: 1px 2px; }
    table.pft tfoot td  { padding: 2px 2px; font-size: 0.59rem; }

    .pf-obs             { font-size: 0.44rem; padding: 1px 5px; }
    .pf-footer          { font-size: 0.44rem; margin-top: 3px; padding-top: 2px; }
}
</style>

<script>
function imprimir() { window.print(); }
</script>
""", unsafe_allow_html=True)

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
    <hr style='border-color:rgba(255,255,255,0.2);margin:1.5rem 0 1rem;'>
    <div style='text-align:center;padding:1rem 0'>
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L12 5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M10.5 4H13.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M5 10L12 5L19 10V21H5V10Z" stroke="white" stroke-width="1.7"
                  stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
            <path d="M9 21V15C9 13.3431 10.3431 12 12 12C13.6569 12 15 13.3431 15 15V21"
                  stroke="white" stroke-width="1.7" stroke-linejoin="round"/>
            <rect x="10.5" y="8" width="3" height="3" rx="0.5" stroke="white"
                  stroke-width="1.4" fill="rgba(255,255,255,0.15)"/>
        </svg>
        <div style='font-family:"Playfair Display",serif;font-size:0.95rem;font-weight:700;margin-top:6px;'>IBF</div>
        <div style='font-size:0.65rem;opacity:0.6;text-transform:uppercase;letter-spacing:.1em;margin-top:2px;'>
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
#  MONTA UM PANFLETO (HTML completo)
# ─────────────────────────────────────────────
def build_panfleto(periodos, df) -> str:
    data_str = datetime.now().strftime('%d/%m/%Y')

    cabecalho = (
        '<div class="pf-header">'
        '<div class="pf-logo" style="background:transparent;padding:1px;">'
        '<img src="app/static/logo.png" style="width:22px;height:22px;object-fit:contain;">'
        '</div>'
        '<div>'
        '<h1>Relatório Financeiro IBF</h1>'
        #f'<p>Três últimos meses · {data_str}</p>'
        '</div>'
        '</div>'
    )

    blocos = ""
    for ano, mes, label in periodos:
        df_mes = df[(df["Ano"] == ano) & (df["Mês"] == mes)].copy()
        #df_mes = df_mes.sort_values("Receitas", ascending=False)
        df_mes = df_mes.sort_values("Indice", ascending=True)
        df_mes["Liquido"]     = df_mes["Receitas"] - df_mes["Despesas"]
        df_mes["Saldo Final"] = df_mes["Saldo Inicial"] + df_mes["Liquido"]

        tot_rec = df_mes["Receitas"].sum()
        tot_des = df_mes["Despesas"].sum()
        tot_liq = tot_rec - tot_des
        tot_si  = df_mes["Saldo Inicial"].sum()
        tot_sf  = df_mes["Saldo Final"].sum()
        df_cx   = df_mes[df_mes["Caixa(Templo)"] > 0].sort_values("Caixa(Templo)", ascending=False)
        tot_cx  = df_cx["Caixa(Templo)"].iloc[0] if not df_cx.empty else 0.0

        liq_cls  = "pf-pill-lp" if tot_liq >= 0 else "pf-pill-ln"
        liq_seta = "&#9650;" if tot_liq >= 0 else "&#9660;"

        # Linhas
        linhas = []
        for _, row in df_mes.iterrows():
            cx = formatar_brl(row["Caixa(Templo)"]) if row["Caixa(Templo)"] > 0 else "—"
            linhas.append(
                '<tr>'
                '<td class="ch">' + str(row["Igrejas"])              + '</td>'
                '<td class="r">'  + formatar_brl(row["Receitas"])    + '</td>'
                '<td class="r">'  + formatar_brl(row["Despesas"])    + '</td>'
                '<td class="r">'  + badge(row["Liquido"])            + '</td>'
                '<td class="r">'  + formatar_brl(row["Saldo Inicial"])+ '</td>'
                '<td class="r">'  + formatar_brl(row["Saldo Final"]) + '</td>'
                '<td class="r">'  + cx                               + '</td>'
                '</tr>'
            )

        cx_total = formatar_brl(tot_cx) if tot_cx > 0 else "—"

        # Observações
        obs_rows = df_mes[
            df_mes["Observações"].notna() &
            (df_mes["Observações"].astype(str).str.strip() != "") &
            (df_mes["Observações"].astype(str).str.strip() != "—")
        ]
        if not obs_rows.empty:
            partes = [
                '<span style="font-weight:700;color:#5A1F05">' + str(r["Igrejas"]) + ':</span> ' + str(r["Observações"])
                for _, r in obs_rows.iterrows()
            ]
            obs_html = (
                '<div class="pf-obs">'
                '<span class="pf-obs-label">Obs.:</span>'
                + ' &nbsp;·&nbsp; '.join(partes) +
                '</div>'
            )
        else:
            obs_html = ""

        blocos += (
            '<div class="pf-month">'
              '<div class="pf-month-header">'
                '<h2>' + str(label) + '</h2>'
                '<div class="pf-pills">'
                  '<span class="pf-pill pf-pill-r">Rec: '  + formatar_brl(tot_rec) + '</span>'
                  '<span class="pf-pill pf-pill-d">Desp: ' + formatar_brl(tot_des) + '</span>'
                  '<span class="pf-pill ' + liq_cls + '">' + liq_seta + ' ' + formatar_brl(tot_liq) + '</span>'
                '</div>'
              '</div>'
              '<table class="pft">'
                '<thead><tr>'
                  '<th>Igreja</th>'
                  '<th class="r">Receitas</th>'
                  '<th class="r">Despesas</th>'
                  '<th class="r">Líquido</th>'
                  '<th class="r">Saldo Inicial</th>'
                  '<th class="r">Saldo Final</th>'
                  '<th class="r">Caixa(Templo)</th>'
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
                '</tr></tfoot>'
              '</table>'
              + obs_html +
            '</div>'
        )

    rodape = (
        '<div class="pf-footer">'
        '&#9642; IBF — Relatório Financeiro Mensal'
        '</div>'
    )

    return cabecalho + blocos + rodape


# ─────────────────────────────────────────────
#  PERÍODOS
# ─────────────────────────────────────────────
periodos = (
    df[["Ano", "Mês", "Data Referência"]]
    .drop_duplicates()
    .sort_values(["Ano", "Mês"], ascending=False)
    .head(3)
    .sort_values(["Ano", "Mês"], ascending=True)
    .values.tolist()
)

# ─────────────────────────────────────────────
#  BOTÃO IMPRIMIR
# ─────────────────────────────────────────────
st.iframe("""
<button onclick="window.parent.print()"
    style="background:#5A1F05;color:#fff;border:none;padding:8px 20px;
           border-radius:7px;font-size:0.82rem;font-weight:700;cursor:pointer;
           font-family:'Source Sans 3',sans-serif;letter-spacing:.05em;
           display:flex;align-items:center;gap:6px;float:right;">
    &#128438; Imprimir / Salvar PDF
</button>
""", height=50)

# ─────────────────────────────────────────────
#  RENDERIZA: dois panfletos lado a lado
# ─────────────────────────────────────────────
if not periodos:
    st.info("Nenhum dado encontrado para os filtros selecionados.")
else:
    panfleto = build_panfleto(periodos, df)

    st.markdown(
        '<div class="panfleto-page">'
        '<div class="panfleto-col">' + panfleto + '</div>'
        '<div class="divisor"></div>'
        '<div class="panfleto-col">' + panfleto + '</div>'
        '</div>',
        unsafe_allow_html=True
    )
