import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies_df = pd.DataFrame(movies_dict)

similarity = pickle.load(open("movies_sim_matrix.pkl",'rb'))

def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZDQ1ZGYxYTBkNWEwOTZiM2Q3ZGVkOTMzMGRhZGUyMSIsInN1YiI6IjY0OGRlODQzYzNjODkxMDBhZTUwY2YyOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.105YYUGfS8AlqMold_iVOcxMgPR8wgAV0z_wlR5vfOk"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    base_post_path = r"http://image.tmdb.org/t/p/w185/" 

    return base_post_path + data['poster_path']



def recommend(movie):
    movie_indx = movies_df[movies_df['title'] == movie].index[0]

    # Return the simialritie's of movie index
    distances = similarity[movie_indx]

    movies_lst = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_lst:

        movie_id = movies_df['id'].iloc[i[0]]
        
        recommended_movies.append(movies_df['title'].iloc[i[0]])
        # Fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster



st.title('Movie Recommender System')

movie_name = st.selectbox("Select a movie to recommed similar movies.",movies_df['title'].values)

if st.button('Recommend'):


    names,posters = recommend(movie_name)
        
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
