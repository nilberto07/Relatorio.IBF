import streamlit as st
import ssl
from utils.theme import load_css

load_css()

ssl._create_default_https_context = ssl._create_stdlib_context

st.set_page_config(
    page_title="Dashboard Financeiro — IBF",
    page_icon="styles/logo.png",
    layout="wide",
    #initial_sidebar_state="collapsed",   # collapsed by default on mobile
)

st.logo(
    "styles/logo.png",
    size="large",
    )

#st.markdown("""
#<div class="dash-header">
#    <h1>Igreja da Filadélfia</h1>
#    <p>Relatório · Assembleia Geral</p>
#</div>
#""", unsafe_allow_html=True)

relatorio = st.Page("pages/relatorio_mensal.py", title="Relatório Assembleia Geral", default=True)
home   = st.Page("pages/home.py",   title="Relatório Detalhado")
export   = st.Page("pages/export.py",   title="Exportar Relatório da Assembleia")

pg = st.navigation({"Navegação": [relatorio, home, export]})
pg.run()





# ── Rodapé ───────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; color: black; font-size: 0.85rem;'>
    Dashboard Financeiro — IBF &nbsp;|&nbsp; Atualizado automaticamente via Google Sheets &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)

