import flask

app = flask.Flask(__name__)

def make_tour():
	tour = {
		'id': 1,
		'name': 'Test Tour',
		'route': [
			{
				'description': 'This is a description of this place.',
				'photos': ['photo1.jpg', 'photo2.jpg'],
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
