import flask
import psycopg2

DB_URL = 'postgres://rpitours:rpitours@localhost:5432/rpitours'

app = flask.Flask(__name__)

def get_db():
	db = getattr(flask.g, 'database', None)
	if db is None:
		db = flask.g.database = psycopg2.connect(DB_URL)
	return db

def make_tour():
	tour = {
		'id': 1,
		'name': 'Test Tour',
		'waypoints': [
			(5, 2),
			(2, 3),
			(1, 4),
			(4, 4)
		],
		'landmarks': [
			{
				'name': 'A Place',
				'description': 'This is a description of this place.',
				'photos': ['https://example.com/photo1.jpg', 'https://example.com/photo2.jpg'],
				'coordinate': (3, 4),
			}, {
				'coordinate': (2, 3),
			}, {
				'coordinate': (4, 1)
			}
		]
	}
	return tour

@app.route('/')
def index():
	return flask.jsonify(hello='world')

@app.route('/tours')
def tours():
	tour_lst = [make_tour()]
	return flask.jsonify(tours=tour_lst)

@app.route('/dbtest')
def dbtest():
	get_db()
	return flask.jsonify(success=True)

if __name__ == '__main__':
	app.run(debug=True)
