from pathlib import Path
from typing import Tuple, List
import implicit
import scipy
from implicit.datasets.lastfm import get_lastfm
import spotify
import numpy as np
from scipy.sparse import coo_matrix, hstack

class ImplicitRecommender:
    def __init__(self, artists: List['str'], users: List['str'],
                    implicit_model: implicit.recommender_base.RecommenderBase):
        self.model = implicit_model
        self.artists = artists
        self.users = users

    #Fits the recommender with a sparse csr matrix of user id's and artist id's
    def fit(self, user_artist_matrix: scipy.sparse.csr_matrix) -> None:
        self.model.fit(user_artist_matrix)

    #Takes a userID and his listening history, and recommends artists using ALS model
    def recommend(self, user_id: int, user_artist_matrix, n: int = 10):
        artist_ids, scores = self.model.recommend(user_id, user_artist_matrix[n])
        artist_names = []

        for id in artist_ids:
            artist_names.append(self.artists[id])
        
        return artist_names, scores

def main():
    #Load the dataset of user to artist relationships
    artists, users, artist_user_plays = get_lastfm()
    users = np.append(users, 'ena456')

    my_profile = spotify.SpotipyWrapper('ena456', '', '')
    my_profile.recommend_playlists()
    artist_names = my_profile.get_artist_names()
    artist_freq = my_profile.get_artist_freq()
    user_profile = [0] * len(artists)

    for i, artist in enumerate(artists):
        if artist in artist_names:
            user_profile[i] += artist_freq[artist]
    new_col = coo_matrix(user_profile)
    new_col = new_col.reshape(-1, 1)

    #Add user column
    artist_user_plays = hstack([artist_user_plays, new_col])

    user_plays = artist_user_plays.T.tocsr()

    #Initialize ALS model with Implicit library
    implicit_model = implicit.als.AlternatingLeastSquares(
        factors=50, iterations=10, regularization=0.01
    )

    #Create recommender object and fit using user artist matrix
    recommender = ImplicitRecommender(artists, users, implicit_model)
    recommender.fit(user_plays)

    #Recommend a user artists
    artists, scores = recommender.recommend(len(users)-1, user_plays)

    for artist, score in zip(artists, scores):
        print(f"{artist}: {score}")

if __name__ == "__main__":
    main()