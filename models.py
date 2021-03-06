import peewee
from playhouse import shortcuts

DB_INFO = {
	'db': 'rpitours',
	'user': 'rpitours',
	'password': 'rpitours',
	'host': 'localhost',
	'port': '5432'
}

db = peewee.PostgresqlDatabase(
	DB_INFO['db'],
	user=DB_INFO['user'],
	password=DB_INFO['password'],
	host=DB_INFO['host'],
	port=DB_INFO['port']
)

class BaseModel(peewee.Model):
	class Meta:
		database = db

class TourCategory(BaseModel):
	name = peewee.TextField()
	description = peewee.TextField()

	def __str__(self):
		return self.name

class Tour(BaseModel):
	name = peewee.TextField()
	category = peewee.ForeignKeyField(TourCategory, related_name='tours')

class Waypoint(BaseModel):
	latitude = peewee.FloatField()
	longitude = peewee.FloatField()
	tour = peewee.ForeignKeyField(Tour, related_name='waypoints')

class Landmark(BaseModel):
	name = peewee.TextField()
	description = peewee.TextField()
	latitude = peewee.FloatField()
	longitude = peewee.FloatField()
	tour = peewee.ForeignKeyField(Tour, related_name='landmarks')

def get_all_tours():
	tours = []
	for tour in Tour.select():
		tours.append(shortcuts.model_to_dict(tour, backrefs=True))
	return tours

db.connect()
db.create_tables([TourCategory, Tour, Waypoint, Landmark], safe=True)
