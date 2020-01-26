import pandas as pd
import numpy as np

names = [
    "movie id | movie title | release date | video release date | IMDb URL | unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western | "]
names = [i.split(' | ') for i in names][0]
movie_data = pd.read_csv("../resource/u.item", delimiter="|", encoding="437", names=names)
movie_data['video release date'] = movie_data['release date']
rating_data = pd.read_csv("../resource/u1.base", delimiter="\t", names=["user id", "item id", "rating", "timestamp"])

rating_data = rating_data.rename(columns={'item id': 'movie id'})
movie_data = movie_data.drop('', axis=1)
# Merge Dataframes
full_data = movie_data.merge(rating_data, on='movie id', how="inner")
user_data = pd.read_csv("../resource/u.user", delimiter="|", names=["user id", "age", "gender", "occupation", "zip code"])

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

# calculate each genre score
genres_titles = np.array(full_data.columns[3:22])

new_user_profiles = pd.DataFrame(
    columns=['user id', 'gender', 'age', 'occupation', 'unknown', 'Action', 'Adventure', 'Animation', "Children's",
             'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
             'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'unknown count', 'Action count', 'Adventure count',
             'Animation count', "Children's count", 'Comedy count', 'Crime count', 'Documentary count', 'Drama count',
             'Fantasy count', 'Film-Noir count', 'Horror count', 'Musical count', 'Mystery count', 'Romance count',
             'Sci-Fi count', 'Thriller count', 'War count', 'Western count'])

for i in range(1, 944, 1):

    user_rated_details_by_id = full_data.loc[full_data['user id'] == i]
    user_rated_details_by_id.reset_index(drop=True, inplace=True)
    #     print(user_rated_details_by_id)
    no_of_times_rated = user_rated_details_by_id.last_valid_index()
    print(no_of_times_rated)

    if no_of_times_rated is not None:

        new_user_profiles.loc[(i - 1), 'user id'] = user_rated_details_by_id.loc[0, 'user id']
        #         get user details from user_data
        current_user_details = user_data.loc[user_data['user id'] == i]
        current_user_details.reset_index(drop=True, inplace=True)
        #         print(current_user_details)
        new_user_profiles.loc[(i - 1), 'gender'] = current_user_details.loc[0, 'gender']
        new_user_profiles.loc[(i - 1), 'age'] = current_user_details.loc[0, 'age']
        new_user_profiles.loc[(i - 1), 'occupation'] = current_user_details.loc[0, 'occupation']

        for j in range(0, no_of_times_rated, 1):
            #             current_watch_count = j+1
            #             new_user_profiles.loc[(i-1), 'watch count'] = current_watch_count
            #         print(movie_rated_details_by_id.loc[j,'rating'])

            for genre in genres_titles:

                if pd.isnull(new_user_profiles.loc[(i - 1), (genre + ' count')]):
                    new_user_profiles.loc[(i - 1), (genre + ' count')] = 0

                if pd.isnull(new_user_profiles.loc[(i - 1), genre]):
                    new_user_profiles.loc[(i - 1), genre] = 0

                current_watch_count = new_user_profiles.loc[(i - 1), (genre + ' count')] + 1

                #             print(new_movie_profiles.loc[(i-1), genre])
                current_overall_genre_score = new_user_profiles.loc[(i - 1), genre] * (current_watch_count - 1)
                current_genre_score = (user_rated_details_by_id.loc[j, 'rating'] * user_rated_details_by_id.loc[j, genre])
                #                 print(current_genre_score)
                if current_genre_score > 0:
                    new_user_profiles.loc[(i - 1), genre] = (current_genre_score + current_overall_genre_score) / current_watch_count
                    new_user_profiles.loc[(i - 1), (genre + ' count')] += 1
    #                 print('current:'+str(new_movie_profiles.loc[(i-1), genre]))
    print(i)

# print(new_user_profiles)
new_user_profiles.to_csv('user_feature_profiles.csv', index=False)
