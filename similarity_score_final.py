from user_based_similarity_features import user_similarity_by_features
from user_based_similarity_movie import user_similarity_by_watchlist


def get_final_sim_score(person):

    scores_by_features = user_similarity_by_features(person)
    scores_by_watchlist = user_similarity_by_watchlist(person)

    # print(scores_by_watchlist[0:5])
    # print(scores_by_features[0:5])
    final_similarity = []

    for user_in_feature in scores_by_features:

        for user_in_watchlist in scores_by_watchlist:

            if user_in_feature['user']['name'] == user_in_watchlist['user']['name']:

                final_similarity.append(((user_in_feature['user']['score']*user_in_watchlist['user']['score']), user_in_feature['user']['name']))

            else:
                continue
    final_similarity.sort()
    final_similarity.reverse()

    return final_similarity

print(get_final_sim_score('Harvey Glover')[0:5])
