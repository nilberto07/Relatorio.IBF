import streamlit as st

st.set_page_config(
    page_title="Dashboard Corporativo",
    layout="wide"
)

# =========================
# CSS CUSTOMIZADO
# =========================
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
            #B87455 70%,
            #5A1F05 100%
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

    padding: 1.2rem;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.15);

    margin-bottom: 1rem;
}

/* ===== TEXTO ===== */
h1, h2, h3, h4, h5, h6 {
    color: #3D1607;
    font-weight: 700;
}

p, label, div {
    color: #2E2E2E;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {

    background: rgba(90, 31, 5, 0.92);

    border-right: 1px solid rgba(255,255,255,0.15);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CONTEÚDO
# =========================

st.title("Dashboard Corporativo")

st.write("Layout moderno com glassmorphism, ondas e tema elegante.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vendas", "R$ 125.000")

with col2:
    st.metric("Clientes", "1.248")

with col3:
    st.metric("Conversão", "18%")

st.divider()

with st.container():
    st.subheader("Filtros")

    nome = st.text_input("Nome")

    categoria = st.selectbox(
        "Categoria",
        ["Financeiro", "Comercial", "Operacional"]
    )

    st.button("Aplicar")