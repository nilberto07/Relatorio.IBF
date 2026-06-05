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
    
    PRIMARY = "#BF5223"
    DARK    = "#7D0911"
    DARKEST = "#5A1F05"
    BORDER  = "#E8D5C8"
    TEXT_SOFT = "#9E7E6A"
    TEXT_DARK = "#1A0A02"

    .page-header {{
    display: flex; align-items: center; gap: 1.1rem;
    padding: 0.8rem 0 1.2rem;
    border-bottom: 3px solid {BORDER};
    margin-bottom: 1.8rem;
    }}
    .page-header-logo {{
        width: 48px; height: 48px; flex-shrink: 0;
        background: linear-gradient(135deg, {DARKEST}, {PRIMARY});
        border-radius: 11px;
        display: flex; align-items: center; justify-content: center;
    }}
    .page-header h1 {{
        font-family: 'Playfair Display', serif;
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        font-weight: 700; color: {DARKEST}; margin: 0 0 2px; line-height: 1.2;
    }}
    .page-header p {{
        font-size: 0.76rem; color: {TEXT_SOFT}; margin: 0;
        text-transform: uppercase; letter-spacing: .1em; font-weight: 600;
    }}

    /* ── Month block ── */
    .month-block {{
        margin-bottom: 1.8rem;
        border-radius: 11px;
        overflow: hidden;
        border: 1px solid {BORDER};
        box-shadow: 0 2px 8px rgba(90,31,5,.06);
    }}
    .month-header {{
        background: linear-gradient(90deg, {DARKEST} 0%, {DARK} 100%);
        padding: 0.7rem 1.2rem;
        display: flex; align-items: center; justify-content: space-between;
        gap: 0.8rem; flex-wrap: wrap;
    }}
    .month-header h2 {{
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem; font-weight: 700; color: #fff; margin: 0;
    }}
    .month-pills {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .mpill {{
        font-size: 0.67rem; font-weight: 700; padding: 2px 9px;
        border-radius: 20px; white-space: nowrap; letter-spacing: .05em;
    }}
    .mpill-r  {{ background: rgba(255,255,255,.18); color: #fff; }}
    .mpill-d  {{ background: rgba(255,255,255,.1);  color: rgba(255,255,255,.85); }}
    .mpill-lp {{ background: #E8F7EC; color: #1E7A3C; }}
    .mpill-ln {{ background: #FDEAEA; color: #C0392B; }}

    /* ── Table ── */
    .month-table-wrap {{ overflow-x: auto; background: #fff; }}
    table.rel {{
        width: 100%; border-collapse: collapse;
        font-family: 'Source Sans 3', sans-serif; font-size: 0.82rem;
    }}
    table.rel thead tr {{ background: #FDF6F0; }}
    table.rel thead th {{
        padding: 9px 13px; text-align: left;
        font-size: 0.67rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: .09em;
        color: {TEXT_SOFT}; border-bottom: 2px solid {BORDER}; white-space: nowrap;
    }}
    table.rel thead th.r {{ text-align: right; }}
    table.rel tbody tr {{ border-bottom: 1px solid {BORDER}; }}
    table.rel tbody tr:hover {{ background: #FDF6F0; }}
    table.rel tbody td {{ padding: 8px 13px; color: {TEXT_DARK}; white-space: nowrap; }}
    table.rel tbody td.r  {{ text-align: right; font-variant-numeric: tabular-nums; }}
    table.rel tbody td.ch {{ font-weight: 700; color: {DARKEST}; }}
    table.rel tfoot tr    {{ background: {DARKEST}; }}
    table.rel tfoot td    {{
        padding: 9px 13px; font-weight: 700; font-size: 0.82rem; color: #fff; white-space: nowrap;
    }}
    table.rel tfoot td.r  {{ text-align: right; font-variant-numeric: tabular-nums; }}

    /* ── Rel footer ── */
    .rel-footer {{
        margin-top: 2rem; padding-top: 0.9rem; border-top: 1px solid {BORDER};
        display: flex; flex-wrap: wrap; justify-content: space-between; gap: .4rem;
        font-size: 0.7rem; color: {TEXT_SOFT}; font-weight: 600;
        text-transform: uppercase; letter-spacing: .06em;
    }}

    @media print {{
        @page {{ size: A4 portrait; margin: 12mm 10mm; }}
        [data-testid="stSidebar"], [data-testid="stHeader"],
        [data-testid="collapsedControl"], footer {{ display: none !important; }}
        .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        .month-block {{ box-shadow: none !important; page-break-inside: avoid; margin-bottom: 12px; }}
        table.rel {{ font-size: 0.72rem; }}
        table.rel thead th, table.rel tbody td, table.rel tfoot td {{ padding: 5px 9px; }}
    }}
    </style>
    """, unsafe_allow_html=True)