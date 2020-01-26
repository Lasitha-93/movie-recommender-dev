from math import sqrt
import pandas as pd
import numpy as np
import json

new_user_profiles = pd.read_csv('user_feature_profiles.csv')
rating_data = pd.read_csv("../resource/u1.base", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])


def feature_based_cosine_similarity(person1_id, person2_id):
    person1_profile = None
    person2_profile = None

    # get user profiles
    for index, profile in new_user_profiles.iterrows():

        if profile['user id'] == person1_id:
            person1_profile = profile

        if profile['user id'] == person2_id:
            person2_profile = profile

    # Add up all the features of each user
    person1_features_sum = 0
    person2_features_sum = 0

    person1_features = []
    person2_features = []

    p1_feature_scores = person1_profile[4:23].iteritems()
    for p1_feature_score in p1_feature_scores:
        person1_features.append(p1_feature_score[1])

    p2_feature_scores = person2_profile[4:23].iteritems()
    for p2_feature_score in p2_feature_scores:
        person2_features.append(p2_feature_score[1])

    # print(person1_features_sum,person2_features_sum)

    # person1_square_features_sum = 0
    # person2_square_features_sum = 0
    #
    # for p1_feature_score in p1_feature_scores:
    #     person1_square_features_sum += pow(p1_feature_score[1], 2)
    #
    # for p2_feature_score in p2_feature_scores:
    #     person2_square_features_sum += pow(p2_feature_score[2], 2)

    product_sum_of_both_users = 0

    # for j in range(0, 19, 1):
    #     product_sum_of_both_users += person1_features[j] * person2_features[j]
    # print(product_sum_of_both_users)
    def square_rooted(x):

        return round(sqrt(sum([a*a for a in x])),3)

    # Calculate the Cosine score
    numerator = sum(a*b for a,b in zip(person1_features,person2_features))
    denominator = square_rooted(person1_features)*square_rooted(person2_features)

    if denominator == 0:
        return 0
    else:
        r = numerator / denominator
        return r


# print(feature_based_cosine_correlation(113,134))


def user_cosine_similarity_by_features(person_id):
    # similar_users = []
    scores = []
    for i, other_person in new_user_profiles.iterrows():
        # if other_person['user id'] != person_id:
        # weighted_sim_score, sim_score = pearson_correlation_watchlist(person_id, other_person['user id'])
        sim_score = feature_based_cosine_similarity(person_id, other_person['user id'])
        scores.append([other_person['user id'], sim_score])
        # print(other_person['user id'])

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    # scores.reverse()
    return scores


# print(len(user_similarity_by_features(113)))

user_similarity_matrix = []


def create_user_features_based_cosine_sim_matrix():
    for k in range(1, 944, 1):
        u_all_sim = user_cosine_similarity_by_features(k)
        u_only_sim = []

        for u in range(0, len(u_all_sim), 1):
            u_only_sim.append(u_all_sim[u][1])

        user_similarity_matrix.append(u_only_sim)
        print(k)

    # print(len(user_similarity_matrix))
    # saving to csv
    a = np.asarray(user_similarity_matrix)
    np.savetxt("user_features_based_cosine_sim_matrix.csv", a, delimiter=",")

    df = pd.read_csv('user_features_based_cosine_sim_matrix.csv', sep=',', header=None)
    print('total rows: ', len(df))


# create_user_features_based_cosine_sim_matrix()


def make_recommendations(user_id):

    recommendation_list = {}
    user_features_based_sim_matrix = np.genfromtxt('user_features_based_cosine_sim_matrix.csv', delimiter=',')

    all_movies = np.arange(1, 1683)
    seen_movies = rating_data.loc[rating_data['user id'] == user_id]['item id'].values
    # print(seen_movies)
    # print((all_movies))
    unseen_movies = np.setdiff1d(all_movies, seen_movies)
    # print((unseen_movies))
    current_user_similarity_matrix = user_features_based_sim_matrix[(user_id - 1), :]
    # print(current_user_similarity_matrix)

    for unseen_movie in unseen_movies:
        available_highest_sim = 0
        available_best_match = 0
        sim_rating_total = 0
        total_sims = 0

        watched_users = rating_data.loc[rating_data['item id'] == unseen_movie]['user id'].values
        # print((watched_users))
        for watched_user in watched_users:
            current_other_user_sim = current_user_similarity_matrix[watched_user-1]
            if current_other_user_sim > 0:
                rating = rating_data.loc[rating_data['user id'] == watched_user]['rating'].values[0]
                sim_rating_total += rating*current_other_user_sim
                total_sims += current_other_user_sim

    #     get the rating from available_best_match
        if sim_rating_total > 0:
            predicted_rating = sim_rating_total/total_sims
            # print('movie id: ', unseen_movie, ' predicted rating: ', rating, 'best match user: ', available_best_match, 'best match user sim: ', available_highest_sim)
            recommendation_list[str(unseen_movie)] = str(predicted_rating)

        else:
            # print('movie id: ', unseen_movie, ' predicted rating: not available', 'best match user: not available', 'best match user sim: not available',)
            recommendation_list[str(unseen_movie)] = None
        # for p_id in range (1, 943, 1):
    return recommendation_list


def get_user_feature_based_rec():

    all_recommendations = {}

    for user_id in range(1, 944, 1):
        recommendation_list = make_recommendations(user_id)
        # print(recommendation_list)
        all_recommendations[str(user_id)] = recommendation_list
        print(user_id)

    # print(all_recommendations)

    with open('user_feature_based_avg_rec_cosine.json', 'w') as file:
        # indented_data=json.dumps(movies, indent=2)
        json.dump(all_recommendations, file)


get_user_feature_based_rec()