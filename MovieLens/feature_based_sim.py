from math import sqrt
import pandas as pd

new_user_profiles = pd.read_csv('new_user_profiles.csv')


def pearson_correlation(person1_id, person2_id):
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
        person1_features_sum += p1_feature_score[1]
        person1_features.append(p1_feature_score[1])

    p2_feature_scores = person2_profile[4:23].iteritems()
    for p2_feature_score in p2_feature_scores:
        person2_features_sum += p2_feature_score[1]
        person2_features.append(p2_feature_score[1])

    # print(person1_features_sum,person2_features_sum)

    person1_square_features_sum = 0
    person2_square_features_sum = 0

    for p1_feature_score in p1_feature_scores:
        person1_square_features_sum += pow(p1_feature_score[1], 2)

    for p2_feature_score in p2_feature_scores:
        person2_square_features_sum += pow(p2_feature_score[2], 2)

    product_sum_of_both_users = 0

    for j in range(0, 19, 1):
        product_sum_of_both_users += person1_features[j] * person2_features[j]
    # print(product_sum_of_both_users)

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
            person1_features_sum * person2_features_sum / 19)
    denominator_value = sqrt(
        (person1_square_features_sum - pow(person1_features_sum, 2) / 19) * (
                person2_square_features_sum - pow(person2_features_sum, 2) / 19))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r


# print(pearson_correlation(113,134))


def user_similarity_by_features(person_id):
    # similar_users = []
    scores = []
    for i, other_person in new_user_profiles.iterrows():
        if other_person['user id'] != person_id:
            sim_score = pearson_correlation(person_id, other_person['user id'])
            scores.append([sim_score, other_person['user id']])
            print(other_person['user id'])

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    # for user in user_data:
    #
    #     if user['user']['name'] == scores[0][1]:
    #         print(user)
    #     if user['user']['name'] == person:
    #         print(user)
    # print(scores[0][1])
    # highest_value = float(scores[0][0])
    # print(len(scores))
    # for j in range(0, len(scores)):
    #     similar_user_model = {'user': {'name': None, 'score': None}}
    #     similar_user_model['user']['name'] = scores[j][1]
    #     similar_user_model['user']['score'] = scores[j][0]
    #
    #     similar_users.append(similar_user_model)
    return scores


print(user_similarity_by_features(113))
