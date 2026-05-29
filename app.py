import streamlit as st
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

st.set_page_config(
    page_title="Financeiro das Igrejas - IBF",
    page_icon="styles/logo.png",
    layout="wide", #Tela cheia
    #initial_sidebar_state="expanded" #Sidebar expandida por padrão
)

st.logo(
    "styles/logo.png",
    size="large",
    )

st.markdown("""
<style>

/* ===== FUNDO GERAL ===== */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(255,255,255,0.9) 0%, transparent 30%),
        radial-gradient(circle at bottom right, rgba(255,255,255,0.12) 0%, transparent 25%),
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #F4E5DE 30%,
            #ffa47a 70%,
            #d54606 100%
        );

    background-attachment: fixed;
}

/* ===== CONTAINERS GLASSMORPHISM ===== */
[data-testid="stVerticalBlock"] > div:has(.element-container),
div[data-testid="stForm"],
div[data-testid="stExpander"] {

    background: rgba(255,255,255,0.15);

    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.25);

    border-radius: 22px;

    padding: 0.8rem;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.15);

    margin-bottom: 1rem;
}


/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgb(45 14 0 / 92%);
}

section[data-testid="stSidebar"] * {
    #color: black !important;
}
            
/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    
}

</style>
""", unsafe_allow_html=True)

st.markdown("# Dashboard Financeiro", text_alignment="center")

home   = st.Page("pages/home.py",   title="Página Principal",         icon="🏷️", default=True)
export = st.Page("pages/export.py", title="Relatório Assembleia Geral", icon="📊")

pg = st.navigation({"Navegação": [home, export]})
pg.run()





# ── Rodapé ───────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; color: black; font-size: 0.85rem;'>
    Dashboard Financeiro — IBF &nbsp;|&nbsp; Atualizado automaticamente via Google Sheets &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)

