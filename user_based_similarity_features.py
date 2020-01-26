# pearson similarity of users related to a particular based on their feature ratings in the profile
import json
from math import sqrt

with open('resources/1000users_with_ratings.json') as file:
    data = json.load(file)
    user_data = data['users']


# print(user_data)
# two users as inputs
def pearson_correlation(person1, person2):
    person1_profile = None
    person2_profile = None

    # get user profiles
    for user in user_data:

        if user['user']['name'] == person1:
            # print(user['user']['name'])
            person1_profile = user

        if user['user']['name'] == person2:
            # print(user['user']['name'])
            person2_profile = user

    # Add up all the features of each user
    person1_features_sum = 0
    person2_features_sum = 0

    for feature in person1_profile['user']['features']:
        person1_features_sum += person1_profile['user']['features'].get(feature)

    for feature in person2_profile['user']['features']:
        person2_features_sum += person2_profile['user']['features'].get(feature)

    person1_square_features_sum = 0
    person2_square_features_sum = 0

    for feature in person1_profile['user']['features']:
        person1_square_features_sum += pow(person1_profile['user']['features'].get(feature), 2)

    for feature in person2_profile['user']['features']:
        person2_square_features_sum += pow(person2_profile['user']['features'].get(feature), 2)

    product_sum_of_both_users = 0

    for feature in person1_profile['user']['features']:
        product_sum_of_both_users += person1_profile['user']['features'].get(feature) * person2_profile['user'][
            'features'].get(feature)

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
            person1_features_sum * person2_features_sum / len(person1_profile['user']['features']))
    denominator_value = sqrt(
        (person1_square_features_sum - pow(person1_features_sum, 2) / len(person1_profile['user']['features'])) * (
                person2_square_features_sum - pow(person2_features_sum, 2) / len(person1_profile['user']['features'])))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r


# print(pearson_correlation('Harvey Glover', 'Lillian Dennis'))


def user_similarity_by_features(person):
    similar_users = []
    scores = [(pearson_correlation(person, other_person['user']['name']), other_person['user']['name']) for other_person
              in user_data if
              other_person['user']['name'] != person]

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
    for j in range(0, len(scores)):
        similar_user_model = {'user': {'name': None, 'score': None}}
        similar_user_model['user']['name'] = scores[j][1]
        similar_user_model['user']['score'] = scores[j][0]

        similar_users.append(similar_user_model)
    return similar_users


# print(user_similarity_by_features('Harvey Glover')[0:5])

# for other_person in user_data:
#     print(other_person['user']['name'])
