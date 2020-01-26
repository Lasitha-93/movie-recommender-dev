import pandas as pd
import json
from support_functions import getage, getfeaturerating

metadata = pd.read_csv('resources/1000users.csv', low_memory=False)

users = {'users': []}
# birthdays = metadata['birthday']
for i in range(0, 1000):

    current_user_model = {'user': {'name': None, 'gender': None, 'age': None, 'features': {'plot': None, 'actors': None, 'theme': None, 'rating': None, 'music': None, 'trailer': None, 'language': None, 'popularity': None, 'awards': None, 'action': None, 'romance': None, 'comedy': None, 'thriller': None, 'drama': None}}}

    # metadata.loc[i, 'birthday'] = getage()
    # metadata.loc[i, 'plot'] = getfeaturerating()
    # metadata.loc[i, 'actors'] = getfeaturerating()
    # metadata.loc[i, 'theme'] = getfeaturerating()
    # metadata.loc[i, 'rating'] = getfeaturerating()
    # metadata.loc[i, 'music'] = getfeaturerating()
    # metadata.loc[i, 'trailer'] = getfeaturerating()
    # metadata.loc[i, 'language'] = getfeaturerating()
    # metadata.loc[i, 'popularity'] = getfeaturerating()
    # metadata.loc[i, 'awards'] = getfeaturerating()
    # metadata.loc[i, 'action'] = getfeaturerating()
    # metadata.loc[i, 'romance'] = getfeaturerating()
    # metadata.loc[i, 'comedy'] = getfeaturerating()
    # metadata.loc[i, 'thriller'] = getfeaturerating()
    # metadata.loc[i, 'drama'] = getfeaturerating()

    current_user_model['user']['name'] = metadata.loc[i, 'name']
    current_user_model['user']['gender'] = metadata.loc[i, 'gender']
    current_user_model['user']['age'] = getage()
    current_user_model['user']['features']['plot'] = getfeaturerating()
    current_user_model['user']['features']['actors'] = getfeaturerating()
    current_user_model['user']['features']['theme'] = getfeaturerating()
    current_user_model['user']['features']['rating'] = getfeaturerating()
    current_user_model['user']['features']['music'] = getfeaturerating()
    current_user_model['user']['features']['trailer'] = getfeaturerating()
    current_user_model['user']['features']['language'] = getfeaturerating()
    current_user_model['user']['features']['popularity'] = getfeaturerating()
    current_user_model['user']['features']['awards'] = getfeaturerating()
    current_user_model['user']['features']['action'] = getfeaturerating()
    current_user_model['user']['features']['romance'] = getfeaturerating()
    current_user_model['user']['features']['comedy'] = getfeaturerating()
    current_user_model['user']['features']['thriller'] = getfeaturerating()
    current_user_model['user']['features']['drama'] = getfeaturerating()

    users['users'].append(current_user_model)

# metadata.rename(columns={'birthday': 'age'}, inplace=True)
# print(metadata.head(1001))

# metadata.to_csv('1000users_with_ratings', index_lable=False)

with open('1000users_with_ratings.json', 'w') as f2:
    # indented_data=json.dumps(movies, indent=2)
    json.dump(users, f2)

with open('1000users_with_ratings.json') as file:
    new_data = json.load(file)
    indented_data=json.dumps(new_data, indent=2)
    # movies = new_data['movies']
    print(indented_data)





