import streamlit as st


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
GREEN     = "#1E7A3C"
GREEN_BG  = "#E8F7EC"
RED       = "#C0392B"
RED_BG    = "#FDEAEA"

def load_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Source Sans 3', sans-serif;
        background-color: #ffffff;
        color: {TEXT_DARK};
    }}
    .main .block-container {{
        padding: 2rem 2rem 3rem;
        max-width: 1200px;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(170deg, {DARKEST} 0%, {DARK} 60%, {PRIMARY} 100%);
        border-right: none;
    }}
    [data-testid="stSidebar"] * {{ color: #fff !important; }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {{
        color: rgba(255,255,255,255) !important;
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
    [data-testid="stSidebarNavSeparator"] {{
        border-color: #00000000 !important;
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

    /*relatorio mensal*/
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