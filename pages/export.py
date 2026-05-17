import streamlit as st
from streamlit_gsheets import GSheetsConnection
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


st.header("Relatório da Assembleia Geral")

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
st.write(df)