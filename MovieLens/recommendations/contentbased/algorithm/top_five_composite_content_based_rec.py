from math import sqrt
import pandas as pd
import numpy as np
import json

new_user_profiles = pd.read_csv('../data/first_five_comp_profiles.csv')
new_movie_profiles = pd.read_csv('../data/new_movie_profiles.csv', encoding='ISO-8859-13')
rating_data = pd.read_csv("../data/u1.base", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])


def feature_based_pearson_similarity(user_id, movie_id):
    user_profile = None
    movie_profile = None

    # get user profiles
    for index, profile in new_user_profiles.iterrows():

        if profile['user id'] == user_id:
            user_profile = profile

    # get movie profile
    for index, profile in new_movie_profiles.iterrows():

        if profile['movie id'] == movie_id:
            movie_profile = profile

    # Add up all the features of each user
    movie1_features_sum = 0
    movie2_features_sum = 0

    movie1_features = []
    movie2_features = []

    user_feature_scores = user_profile[4:23].iteritems()
    for m1_feature_score in user_feature_scores:
        # print(m1_feature_score[1])
        movie1_features_sum += m1_feature_score[1]
        movie1_features.append(m1_feature_score[1])
    # print(movie1_features)

    movie_feature_scores = movie_profile[3:22].iteritems()
    for m2_feature_score in movie_feature_scores:
        movie2_features_sum += m2_feature_score[1]
        movie2_features.append(m2_feature_score[1])
    # print(movie2_features)

    # print(movie1_features_sum, movie2_features_sum)

    movie1_square_features_sum = 0
    movie2_square_features_sum = 0

    for movie1_feature in movie1_features:
        movie1_square_features_sum += pow(movie1_feature, 2)

    for movie2_feature in movie2_features:
        movie2_square_features_sum += pow(movie2_feature, 2)

    product_sum_of_both_movies = 0

    for j in range(0, len(movie1_features), 1):
        product_sum_of_both_movies += movie1_features[j] * movie2_features[j]
    # print(product_sum_of_both_users)

    # Calculate the pearson score
    numerator_value = product_sum_of_both_movies - (
            movie1_features_sum * movie2_features_sum / len(movie1_features))
    denominator_value = sqrt(
        (movie1_square_features_sum - pow(movie1_features_sum, 2) / len(movie1_features)) * (
                movie2_square_features_sum - pow(movie2_features_sum, 2) / len(movie1_features)))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        # print(r)
        return r


# feature_based_pearson_similarity(113, 345)


def movie_pearson_similarity_rec_by_features(user_id):
    # similar_users = []
    scores = []
    for i, other_movie in new_movie_profiles.iterrows():
        if other_movie['movie id'] != user_id:
            # weighted_sim_score, sim_score = pearson_correlation_watchlist(person_id, other_person['user id'])
            sim_score = feature_based_pearson_similarity(user_id, other_movie['movie id'])
            if sim_score > 0:
                # sim  = 1 means it's exactly the user preference. therefore multiply the sim by 5 and get the predicted rating
                pred_rating = sim_score * 5
                scores.append([pred_rating, other_movie['movie id']])
        else:
            continue
        print(other_movie['movie id'])

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores


# print(movie_pearson_similarity_by_features(113))


# def make_recommendations(user_id):
#     # recommendation_list = {}
#     # using same similarity matrix as user_feature_based_rec since the modification is made in calculating similarity, this function
#     # user_features_based_sim_matrix = np.genfromtxt('user_features_based_sim_matrix.csv', delimiter=',')
#
#     # all_movies = np.arange(1, 1683)
#     seen_movies = rating_data.loc[rating_data['user id'] == user_id].sort_values(by=['rating'], ascending=False)
#     top_high_five = seen_movies.head()
#     # print(top_high_five)
#     all_weighted_by_ratings = []
#     top_five_id = []
#     count = 1
#     for item in top_high_five.iterrows():
#         # print('current movie: ', count)
#         # current_movie = movie_pearson_similarity_by_features(item[1]['item id'], item[1]['rating'])
#         # all_weighted_by_ratings += current_movie
#         # count += 1
#         top_five_id.append(item[1]['item id'])
#
#     all_weighted_by_ratings.sort()
#     all_weighted_by_ratings.reverse()
#
#     return all_weighted_by_ratings
#
#
# # print(feature_based_pearson_similarity(2, 4))


def get_user_feature_based_rec():
    all_recommendations = {}

    for user_id in range(1, 101, 1):

        print('working on id: ', user_id)
        recommendation_list = movie_pearson_similarity_rec_by_features(user_id)
        recommendation_list_dict = {}
        # print(recommendation_list)
        for i in range(0, len(recommendation_list), 1):
            recommendation_list_dict[str(recommendation_list[i][1])] = recommendation_list[i][0]
        all_recommendations[str(user_id)] = recommendation_list_dict

    # print(all_recommendations)

    with open('five_movies_user_feature_based_rec.json', 'w') as file:
        # indented_data=json.dumps(movies, indent=2)
        json.dump(all_recommendations, file)


get_user_feature_based_rec()
