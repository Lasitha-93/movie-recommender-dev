from math import sqrt
import pandas as pd
import numpy as np
import json

rating_data = pd.read_csv("../resource/u1.base", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])
new_user_profiles = pd.read_csv("../resource/u.user", delimiter="|",
                                names=["user id", "age", "gender", "occupation", "zip code"])


def pearson_correlation_watchlist(person1_id, person2_id):
    user1_rated_details_by_id = rating_data.loc[rating_data['user id'] == person1_id]
    user2_rated_details_by_id = rating_data.loc[rating_data['user id'] == person2_id]

    if len(user1_rated_details_by_id) > 5:
        user1_rated_details_by_id = user1_rated_details_by_id.head()
    if len(user2_rated_details_by_id) > 5:
        user2_rated_details_by_id = user2_rated_details_by_id.head()

    # print(len(user1_rated_details_by_id), len(user2_rated_details_by_id))

    common_list = list(set(user1_rated_details_by_id['item id']).intersection(user2_rated_details_by_id['item id']))

    person1_ratings = []
    person2_ratings = []

    for item_id in common_list:
        user1_rating = user1_rated_details_by_id.loc[user1_rated_details_by_id['item id'] == item_id]['rating']
        user2_rating = user2_rated_details_by_id.loc[user2_rated_details_by_id['item id'] == item_id]['rating']

        current_user1_rating = user1_rating.iat[0]
        current_user2_rating = user2_rating.iat[0]

        person1_ratings.append(current_user1_rating)
        person2_ratings.append(current_user2_rating)

    def square_rooted(x):

        return round(sqrt(sum([a*a for a in x])),3)

    # Calculate the Cosine score
    numerator = sum(a*b for a,b in zip(person1_ratings,person2_ratings))
    denominator = square_rooted(person1_ratings)*square_rooted(person2_ratings)

    if denominator == 0:
        return 0
    else:
        r = numerator / denominator
        return r


# print(pearson_correlation_watchlist(113, 113))


def user_similarity_by_watch_list(person_id):
    # similar_users = []
    scores = []
    for i, other_person in new_user_profiles.iterrows():
        # if other_person['user id'] != person_id:
        # weighted_sim_score, sim_score = pearson_correlation_watchlist(person_id, other_person['user id'])
        sim_score = pearson_correlation_watchlist(person_id, other_person['user id'])
        scores.append([other_person['user id'], sim_score])
        # print(other_person['user id'])

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    # scores.reverse()
    return scores


# print(user_similarity_by_features(113))
user_similarity_matrix = []


def create_watchlist_basic_sim_matrix():
    for k in range(1, 944, 1):
        u_all_sim = user_similarity_by_watch_list(k)
        u_only_sim = []

        for u in range(0, len(u_all_sim), 1):
            u_only_sim.append(u_all_sim[u][1])

        user_similarity_matrix.append(u_only_sim)
        print(k)

    # print(len(user_similarity_matrix))
    # saving to csv
    a = np.asarray(user_similarity_matrix)
    np.savetxt("first_five_watchlist_basic_cosine_sim_matrix.csv", a, delimiter=",")

    # df = pd.read_csv('watchlist_basic_sim_matrix.csv', sep=',', header=None)
    # print(len(df))


# create_watchlist_basic_sim_matrix()


def make_recommendations(user_id):

    recommendation_list = {}
    watchlist_basic_sim_matrix = np.genfromtxt('first_five_watchlist_basic_cosine_sim_matrix.csv', delimiter=',')
    # print(type(watchlist_basic_sim_matrix))
    # print(watchlist_basic_sim_matrix[0][1])

    # create header per user id
    # header_col_list = ['movie id']
    # for p_id in range(1, 944, 1):
    #     header_col_list.append(str(p_id))
    #
    # final_rec = pd.DataFrame(columns=header_col_list)
    # print(final_rec.head())
    all_movies = np.arange(1, 1683)
    seen_movies = rating_data.loc[rating_data['user id'] == user_id]['item id'].values
    # print(seen_movies)
    # print((all_movies))
    unseen_movies = np.setdiff1d(all_movies, seen_movies)
    # print((unseen_movies))
    current_user_similarity_matrix = watchlist_basic_sim_matrix[(user_id - 1), :]
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


def get_watch_list_basic_rec():

    all_recommendations = {}

    for user_id in range(1, 944, 1):
        print(user_id)
        recommendation_list = make_recommendations(user_id)
        # print(recommendation_list)
        all_recommendations[str(user_id)] = recommendation_list

    # print(all_recommendations)

    with open('first_five_watch_list_based_cosine_avg_rec.json', 'w') as file:
        # indented_data=json.dumps(movies, indent=2)
        json.dump(all_recommendations, file)

    # with open('watch_list_basic_rec.json') as file:
    #     new_data = json.load(file)
    #     indented_data=json.dumps(new_data, indent=2)
    #     print(indented_data)

    # final_list = np.asarray(all_recommendations)
    # np.savetxt("watch_list_basic_rec.csv", final_list, delimiter=",")
    #
    # df = pd.read_csv('watch_list_basic_rec.csv', sep=',', header=None)
    # print(len(df))


get_watch_list_basic_rec()
