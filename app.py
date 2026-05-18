import streamlit as st
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

st.set_page_config(
    page_title="Financeiro das Igrejas - IBF",
    page_icon="⛪",
    layout="wide", #Tela cheia
    #initial_sidebar_state="expanded" #Sidebar expandida por padrão
)

st.markdown("# ⛪ Dashboard Financeiro", text_alignment="center")

home   = st.Page("pages/home.py",   title="Página Principal",         icon="🏷️", default=True)
export = st.Page("pages/export.py", title="Relatório Assembleia Geral", icon="📊")

pg = st.navigation({"Navegação": [home, export]})
pg.run()





# ── Rodapé ───────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85rem;'>
    Dashboard Financeiro — IBF &nbsp;|&nbsp; Atualizado automaticamente via Google Sheets &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)

