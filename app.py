import streamlit as st
import pickle
import pandas as pd
import requests


# https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US
# 06a4272d14d59c375bfc207a8fd1731f
# https://image.tmdb.org/t/p/w185/

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=06a4272d14d59c375bfc207a8fd1731f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # poster fetching
        recommend_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommend_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommendation System')
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.selectbox('Select your movie', movies['title'].values)

if st.button ('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])



