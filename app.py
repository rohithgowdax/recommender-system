import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))  # Ensure this DataFrame contains 'title' and 'movie_id'
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=14cc2b05e6730257bc2115ea0460ffee&language=en-US'
    response = requests.get(url)
    data = response.json()

    # Check if 'poster_path' exists in the response
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500"  # Fallback image

def recommend(movie):
    try:
        # Find movie index
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        # Sort and pick top 5
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            # Use correct TMDb movie_id
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        # Handle all exceptions
        st.error(f"Error: {e}")
        return ["No recommendations available"], ["https://via.placeholder.com/500"]

# Streamlit App
st.title('Movie Recommender System')

# Dropdown for movie selection
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Recommendation button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.write("Recommended Movies:")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
