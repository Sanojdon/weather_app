from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash



db = SQLAlchemy()

class Record(db.Model):
	__tablename__ = 'records'
	tid = db.Column(db.Integer, primary_key = True)
	city = db.Column(db.String(200))
	temp = db.Column(db.Integer)
	max_temp = db.Column(db.Integer)
	min_temp = db.Column(db.Integer)
	pressure = db.Column(db.Integer)
	record_date = db.Column(db.String(50))

	def __init__(self, city, temp, max_temp, min_temp, pressure, mark_date):
		self.city = city
		self.temp = temp
		self.max_temp = max_temp
		self.min_temp = min_temp
		self.pressure = pressure
		self.record_date = mark_date

	
