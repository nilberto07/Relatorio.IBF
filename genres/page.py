import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

#Locado
genres = [
    {'id': 1, 'name': 'Ação'},
    {'id': 2, 'name': 'Comédia'},
    {'id': 3, 'name': 'Drama'},
]

def show_genres():
    st.write("Gêneros de Filmes")
    #AgGrid(
    #    data=pd.DataFrame(genres),
    #    reload_data=True,
    #)
    st.dataframe(genres)

    st.title("Cadastrar Novo Gênero")
    name = st.text_input("Nome do Gênero")
    if st.button("Cadastrar"):
        new_genre = {'id': len(genres) + 1, 'name': name}
        genres.append(new_genre)
        st.success(f"Gênero '{name}' cadastrado com sucesso!")

