import flask
import models
import admin

app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.jsonify(hello='world')

@app.route('/tours')
def tours():
	tour_lst = []
	return flask.jsonify(tours=tour_lst)

@app.route('/dbtest')
def dbtest():
	get_db()
	return flask.jsonify(success=True)

if __name__ == '__main__':
	admin.RPIToursAdmin(app)
	app.secret_key = 'fj24kfj23jds9ifdji'
	app.run(debug=True)
