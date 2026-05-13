import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Create a simple dataset
data = {
    'movie_id': [1, 2, 3, 4, 5],
    'title': ['The Matrix', 'John Wick', 'Toy Story', 'Shrek', 'Inception'],
    'genres': ['Action Sci-Fi', 'Action Thriller', 'Animation Kids Comedy', 'Animation Kids Fantasy', 'Action Sci-Fi Thriller']
}

df = pd.DataFrame(data)

# 2. Convert genres into a matrix of token counts
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['genres'])

# 3. Compute the Cosine Similarity matrix
cosine_sim = cosine_similarity(count_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df[df['title'] == title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 3 most similar movies (excluding itself)
    sim_scores = sim_scores[1:4]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 3 most similar movies
    return df['title'].iloc[movie_indices]

# Test the system
print("Recommendations for 'The Matrix':")
print(get_recommendations('The Matrix'))