import pandas as pd
import numpy as np
import json

user_profiles = pd.read_csv('./data/user_feature_profiles.csv')
with open('./data/heat_movies.json') as file:
    new_data = json.load(file)


def now_showing_rec(user_id):

    user_profile = None

    for index, profile in user_profiles.iterrows():

        if profile['user id'] == user_id:
            user_profile = profile

    if user_profile is None:
        return "invalid user id!"

    user_feature_scores = user_profile[4:23].iteritems()

    feature_n_score = []

    for feature_score in user_feature_scores:
        feature_n_score.append([feature_score[1], feature_score[0]])

    feature_n_score.sort()
    feature_n_score.reverse()
    first_three_features = feature_n_score[:3]
    print("user's",first_three_features)

    movies = new_data['intheatres']
    suggesting_movies = []

    for movie in movies:
        print(movie['genres'])
        if len(np.intersect1d(movie['genres'], [i[1] for i in first_three_features])) > 0:
            suggesting_movies.append(movie)

    return suggesting_movies


print(now_showing_rec(17))
