import pandas as pd
import numpy as np

names = [
    "movie id | movie title | release date | video release date | IMDb URL | unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western | "]
names = [i.split(' | ') for i in names][0]
movie_data = pd.read_csv("resource/u.item", delimiter="|", encoding="437", names=names)
movie_data['video release date'] = movie_data['release date']
rating_data = pd.read_csv("resource/u.data", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])

rating_data = rating_data.rename(columns={'item id': 'movie id'})
movie_data = movie_data.drop('', axis=1)
# Merge Dataframes
full_data = movie_data.merge(rating_data, on='movie id', how="inner")
user_data = pd.read_csv("resource/u.user", delimiter="|", names=["user id", "age", "gender", "occupation", "zip code"])

# Observe NaN
# full_data[full_data.isnull().any(1)]

# drop record containing NaN
full_data = full_data.dropna(axis=0, subset=['release date']).reset_index().drop('index', axis=1)
full_data.head()

# Separate title with release year
full_data['release date'] = full_data['movie title'].str.split('(').str[1].str.replace(')', '')
full_data['movie title'] = full_data['movie title'].str.split('(').str[0]

full_data = full_data.drop('video release date', axis=1)
full_data = full_data.drop('IMDb URL', axis=1)

genres_titles = np.array(full_data.columns[3:22])
genres_titles

new_movie_profiles = pd.DataFrame(
    columns=['movie id', 'title', 'watch count', 'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
             'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
             'Sci-Fi', 'Thriller', 'War', 'Western'])

for i in range(1, 1683, 1):

    movie_rated_details_by_id = full_data.loc[full_data['movie id'] == i]
    movie_rated_details_by_id.reset_index(drop=True, inplace=True)
    no_of_times_rated = movie_rated_details_by_id.last_valid_index()

    if no_of_times_rated is not None:
        new_movie_profiles.loc[(i - 1), 'movie id'] = movie_rated_details_by_id.loc[0, 'movie id']

        new_movie_profiles.loc[(i - 1), 'title'] = movie_rated_details_by_id.loc[0, 'movie title']

        for j in range(0, no_of_times_rated, 1):
            current_watch_count = j + 1
            new_movie_profiles.loc[(i - 1), 'watch count'] = current_watch_count
            #         print(movie_rated_details_by_id.loc[j,'rating'])

            for genre in genres_titles:

                if pd.isnull(new_movie_profiles.loc[(i - 1), genre]):
                    new_movie_profiles.loc[(i - 1), genre] = 0

                #             print(new_movie_profiles.loc[(i-1), genre])
                current_overall_genre_score = new_movie_profiles.loc[(i - 1), genre] * (current_watch_count - 1)
                current_genre_score = (
                        movie_rated_details_by_id.loc[j, 'rating'] * (movie_rated_details_by_id.loc[j, genre]))
                new_movie_profiles.loc[(i - 1), genre] = (
                                                                 current_genre_score + current_overall_genre_score) / current_watch_count
    #             print(new_movie_profiles.loc[(i-1), genre])
    print(i)

# print(new_movie_profiles)
new_movie_profiles.fillna(0, inplace=True)
new_movie_profiles.to_csv('new_movie_profiles.csv', index=False)
