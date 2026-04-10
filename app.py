import streamlit as st
import pickle
import pandas as pd

import requests


def fetch_poster(imdb_id):
    url = f"https://imdb236.p.rapidapi.com/api/imdb/{imdb_id}/poster"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "imdb236.p.rapidapi.com",
        "x-rapidapi-key": "d6aa72e771msh0ed784a6e55d3b8p100700jsnfc83726ff58b"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data["poster"]


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:4]

    for i in movies_list:
        st.write(movies.iloc[i[0]].title)
        st.image(fetch_poster(movies.iloc[i[0]].imdb_id))

st.title("Movie Recommender")

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,
)


if st.button("Recommend"):
    recommend(selected_movie_name)
    