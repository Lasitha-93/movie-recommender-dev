import random


def getage():
    number_range = ["1", "2", "3", "4", "5", "6"]
    picked = random.choices(number_range, weights=[2, 6, 5, 3, 2, 1], k=1)
    if int(picked[0]) == 1:
        age = int(picked[0]) * 10 + random.randint(6, 9)
        return age
    else:
        age = int(picked[0]) * 10 + random.randint(0, 9)
        return age


def getfeaturerating():
    rating = round(random.uniform(1, 10), 1)
    return rating


def getagewatched(user_age, movie_year):
    years_passed = 2018 - movie_year
    year_watched = random.randint(0, years_passed)

    # if user is less than 15years of age when he/she happened to watch the movie it should not be considered
    if (user_age - year_watched) < 16:
        return user_age

    else:
        return user_age - year_watched


def getagewiserating(user, movie_watched):
    # making the rating somewhat bias towards the age to get a proper diversity
    if ('Romance' in movie_watched['movie']['genres'] or 'Comedy' in movie_watched['movie']['genres'] or 'Drama' in movie_watched['movie'][
        'genres']) and (
            'Thriller' not in movie_watched['movie']['genres'] or 'Crime' not in movie_watched['movie']['genres'] or 'Horror' not in
            movie_watched['movie']['genres'] or 'Action' not in movie_watched['movie']['genres']):
        if user['gender'] == 'Female':
            if 15 <= int(user['age']) < 25:
                rating = random.randint(6, 10)
                return rating

            else:
                rating = random.randint(4, 10)
                return rating

        else:
            rating = rating = random.randint(1, 10)
            return rating

    if ('Romance' in movie_watched['movie']['genres'] or 'Comedy' in movie_watched['movie']['genres'] or 'Drama' in movie_watched['movie'][
        'genres'] or 'Thriller' in movie_watched['movie']['genres'] or 'Crime' in movie_watched['movie']['genres'] or 'Horror' in
            movie_watched['movie']['genres'] or 'Action' in movie_watched['movie']['genres']):
        if user['gender'] == 'Male':
            if 15 <= int(user['age']) < 35:
                rating = random.randint(5, 10)
                return rating

            else:
                rating = rating = random.randint(4, 10)
                return rating

        else:
            rating = rating = random.randint(1, 10)
            return rating

    else:
        rating = rating = random.randint(1, 10)
        return rating
