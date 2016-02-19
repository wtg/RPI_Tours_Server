import flask
import psycopg2

app = flask.Flask(__name__)
db = psycopg2.connect('postgres://rpitours:rpitours@localhost:5432/rpitours')

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

if __name__ == '__main__':
	app.run(debug=True)
