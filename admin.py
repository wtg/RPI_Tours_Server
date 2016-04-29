from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

import models

class TourAdmin(ModelView):
	inline_models = (models.Landmark, models.Waypoint)

	pass

class RPIToursAdmin():
	def __init__(self, app):
		admin = Admin(app, name='RPI Tours')
		admin.add_view(TourAdmin(models.Tour, name='Tours'))
		admin.add_view(ModelView(models.TourCategory, name='Tour Categories'))
