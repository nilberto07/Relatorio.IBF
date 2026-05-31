import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Financeiro — IBF",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed",   # collapsed by default on mobile
)

# ─────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────
PRIMARY   = "#BF5223"
DARK      = "#7D0911"
DARKEST   = "#5A1F05"
BORDER    = "#E8D5C8"
TEXT_DARK = "#1A0A02"
TEXT_MID  = "#5A3D2B"
TEXT_SOFT = "#9E7E6A"

# ─────────────────────────────────────────────
#  GLOBAL CSS  — responsive + print
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Sans 3', sans-serif;
    background-color: #ffffff;
    color: {TEXT_DARK};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(170deg, {DARKEST} 0%, {DARK} 60%, {PRIMARY} 100%);
    border-right: none;
}}
[data-testid="stSidebar"] * {{ color: #fff !important; }}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 6px;
    color: #fff !important;
}}

/* ── Main container ── */
.main .block-container {{
    padding: 1.5rem 1.5rem 3rem;
    max-width: 1300px;
}}

/* ── Header ── */
.dash-header {{
    border-left: 5px solid {PRIMARY};
    padding: 0.75rem 0 0.75rem 1.2rem;
    margin-bottom: 1.5rem;
}}
.dash-header h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.4rem, 4vw, 2.1rem);
    font-weight: 700;
    color: {DARKEST};
    margin: 0 0 0.15rem;
    line-height: 1.2;
}}
.dash-header p {{
    font-size: 0.8rem;
    color: {TEXT_SOFT};
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}}

/* ── Section title ── */
.section-title {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: {PRIMARY};
    margin: 1.75rem 0 0.85rem;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid {BORDER};
}}
.section-title::before {{
    content: '';
    display: inline-block;
    width: 3px;
    height: 13px;
    background: {PRIMARY};
    border-radius: 2px;
    flex-shrink: 0;
}}

/* ── KPI Grid — responsive ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}}

/* Tablet: 2x2 */
@media (max-width: 900px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .main .block-container {{ padding: 1rem 1rem 2.5rem; }}
}}

/* Mobile: 1 column */
@media (max-width: 520px) {{
    .kpi-grid {{ grid-template-columns: 1fr; gap: 0.6rem; }}
    .main .block-container {{ padding: 0.75rem 0.75rem 2rem; }}
    .dash-header {{ padding: 0.6rem 0 0.6rem 1rem; }}
}}

/* ── KPI Card ── */
.kpi-card {{
    background: #fff;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.1rem 1.2rem 1rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(90,31,5,0.06);
    min-width: 0;      /* prevent grid blowout */
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}}
.kpi-card.receitas::before {{ background: {PRIMARY}; }}
.kpi-card.despesas::before {{ background: {DARK}; }}
.kpi-card.saldo::before    {{ background: {DARKEST}; }}
.kpi-card.caixa::before    {{ background: {PRIMARY}; opacity: 0.65; }}

