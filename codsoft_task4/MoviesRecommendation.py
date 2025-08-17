import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the movies dataset
movies = pd.read_csv("/Users/krishnakant/Desktop/CODSOFT/codsoft_task4/movies.csv")
movies

# Step 2: Fill any missing genres with empty string
movies['genres'] = movies['genres'].fillna('')

# Step 3: Convert genres into lowercase and format text
movies['genres'] = movies['genres'].str.replace('|', ' ').str.lower()

# Step 4: Initialize TF-IDF Vectorizer to convert genre text to numerical vectors
tfidf = TfidfVectorizer(stop_words='english')  
tfidf_matrix = tfidf.fit_transform(movies['genres']) 

# Step 5: Compute cosine similarity between all movies based on genre vectors
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 6: Create a mapping from movie titles to their DataFrame index
indices = pd.Series(movies.index, index=movies['title'].str.lower())

def recommend_movies(title, num_recommendations=5):
    title = title.lower().strip()

    if title in indices:
        idx = indices[title]
    else:
        matches = movies[movies['title'].str.lower().str.contains(title, na=False)]
        if matches.empty:
            return f"No movies found matching '{title}'."
        
        # Pick the best match (first one) and get its index
        idx = matches.index[0]
        print(f"No exact match found. Using closest match: '{movies.loc[idx, 'title']}'")

    # Get similarity scores for this movie with all others
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort movies by similarity score in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Skip the first one (it’s the same movie)
    sim_scores = sim_scores[1:num_recommendations+1]

    # Get indices of recommended movies
    movie_indices = [i[0] for i in sim_scores]

    return movies['title'].iloc[movie_indices]

sample_movie = input("Enter a movie title to get recommendations: ")
print(f"Recommendations for '{sample_movie}':")
print(recommend_movies(sample_movie))