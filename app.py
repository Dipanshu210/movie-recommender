import pandas as pd
import pickle
import streamlit as st
import requests
import os


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8ad39994975564bdd0e701b723e3c4e1"
        data = requests.get(url, timeout=10)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies_name = []
    recommended_movies_poster = []
    
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
        
    return recommended_movies_name, recommended_movies_poster

st.header("Movies Recommendation System Using Machine Learning")

movies = pd.read_pickle("artifacts/movie_list.pkl")
similarity = pd.read_pickle("artifacts/similarity.pkl")

movie_list = movies['title'].values

# Only one selectbox is needed
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation',
    movie_list
)

# After this, you would usually add a button and the recommendation logic
if st.button('Show Recommendation'):
    recommended_movies_name , recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])
    