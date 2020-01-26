import random
import pandas as pd
import json
from support_functions import getagewatched, getagewiserating


user_watch_list = {'users': []}

movie_model = {'movie': {'title': None, 'age_watched': None, 'rating': None}}

with open('crawler/movie_list_5000.json') as file:
    data = json.load(file)
    movies = data['movies']

movie_data = movies
user_data = pd.read_csv('resources/1000users_with_ratings.csv', low_memory=False)
all_user_watch_total = 0

for i in range(0, 1000, 1):
    current_user = user_data.loc[i]
    user_model = {'user': {'name': None, 'watched_total': None, 'movies': []}}
    user_model['user']['name'] = current_user['name']

    no_watched_movies = random.randint(50, 400)
    movies_watched = random.sample(range(1, 500), no_watched_movies)
    len_movies_watched = len(movies_watched)
    print('given amount: '+str(len_movies_watched))
    real_count = 0
    user_model['user']['watched_total'] = len_movies_watched

    all_user_watch_total += len_movies_watched

    for j in range(0, len_movies_watched, 1):
        movie_model = {'movie': {'title': None, 'age_watched': None, 'rating': None}}
        movie_index = movies_watched[j]
        current_movie = movie_data[movie_index]

        movie_model['movie']['title'] = current_movie['movie']['title']
        movie_model['movie']['age_watched'] = getagewatched(int(current_user['age']), int(current_movie['movie']['year']))
        movie_model['movie']['rating'] = getagewiserating(current_user, current_movie)

        user_model['user']['movies'].append(movie_model)
        real_count += 1

    print('real count: '+str(real_count))
    user_watch_list['users'].append(user_model)
    print(str(i)+" : "+str(current_user['name'])+" "+str(len_movies_watched)+"\n")

print('total movies by each user :'+str(all_user_watch_total))
with open('users_watched_movies_list_test.json', 'w') as f2:
    # indented_data=json.dumps(movies, indent=2)
    json.dump(user_watch_list, f2)
