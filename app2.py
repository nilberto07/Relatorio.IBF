import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Relatório Mensal — IBF",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────
PRIMARY   = "#BF5223"
DARK      = "#7D0911"
DARKEST   = "#5A1F05"
BORDER    = "#E8D5C8"
TEXT_DARK = "#1A0A02"
TEXT_SOFT = "#9E7E6A"
GREEN     = "#1E7A3C"
GREEN_BG  = "#E8F7EC"
RED       = "#C0392B"
RED_BG    = "#FDEAEA"

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Sans 3', sans-serif;
    background: #ffffff;
    color: {TEXT_DARK};
}}
.main .block-container {{
    padding: 2rem 2rem 3rem;
    max-width: 1200px;
}}

/* ── Page header ── */
.page-header {{
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1.2rem 0 1.4rem;
    border-bottom: 3px solid {BORDER};
    margin-bottom: 2rem;
}}
.page-header-logo {{
    width: 52px; height: 52px;
    background: linear-gradient(135deg, {DARKEST}, {PRIMARY});
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}}
.page-header-text h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.3rem, 3vw, 1.9rem);
    font-weight: 700;
    color: {DARKEST};
    margin: 0 0 0.1rem;
    line-height: 1.2;
}}
.page-header-text p {{
    font-size: 0.78rem;
    color: {TEXT_SOFT};
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}}

/* ── Month block ── */
.month-block {{
    margin-bottom: 2rem;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {BORDER};
    box-shadow: 0 2px 8px rgba(90,31,5,0.06);
}}
.month-header {{
    background: linear-gradient(90deg, {DARKEST} 0%, {DARK} 100%);
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}}
.month-header h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: 0.02em;
}}
.month-pills {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}}
.month-pill {{
    font-size: 0.68rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
    letter-spacing: 0.06em;
}}
.pill-rec  {{ background: rgba(255,255,255,0.18); color: #fff; }}
.pill-desp {{ background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.85); }}
.pill-liq-pos {{ background: {GREEN_BG}; color: {GREEN}; }}
.pill-liq-neg {{ background: {RED_BG};   color: {RED}; }}

/* ── Table ── */
.month-table-wrap {{
    overflow-x: auto;
    background: #fff;
}}
table.relatorio {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.83rem;
}}
table.relatorio thead tr {{
    background: #FDF6F0;
}}
table.relatorio thead th {{
    padding: 10px 14px;
    text-align: left;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {TEXT_SOFT};
    border-bottom: 2px solid {BORDER};
    white-space: nowrap;
}}
table.relatorio thead th.num {{
    text-align: right;
}}
table.relatorio tbody tr {{
    border-bottom: 1px solid {BORDER};
    transition: background 0.15s;
}}
table.relatorio tbody tr:hover {{
    background: #FDF6F0;
}}
table.relatorio tbody td {{
    padding: 9px 14px;
    color: {TEXT_DARK};
    white-space: nowrap;
}}
table.relatorio tbody td.num {{
    text-align: right;
    font-variant-numeric: tabular-nums;
}}
table.relatorio tbody td.church {{
    font-weight: 700;
    color: {DARKEST};
}}
table.relatorio tfoot tr {{
    background: {DARKEST};
}}
table.relatorio tfoot td {{
    padding: 10px 14px;
    font-weight: 700;
    font-size: 0.83rem;
    color: #fff !important;
    white-space: nowrap;
}}
table.relatorio tfoot td.num {{
    text-align: right;
    font-variant-numeric: tabular-nums;
}}

/* ── Badge ── */
.badge {{
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 20px;
    white-space: nowrap;
}}
.badge-pos {{ background: {GREEN_BG}; color: {GREEN}; }}
.badge-neg {{ background: {RED_BG};   color: {RED}; }}

