from math import sqrt
import pandas as pd

rating_data = pd.read_csv("resource/u.data", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])
new_user_profiles = pd.read_csv('new_user_profiles.csv')


def pearson_correlation_watchlist(person1_id, person2_id):

    user1_rated_details_by_id = rating_data.loc[rating_data['user id'] == person1_id]
    user2_rated_details_by_id = rating_data.loc[rating_data['user id'] == person2_id]

    common_list = list(set(user1_rated_details_by_id['item id']).intersection(user2_rated_details_by_id['item id']))
    # print(common_list)
    person1_features_sum = 0
    person2_features_sum = 0
    person1_square_features_sum = 0
    person2_square_features_sum = 0

    product_sum_of_both_users = 0

    for item_id in common_list:
        user1_rating = user1_rated_details_by_id.loc[user1_rated_details_by_id['item id'] == item_id]['rating']
        user2_rating = user2_rated_details_by_id.loc[user2_rated_details_by_id['item id'] == item_id]['rating']

        current_user1_rating = user1_rating.iat[0]
        current_user2_rating = user2_rating.iat[0]

        person1_features_sum += current_user1_rating
        person2_features_sum += current_user2_rating

        person1_square_features_sum += pow(person1_features_sum, 2)
        person2_square_features_sum += pow(person2_features_sum, 2)

        product_sum_of_both_users += current_user1_rating*current_user2_rating

    # print(person1_features_sum, person2_features_sum, person1_square_features_sum, person2_square_features_sum, product_sum_of_both_users)
    # calculating pearson similarity:
    if len(common_list) != 0:
        numerator_value = product_sum_of_both_users - (
                    person1_features_sum * person2_features_sum / len(common_list))
        denominator_value = sqrt(
            (person1_square_features_sum - pow(person1_features_sum, 2) / len(common_list)) * (
                    person2_square_features_sum - pow(person2_features_sum, 2) / len(common_list)))
        if denominator_value == 0:
            return 0, 0
        else:
            r = numerator_value / denominator_value
            # adding weight according to the number of common movies
            weighted_r = r*len(common_list)/len(user1_rated_details_by_id)
            return weighted_r, r
    else:
        return 0, 0


# print(pearson_correlation_watchlist(113,13))


def user_similarity_by_features(person_id):
    # similar_users = []
    scores = []
    for i, other_person in new_user_profiles.iterrows():
        if other_person['user id'] != person_id:
            weighted_sim_score, sim_score = pearson_correlation_watchlist(person_id, other_person['user id'])
            scores.append([weighted_sim_score, sim_score, other_person['user id']])
            print(other_person['user id'])

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    return scores


print('users:', len(user_similarity_by_features(113)))
