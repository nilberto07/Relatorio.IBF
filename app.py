import streamlit as st
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

st.set_page_config(
    page_title="Financeiro das Igrejas",
    page_icon="⛪",
    layout="wide", #Tela cheia
    #initial_sidebar_state="expanded" #Sidebar expandida por padrão
)

def load_css(filepath: str):
    """Carrega um arquivo CSS e aplica globalmente no app."""
    with open(filepath, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega o CSS global
load_css("styles/global.css")

st.title("⛪ Dashboard Financeiro - IBF")

home   = st.Page("pages/home.py",   title="Página Principal",         icon="🏷️", default=True)
export = st.Page("pages/export.py", title="Relatório Assembleia Geral", icon="📊")

pg = st.navigation({"Navegação": [home, export]})
pg.run()