/* ── Footer ── */
.rel-footer {{
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid {BORDER};
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.4rem;
    font-size: 0.7rem;
    color: {TEXT_SOFT};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}

/* ── Print ── */
@media print {{
    @page {{ size: A4 portrait; margin: 12mm 10mm; }}
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="collapsedControl"],
    footer {{ display: none !important; }}
    .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    .month-block {{ box-shadow: none !important; page-break-inside: avoid; margin-bottom: 14px; }}
    table.relatorio {{ font-size: 0.74rem; }}
    table.relatorio thead th,
    table.relatorio tbody td,
    table.relatorio tfoot td {{ padding: 6px 10px; }}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    rows = [
        (2025, 6,  "Jun/2025", "IBF",   149540.39, 120725.63, 662878.02, 691692.78, 572953.48),
        (2025, 6,  "Jun/2025", "IBE",    28585.36,  18202.89,  76841.77,  87224.24,       0.0),
        (2025, 6,  "Jun/2025", "IBT",     1713.64,   1860.59,    984.29,   9695.95,       0.0),
        (2025, 6,  "Jun/2025", "IBP",      267.98,   1159.42,  12523.43,  14043.81,       0.0),
        (2025, 6,  "Jun/2025", "IBR",     5335.96,   4621.21,  16446.25,  16677.37,       0.0),
        (2025, 6,  "Jun/2025", "IBFSB",   8104.56,   6593.31,   7808.16,   9287.44,       0.0),
        (2025, 7,  "Jul/2025", "IBF",   158283.87, 179263.67, 691692.78, 671212.98, 583147.51),
        (2025, 7,  "Jul/2025", "IBE",      244.66,  17331.39,  87224.24,  70137.51,       0.0),
        (2025, 7,  "Jul/2025", "IBT",     1707.65,   1358.63,   9695.95,  10044.97,       0.0),
        (2025, 7,  "Jul/2025", "IBP",      144.95,   1348.99,  14043.81,  12839.77,       0.0),
        (2025, 7,  "Jul/2025", "IBR",     4218.44,   3987.32,  16677.37,  16908.49,       0.0),
        (2025, 7,  "Jul/2025", "IBFSB",   7320.11,   5841.20,   9287.44,  10766.35,       0.0),
        (2025, 8,  "Ago/2025", "IBF",   161002.55, 142310.88, 671212.98, 689905.65, 601230.00),
        (2025, 8,  "Ago/2025", "IBE",    31200.00,  19850.75,  70137.51,  81486.76,       0.0),
        (2025, 8,  "Ago/2025", "IBT",     2105.30,   1720.15,  10044.97,  10430.12,       0.0),
        (2025, 8,  "Ago/2025", "IBP",      398.60,   1210.00,  12839.77,  12028.37,       0.0),
        (2025, 8,  "Ago/2025", "IBR",     5980.75,   5102.44,  16908.49,  17786.80,       0.0),
        (2025, 8,  "Ago/2025", "IBFSB",   9412.88,   7634.91,  10766.35,  12544.32,       0.0),
    ]
    return pd.DataFrame(rows, columns=[
        "Ano","Mês","Data Referência","Igreja",
        "Receitas","Despesas","Saldo Inicial","Saldo Final","Caixa(Templo)"
    ])

df_all = load_data()

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def fmt(v):
    if v == 0: return "—"
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def badge(v):
    seta = "&#9650;" if v >= 0 else "&#9660;"
    cls  = "badge-pos" if v >= 0 else "badge-neg"
    return f'<span class="badge {cls}">{seta} {fmt(v)}</span>'

def render_month_block(label, df_mes):
    df_mes = df_mes.sort_values("Receitas", ascending=False).copy()
    df_mes["Liquido"] = df_mes["Receitas"] - df_mes["Despesas"]

    tot_rec  = df_mes["Receitas"].sum()
    tot_desp = df_mes["Despesas"].sum()
    tot_liq  = tot_rec - tot_desp
    tot_si   = df_mes["Saldo Inicial"].sum()
    tot_sf   = df_mes["Saldo Final"].sum()
    tot_cx   = df_mes[df_mes["Caixa(Templo)"] > 0]["Caixa(Templo)"].max() if df_mes["Caixa(Templo)"].max() > 0 else 0

    liq_cls  = "pill-liq-pos" if tot_liq >= 0 else "pill-liq-neg"
    liq_seta = "&#9650;" if tot_liq >= 0 else "&#9660;"

    # Linhas da tabela
    rows_html = ""
    for _, row in df_mes.iterrows():
        cx_val = fmt(row["Caixa(Templo)"]) if row["Caixa(Templo)"] > 0 else "—"
        liq_v  = row["Receitas"] - row["Despesas"]
        rows_html += f"""
        <tr>
            <td class="church">{row['Igreja']}</td>
            <td class="num">{fmt(row['Receitas'])}</td>
            <td class="num">{fmt(row['Despesas'])}</td>
            <td class="num">{badge(liq_v)}</td>
            <td class="num">{fmt(row['Saldo Inicial'])}</td>
            <td class="num">{fmt(row['Saldo Final'])}</td>
            <td class="num">{cx_val}</td>
        </tr>"""

    cx_total = fmt(tot_cx) if tot_cx > 0 else "—"

    return f"""
<div class="month-block">
    <div class="month-header">
        <h2>{label}</h2>
        <div class="month-pills">
            <span class="month-pill pill-rec">Rec: {fmt(tot_rec)}</span>
            <span class="month-pill pill-desp">Desp: {fmt(tot_desp)}</span>
            <span class="month-pill {liq_cls}">{liq_seta} {fmt(tot_liq)}</span>
        </div>
    </div>
    <div class="month-table-wrap">
        <table class="relatorio">
            <thead>
                <tr>
                    <th>Igreja</th>
                    <th class="num">Receitas</th>
                    <th class="num">Despesas</th>
                    <th class="num">Líquido</th>
                    <th class="num">Saldo Inicial</th>
                    <th class="num">Saldo Final</th>
                    <th class="num">Caixa (Templo)</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
            <tfoot>
                <tr>
                    <td><strong>Total</strong></td>
                    <td class="num">{fmt(tot_rec)}</td>
                    <td class="num">{fmt(tot_desp)}</td>
                    <td class="num">{badge(tot_liq)}</td>
                    <td class="num">{fmt(tot_si)}</td>
                    <td class="num">{fmt(tot_sf)}</td>
                    <td class="num">{cx_total}</td>
                </tr>
            </tfoot>
        </table>
    </div>
</div>"""

# ─────────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-header-logo">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L12 5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M10.5 4H13.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
            <path d="M5 10L12 5L19 10V21H5V10Z" stroke="white" stroke-width="1.7"
                  stroke-linejoin="round" fill="rgba(255,255,255,0.15)"/>
            <path d="M9 21V15C9 13.343 10.343 12 12 12C13.657 12 15 13.343 15 15V21"
                  stroke="white" stroke-width="1.7" stroke-linejoin="round"/>
            <rect x="10.5" y="8" width="3" height="3" rx="0.5"
                  stroke="white" stroke-width="1.4" fill="rgba(255,255,255,0.15)"/>
        </svg>
    </div>
    <div class="page-header-text">
        <h1>Relatório Financeiro IBF</h1>
        <p>Três últimos meses · Gerado em {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  3 ÚLTIMOS MESES
# ─────────────────────────────────────────────
periodos = (
    df_all[["Ano","Mês","Data Referência"]]
    .drop_duplicates()
    .sort_values(["Ano","Mês"], ascending=False)
    .head(3)
    .values.tolist()
)
# Mostra do mais recente para o mais antigo
for ano, mes, label in periodos:
    df_mes = df_all[(df_all["Ano"] == ano) & (df_all["Mês"] == mes)]
    st.markdown(render_month_block(label, df_mes), unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="rel-footer">
    <span>&#9642; IBF — Relatório Financeiro Mensal</span>
    <span>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</span>
</div>
""", unsafe_allow_html=True)