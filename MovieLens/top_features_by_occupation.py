import pandas as pd
import numpy as np

user_data = pd.read_csv("new_user_profiles.csv")

occupation_feature_total = pd.DataFrame(
    columns=['occupation', 'unknown count', 'Action count', 'Adventure count',
             'Animation count', "Children's count", 'Comedy count', 'Crime count', 'Documentary count', 'Drama count',
             'Fantasy count', 'Film-Noir count', 'Horror count', 'Musical count', 'Mystery count', 'Romance count',
             'Sci-Fi count', 'Thriller count', 'War count', 'Western count'])

occupation_list = user_data.occupation.unique()
genre_list = np.array(user_data.columns[4:23])

for index, occupation in enumerate(occupation_list):

    users_by_occupation = user_data.loc[user_data['occupation'] == occupation]
    users_by_occupation.reset_index(drop=True, inplace=True)
    #     print(user_rated_details_by_id)
    no_of_watches = users_by_occupation.last_valid_index()
    occupation_feature_total.loc[index, 'occupation'] = occupation

    for genre in genre_list:
        total = users_by_occupation[genre+" count"].sum()
        occupation_feature_total.loc[index, genre+" count"] = total

print(occupation_feature_total)
occupation_feature_total.to_csv('occupation_feature_total.csv', index=False)

occupation_wise_totals = pd.read_csv("occupation_feature_total.csv")
print(occupation_wise_totals.head())
