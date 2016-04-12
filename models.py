import peewee

DB_URL = 'postgres://rpitours:rpitours@localhost:5432/rpitours'

database = peewee.PostgresqlDatabase(DB_URL)

class BaseModel(peewee.Model):
	class Meta:
		database = database

class TourCategory(BaseModel):
	name = peewee.TextField()
	description = peewee.TextField()

class Tour(BaseModel):
	name = peewee.TextField()
	category = peewee.ForeignKeyField(TourCategory)

	def json(self):
		return

class Waypoint(BaseModel):
	latitude = peewee.FloatField()
	longitude = peewee.FloatField()
	tour = peewee.ForeignKeyField(Tour)

class Landmark(BaseModel):
	name = peewee.TextField()
	description = peewee.TextField()
	latitude = peewee.FloatField()
	longitude = peewee.FloatField()
	tour = peewee.ForeignKeyField(Tour)
