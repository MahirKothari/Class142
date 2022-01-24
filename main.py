import csv
from flask import Flask , jsonify , request
from storage import all_movies,liked_movies,not_liked_movies,did_not_watch
from Demographicfiltering import output
from Contentfilteriing import getRecommendations
app = Flask(__name__)
@app.route('/get-movie')
def getMovie():
    movie_data = {
        'title' : all_movies[0][19],
        'poster_link' : all_movies[0][27],
        'release_date' : all_movies[0][13] or 'n/a',
        'duration' : all_movies[0][15],
        'rating' : all_movies[0][20],
        'overview' : all_movies[0][9]
        }
    return jsonify({
        'data': movie_data,
        'status':'success'
    })
@app.route('/liked-movies',methods = ['POST'])
def liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        'status':'success'
    }),201
@app.route('/unliked-movie',methods = ['POST'])
def not_liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_liked_movies.append(movie)
    return jsonify({
        'status':'success'
    }),201
@app.route('/did-not-watch',methods = ['POST'])
def did_not_watch():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    did_not_watch.append(movie)
    return jsonify({
        'status':'success'
    }),201
@app.route('/popular-movies')
def popular_movies():
    movie_data = []
    for movie in output:
        d = {
            'title' : movie[0],
            'poster_link' : movie[1],
            'release_date' : movie[2] or 'n/a',
            'duration' : movie[3],
            'rating' : movie[4],
            'overview' : movie[5]
        }
        movie_data.append(d)
    return jsonify({
        'data': movie_data,
        'status':'success'
    })
@app.route('/recommended-movies')
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = getRecommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended in itertools.groupby(all_recommended))
    movie_data = []
    for movie in all_recommended:
        d = {
            'title' : movie[0],
            'poster_link' : movie[1],
            'release_date' : movie[2] or 'n/a',
            'duration' : movie[3],
            'rating' : movie[4],
            'overview' : movie[5]
        }
        movie_data.append(d)
    return jsonify({
        'data': movie_data,
        'status':'success'
    })
if __name__ == '__main__':
    app.run()