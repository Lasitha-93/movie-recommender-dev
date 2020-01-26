# pearson similarity of users related to a particular based on the movies watched in common
import json
from math import sqrt

with open('resources/users_watched_movies_list_test.json') as file:
    data = json.load(file)
    user_data = data['users']

highest_no_of_matches = 0


def pearson_correlation_movie(person1, person2):
    global highest_no_of_matches
    person1_profile = None
    person2_profile = None

    person1_movie_list = {'movies': []}
    # get user profiles
    for user in user_data:

        if user['user']['name'] == person1:
            # print(user['user']['name'])
            person1_profile = user

        if user['user']['name'] == person2:
            # print(user['user']['name'])
            person2_profile = user

    # print(len(person1_profile['user']['movies']))
    # print(person1_profile['user']['watched_total'])
    # print(len(person2_profile['user']['movies']))
    # print(person2_profile['user']['watched_total'])

    for movie in person1_profile['user']['movies']:
        movie_model = {'movie': {'title': None, 'rating': None}}

        movie_model['movie']['title'] = movie['movie']['title']
        movie_model['movie']['rating'] = movie['movie']['rating']

        person1_movie_list['movies'].append(movie_model)

    number_of_matches = 0
    person1_features_sum = 0
    person2_features_sum = 0

    person1_square_features_sum = 0
    person2_square_features_sum = 0

    product_sum_of_both_users = 0

    for person1_item in person1_movie_list['movies']:
        current_movie = person1_item['movie']['title']
        # print(current_movie)

        for person2_item in person2_profile['user']['movies']:
            if person2_item['movie']['title'] == current_movie:
                # print(person2_item['movie']['title'])
                person1_features_sum += person1_item['movie']['rating']
                person2_features_sum += person2_item['movie']['rating']

                person1_square_features_sum += pow(person1_item['movie']['rating'], 2)
                person2_square_features_sum += pow(person2_item['movie']['rating'], 2)

                product_sum_of_both_users += person1_item['movie']['rating']*person2_item['movie']['rating']

                number_of_matches += 1

    if number_of_matches == 0:
        return 0
    if number_of_matches > highest_no_of_matches:
        highest_no_of_matches = number_of_matches
    # print(number_of_matches)
    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (
            person1_features_sum * person2_features_sum / number_of_matches)

    denominator_value = sqrt(
        (person1_square_features_sum - pow(person1_features_sum, 2) / number_of_matches) * (
                person2_square_features_sum - pow(person2_features_sum, 2) / number_of_matches))

    # print(person1_features_sum)
    # print(person2_features_sum)
    # print(person1_square_features_sum)
    # print(person2_square_features_sum)
    # print(product_sum_of_both_users)
    # print(numerator_value)
    # print(denominator_value)
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r*number_of_matches


# print(pearson_correlation_movie('Jared Flowers', 'Glenn Barton'))


def user_similarity_by_watchlist(person):
    similar_users = []
    scores = [(pearson_correlation_movie(person, other_person['user']['name']), other_person['user']['name']) for other_person in user_data if
              other_person['user']['name'] != person]

    # Sort the similar persons so that highest scores person will appear at the first
    scores.sort()
    scores.reverse()
    # for user in user_data:
    #
    #     if user['user']['name'] == scores[0][1]:
    #         print(user)
    #
    #     if user['user']['name'] == person:
    #         print(user)
    # print(scores[998][0])
    # scale the similarity values between 1-0
    highest_value = 0
    for user in user_data:

        if user['user']['name'] == person:
            highest_value = user['user']['watched_total']
    # print('user watched : ' + str(highest_value))
    # print('highest match : ' + str(highest_no_of_matches))
    for j in range(0, len(scores)):
        similar_user_model = {'user': {'name': None, 'score': None}}
        similar_user_model['user']['name'] = scores[j][1]
        similar_user_model['user']['score'] = scores[j][0]/highest_value

        similar_users.append(similar_user_model)
    return similar_users


# print(user_similarity_by_watchlist('Jared Flowers')[0:5])

