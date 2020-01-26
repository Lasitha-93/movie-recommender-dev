from flask import Flask, render_template, request, jsonify
from FlaskApp.src.SparqlQueries import runQuery


app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/byMovieTypeSearch', methods=['POST'])
def byMatSearch():
    return jsonify(runQuery.searchByMovieType(request.form['material']))

@app.route('/byGETMaterialSearch', methods=['GET'])
def byMatSearchGet():
    return jsonify(runQuery.searchByMovieType('ActionMovie'))

@app.route('/byFeatureSearch', methods=['POST'])
def byFeatureSetSearch():
    language = request.form['language']
    genre = request.form['genre']
    actor = request.form['actor']
    country = request.form['country']
    director = request.form['director']
    if (country == '' and actor == '' and director  == '' ):
        return jsonify(runQuery.searchByLangGen(language, genre))
    elif (actor == '' and director == ''):
        return jsonify(runQuery.searchByLGC(language, genre, country))
    elif(actor == '' and country == ''):
        return jsonify(runQuery.searchByLGD(language, genre, director))
    elif (director == '' and country == ''):
        return jsonify(runQuery.searchByLGA(language, genre, actor))
    elif (actor == ''):
        return jsonify(runQuery.searchByLGCD(language, genre, country, director))
    elif (director == ''):
        return jsonify(runQuery.searchByLGCA(language, genre, country, actor))
    elif (country == ''):
        return jsonify(runQuery.searchByLGAD(language, genre, actor, director))
    else:
        return jsonify(runQuery.searchByFeatureSet(language, genre, country, actor, director))

@app.route('/byMoviePrcofileSearch', methods=['POST'])
def byMovieProfileSearch():
    return jsonify(runQuery.getMovieProfiles())

@app.route('/byUserProfileSearch', methods=['POST'])
def byUserProfileSearch():
    return jsonify(runQuery.getUserProfiles())

@app.route('/byMovieProfileByIdSearch', methods=['POST'])
def byMovieProfileIdSearch():
    return jsonify(runQuery.getMovieProfileByMovieId(request.form['movie_id']))

@app.route('/byUserProfileByIdSearch', methods=['POST'])
def byUserProfileIdSearch():
    return jsonify(runQuery.getUserProfileByUserId(request.form['user_id']))

@app.route('/byMoodSearch', methods=['POST'])
def byMyMoodSearch():
    return jsonify(runQuery.searchByMood(request.form['user_id'], request.form['mood']))


app.run()