/* ── Card inner layout: icon + text side-by-side on mobile ── */
.kpi-inner {{
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
}}
.kpi-icon {{
    width: 34px;
    height: 34px;
    min-width: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
    flex-shrink: 0;
}}
.kpi-icon.receitas {{ background: #FEF0E8; }}
.kpi-icon.despesas {{ background: #FDEAEA; }}
.kpi-icon.saldo    {{ background: #F0EBE8; }}
.kpi-icon.caixa    {{ background: #EBF0F0; }}

.kpi-body {{ min-width: 0; flex: 1; }}
.kpi-label {{
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {TEXT_SOFT};
    margin-bottom: 0.2rem;
    white-space: nowrap;
}}
.kpi-value {{
    font-size: clamp(1.1rem, 2.5vw, 1.4rem);
    font-weight: 700;
    color: {TEXT_DARK};
    line-height: 1.15;
    font-variant-numeric: tabular-nums;
    /* allow wrapping at the space between R$ and number */
    word-break: keep-all;
    overflow-wrap: normal;
    white-space: normal;
}}
.kpi-sub {{
    font-size: 0.72rem;
    color: {TEXT_SOFT};
    margin-top: 0.25rem;
    line-height: 1.3;
}}
.kpi-badge {{
    display: inline-block;
    font-size: 0.67rem;
    font-weight: 700;
    padding: 0.12rem 0.5rem;
    border-radius: 20px;
    margin-top: 0.35rem;
    white-space: nowrap;
}}
.badge-pos {{ background: #E8F7EC; color: #1E7A3C; }}
.badge-neg {{ background: #FDEAEA; color: #C0392B; }}

/* ── Table ── */
.stDataFrame {{
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    overflow: hidden;
}}

/* ── Footer ── */
.dash-footer {{
    margin-top: 2.5rem;
    padding: 1rem 0;
    border-top: 1px solid {BORDER};
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    justify-content: space-between;
    font-size: 0.7rem;
    color: {TEXT_SOFT};
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

/* ── Print ── */
@media print {{
    @page {{ size: A4 portrait; margin: 14mm 12mm; }}
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="collapsedControl"],
    footer {{ display: none !important; }}
    .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    .kpi-grid {{ grid-template-columns: repeat(4, 1fr) !important; gap: 6px !important; }}
    .kpi-card {{ padding: 9px 11px; box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }}
    .kpi-value {{ font-size: 1rem !important; }}
    .dash-header h1 {{ font-size: 1.4rem !important; }}
    .section-title {{ margin: 10px 0 7px; }}
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    rows = [
        (2025, 6, "Jun/2025", "IBF",   149540.39, 120725.63, 662878.02, 572953.48, ""),
        (2025, 6, "Jun/2025", "IBE",    28585.36,  18202.89,  76841.77,       0.0, ""),
        (2025, 6, "Jun/2025", "IBT",     1713.64,   1860.59,    984.29,       0.0, ""),
        (2025, 6, "Jun/2025", "IBP",      267.98,   1159.42,  12523.43,       0.0, ""),
        (2025, 6, "Jun/2025", "IBR",     5335.96,   4621.21,  16446.25,       0.0, ""),
        (2025, 6, "Jun/2025", "IBFSB",   8104.56,   6593.31,   7808.16,       0.0, ""),
        (2025, 7, "Jul/2025", "IBF",   158283.87, 179263.67, 691692.78, 583147.51, ""),
        (2025, 7, "Jul/2025", "IBE",      244.66,  17331.39,  87224.24,       0.0, ""),
        (2025, 7, "Jul/2025", "IBT",     1707.65,   1358.63,   9695.95,       0.0, ""),
        (2025, 7, "Jul/2025", "IBP",      144.95,   1348.99,  14043.81,       0.0, ""),
        (2025, 7, "Jul/2025", "IBR",     4218.44,   3987.32,  16677.37,       0.0, ""),
        (2025, 7, "Jul/2025", "IBFSB",   7320.11,   5841.20,   9287.44,       0.0, ""),
        (2025, 8, "Ago/2025", "IBF",   161002.55, 142310.88, 710384.45, 601230.00, ""),
        (2025, 8, "Ago/2025", "IBE",    31200.00,  19850.75,  98275.49,       0.0, ""),
        (2025, 8, "Ago/2025", "IBT",     2105.30,   1720.15,   8080.40,       0.0, ""),
        (2025, 8, "Ago/2025", "IBP",      398.60,   1210.00,  13232.41,       0.0, ""),
        (2025, 8, "Ago/2025", "IBR",     5980.75,   5102.44,  17554.68,       0.0, ""),
        (2025, 8, "Ago/2025", "IBFSB",   9412.88,   7634.91,   8961.22,       0.0, ""),
    ]
    return pd.DataFrame(rows, columns=[
        "Ano","Mês","Data Referência","Igreja",
        "Receitas","Despesas","Saldo Inicial","Caixa(Templo)","Observações"
    ])

df_all = load_data()

# ─────────────────────────────────────────────
#  SIDEBAR — FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
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
    <hr style='border-color:rgba(255,255,255,0.15); margin-bottom:1.5rem;'>
    <div style='font-size:0.68rem; text-transform:uppercase; letter-spacing:0.12em; opacity:0.65; margin-bottom:1rem; font-weight:700;'>▸ Filtros</div>
    """, unsafe_allow_html=True)

    igrejas_opts = sorted(df_all["Igreja"].unique().tolist())
    sel_igrejas = st.multiselect("Igrejas", igrejas_opts, placeholder="Todas as igrejas")

    anos_opts = sorted(df_all["Ano"].unique().tolist())
    sel_ano = st.selectbox("Ano", ["Todos os anos"] + [str(a) for a in anos_opts])

    meses_map = {
        1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",
        7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"
    }
    meses_opts = sorted(df_all["Mês"].unique().tolist())
    meses_labels = [meses_map.get(m, str(m)) for m in meses_opts]
    sel_mes_label = st.selectbox("Mês", ["Todos os meses"] + meses_labels)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.15); margin: 1.5rem 0 1rem;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.68rem; opacity:0.5; text-transform:uppercase; letter-spacing:0.08em;'>
        Atualizado em {datetime.now().strftime('%d/%m/%Y')}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = df_all.copy()
if sel_igrejas:
    df = df[df["Igreja"].isin(sel_igrejas)]
if sel_ano != "Todos os anos":
    df = df[df["Ano"] == int(sel_ano)]
if sel_mes_label != "Todos os meses":
    rev_map = {v: k for k, v in meses_map.items()}
    df = df[df["Mês"] == rev_map[sel_mes_label]]

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <h1>Dashboard Financeiro</h1>
    <p>Relatório · Assembleia Geral</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
total_rec  = df["Receitas"].sum()
total_desp = df["Despesas"].sum()
saldo_ini  = df["Saldo Inicial"].sum()
caixa_tmp  = df["Caixa(Templo)"].sum()
liquido    = total_rec - total_desp
badge_class = "badge-pos" if liquido >= 0 else "badge-neg"
badge_sign  = "▲" if liquido >= 0 else "▼"

def fmt(v):
    return f"R$&nbsp;{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

SVG_RECEITAS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" stroke="#BF5223" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_DESPESAS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17 8 12 3 7 8" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="3" x2="12" y2="15" stroke="#7D0911" stroke-width="1.8" stroke-linecap="round"/></svg>'
SVG_SALDO    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="#5A1F05" stroke-width="1.8"/><path d="M16 3H8a2 2 0 0 0-2 2v2h12V5a2 2 0 0 0-2-2Z" stroke="#5A1F05" stroke-width="1.8"/><circle cx="12" cy="14" r="2" stroke="#5A1F05" stroke-width="1.8"/></svg>'
SVG_CAIXA    = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/><polyline points="9 22 9 12 15 12 15 22" stroke="#BF5223" stroke-width="1.8" stroke-linejoin="round"/></svg>'

st.markdown(f"""
<div class="section-title">Resumo Financeiro</div>
<div class="kpi-grid">
    <div class="kpi-card receitas">
        <div class="kpi-inner">
            <div class="kpi-icon receitas">{SVG_RECEITAS}</div>
            <div class="kpi-body">
                <div class="kpi-label">Receitas</div>
                <div class="kpi-value">{fmt(total_rec)}</div>
                <div class="kpi-sub">Entradas no período</div>
            </div>
        </div>
    </div>
    <div class="kpi-card despesas">
        <div class="kpi-inner">
            <div class="kpi-icon despesas">{SVG_DESPESAS}</div>
            <div class="kpi-body">
                <div class="kpi-label">Despesas</div>
                <div class="kpi-value">{fmt(total_desp)}</div>
                <span class="kpi-badge {badge_class}">{badge_sign} Líquido: {fmt(liquido)}</span>
            </div>
        </div>
    </div>
    <div class="kpi-card saldo">
        <div class="kpi-inner">
            <div class="kpi-icon saldo">{SVG_SALDO}</div>
            <div class="kpi-body">
                <div class="kpi-label">Saldo Inicial</div>
                <div class="kpi-value">{fmt(saldo_ini)}</div>
                <div class="kpi-sub">Patrimônio acumulado</div>
            </div>
        </div>
    </div>
    <div class="kpi-card caixa">
        <div class="kpi-inner">
            <div class="kpi-icon caixa">{SVG_CAIXA}</div>
            <div class="kpi-body">
                <div class="kpi-label">Caixa (Templo)</div>
                <div class="kpi-value">{fmt(caixa_tmp)}</div>
                <div class="kpi-sub">Reserva para obras</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHARTS — stacked on mobile via use_container_width
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Receitas vs Despesas por Igreja</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    df_grp = df.groupby("Igreja")[["Receitas","Despesas"]].sum().reset_index().sort_values("Receitas", ascending=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Receitas", y=df_grp["Igreja"], x=df_grp["Receitas"],
        orientation="h", marker_color=PRIMARY, marker_line_width=0,
    ))
    fig_bar.add_trace(go.Bar(
        name="Despesas", y=df_grp["Igreja"], x=df_grp["Despesas"],
        orientation="h", marker_color=DARK, marker_line_width=0,
    ))
    fig_bar.update_layout(
        barmode="group", height=260, margin=dict(l=0,r=10,t=10,b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.18, x=0, font_size=11),
        font=dict(family="Source Sans 3", color=TEXT_DARK),
        xaxis=dict(showgrid=True, gridcolor=BORDER, tickprefix="R$", tickfont_size=10),
        yaxis=dict(tickfont_size=11),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title" style="margin-top:0">Distribuição de Receitas</div>', unsafe_allow_html=True)
    df_pie = df.groupby("Igreja")["Receitas"].sum().reset_index().sort_values("Receitas", ascending=False)
    colors_pie = [PRIMARY, DARK, DARKEST, "#E07B4A", "#A83020", "#D4956A"]
    fig_pie = go.Figure(go.Pie(
        labels=df_pie["Igreja"], values=df_pie["Receitas"],
        hole=0.50,
        marker=dict(colors=colors_pie[:len(df_pie)], line=dict(color="#fff", width=2)),
        textinfo="percent",
        textfont_size=11,
        textposition="inside",
        insidetextorientation="horizontal",
        direction="clockwise",
        sort=False,
    ))
    fig_pie.update_layout(
        height=300,
        margin=dict(l=10, r=120, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.02, y=0.5,
            xanchor="left", yanchor="middle",
            font=dict(size=11, family="Source Sans 3", color=TEXT_DARK),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=30,
        ),
        font=dict(family="Source Sans 3"),
        annotations=[dict(
            text="Receitas", x=0.5, y=0.5,
            font_size=12, font_color=TEXT_MID, showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

# ── Evolução mensal ──
st.markdown('<div class="section-title">Evolução Mensal — Receitas &amp; Despesas</div>', unsafe_allow_html=True)
df_ev = df.groupby(["Ano","Mês","Data Referência"])[["Receitas","Despesas"]].sum().reset_index().sort_values(["Ano","Mês"])

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df_ev["Data Referência"], y=df_ev["Receitas"],
    name="Receitas", mode="lines+markers",
    line=dict(color=PRIMARY, width=2.5),
    marker=dict(size=7, color=PRIMARY),
    fill="tozeroy", fillcolor="rgba(191,82,35,0.07)"
))
fig_line.add_trace(go.Scatter(
    x=df_ev["Data Referência"], y=df_ev["Despesas"],
    name="Despesas", mode="lines+markers",
    line=dict(color=DARK, width=2.5, dash="dot"),
    marker=dict(size=7, color=DARK),
))
fig_line.update_layout(
    height=210, margin=dict(l=0,r=10,t=10,b=30),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", y=-0.25, x=0, font_size=11),
    font=dict(family="Source Sans 3", color=TEXT_DARK),
    xaxis=dict(showgrid=False, tickfont_size=10),
    yaxis=dict(showgrid=True, gridcolor=BORDER, tickprefix="R$", tickfont_size=10),
)
st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  TABLES
# ─────────────────────────────────────────────
def fmt_plain(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".") if v > 0 else "—"

st.markdown('<div class="section-title">Tabela Detalhada</div>', unsafe_allow_html=True)
df_show = df[["Ano","Data Referência","Igreja","Receitas","Despesas","Saldo Inicial","Caixa(Templo)","Observações"]].copy()
for col in ["Receitas","Despesas","Saldo Inicial","Caixa(Templo)"]:
    df_show[col] = df_show[col].apply(fmt_plain)
df_show["Observações"] = df_show["Observações"].replace("", "—")
st.dataframe(
    df_show.rename(columns={"Data Referência":"Referência"}),
    use_container_width=True, hide_index=True, height=320,
    column_config={
        "Ano": st.column_config.NumberColumn("Ano", format="%d", width=60),
        "Referência": st.column_config.TextColumn("Referência", width=100),
        "Igreja": st.column_config.TextColumn("Igreja", width=80),
    }
)

st.markdown('<div class="section-title">Resumo por Igreja</div>', unsafe_allow_html=True)
df_sum = df.groupby("Igreja").agg(
    Receitas=("Receitas","sum"), Despesas=("Despesas","sum"),
    Saldo_Inicial=("Saldo Inicial","sum"), Caixa_Templo=("Caixa(Templo)","sum"),
).reset_index()
df_sum["Líquido"] = df_sum["Receitas"] - df_sum["Despesas"]
for col in ["Receitas","Despesas","Saldo_Inicial","Caixa_Templo","Líquido"]:
    df_sum[col] = df_sum[col].apply(
        lambda v: f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    )
st.dataframe(
    df_sum.rename(columns={"Saldo_Inicial":"Saldo Inicial","Caixa_Templo":"Caixa (Templo)"}),
    use_container_width=True, hide_index=True,
)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dash-footer">
    <span>▪ IBF — Dashboard Financeiro</span>
    <span>Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}</span>
</div>
""", unsafe_allow_html=True)
