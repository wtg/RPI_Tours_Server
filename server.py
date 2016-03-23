import flask
import psycopg2
import psycopg2.extras

DB_URL = 'postgres://rpitours:rpitours@localhost:5432/rpitours'

app = flask.Flask(__name__)

def get_db():
	db = getattr(flask.g, 'database', None)
	if db is None:
		db = flask.g.database = psycopg2.connect(DB_URL)
	return db

def init_db():
	db = psycopg2.connect(DB_URL)
	cur = db.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS tour_categories (
			id serial PRIMARY KEY,
			name text NOT NULL,
			description text
		);
		CREATE TABLE IF NOT EXISTS tours (
			id serial PRIMARY KEY,
			tour json NOT NULL,
			category_id integer REFERENCES tour_categories NOT NULL
		);
		CREATE TABLE IF NOT EXISTS waypoints (
			id serial PRIMARY KEY,
			coordinate point NOT NULL,
			tour_id integer REFERENCES tours NOT NULL
		);
		CREATE TABLE IF NOT EXISTS landmarks (
			id serial PRIMARY KEY,
			name text NOT NULL,
			description text,
			coordinate point NOT NULL,
			tour_id integer REFERENCES tours NOT NULL
		);
	""")
	db.commit()

def make_tour():
	tour = {
		'name': 'Example Tour',
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

	db = get_db()
	cur = db.cursor()
	cur.execute("SELECT id, tour FROM tours")
	for row in cur.fetchall():
		tour = row[1]
		tour_id = row[0]
		tour['id'] = tour_id
		tour_lst.append(tour)

	return flask.jsonify(tours=tour_lst)

@app.route('/tours', methods=('POST',))
def tour_create():
	tour = make_tour()

	db = get_db()
	cur = db.cursor()
	cur.execute("INSERT INTO tours (tour) VALUES (%s) RETURNING id;", (psycopg2.extras.Json(tour),))
	row = cur.fetchone()
	tour_id = row[0]

	tour['id'] = tour_id

	# add tour ID to JSON in database
	cur.execute("UDPATE tours SET tour = %s WHERE id = %s;", (psycopg2.extras.Json(tour), tour_id))
	db.commit()

	return flask.jsonify(tour)

@app.route('/tours/<int:tour_id>', methods=('GET', 'PUT', 'DELETE'))
def tour(tour_id):
	db = get_db()
	cur = db.cursor()

	if flask.request.method == 'GET':
		cur.execute("SELECT tour FROM tours WHERE id = %s", (tour_id,))
		row = cur.fetchone()
		tour = row[0]

		return flask.jsonify(tour)

	if flask.request.method == 'PUT':
		tour = flask.request.get_json()
		if tour is not None:
			tour['id'] = tour_id
			cur.execute("UPDATE tours SET tour = %s WHERE id = %s", (psycopg2.extras.Json(tour), tour_id))
			db.commit()

			return flask.jsonify(tour)
		else:
			flask.abort(400)

	if flask.request.method == 'DELETE':
		cur.execute("DELETE FROM tours WHERE id = %s", (tour_id,))
		db.commit()

		return flask.jsonify(success=True)

@app.route('/dbtest')
def dbtest():
	get_db()
	return flask.jsonify(success=True)

if __name__ == '__main__':
	init_db()
	app.run(debug=True)
