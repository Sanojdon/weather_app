from flask import Flask, render_template, request
import requests
import json
from models import db, Record
from datetime import datetime, timedelta
import sys

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temp_records.db"
db.init_app(app)

key = '052745e6bb184286a6102fcc2ca59f52'

def result(addr, dfro=None, dend=None):
	if dfro is None and dend is None:
		dfro = datetime.now().strftime("%Y-%m-%d")
		dend = (datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
	query = "https://api.weatherbit.io/v2.0/history/daily?city="+addr+"&start_date="+dfro+"&end_date="+dend+"&key="+key
	try:
		r = requests.get(query)
		data = json.loads(r.text)
		fin = data['data'][0]
		fin['city'] = data['city_name']
		return fin
	except:
		return "Connection Failure.."


@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == 'GET':
		place = request.args.get('place')
		dfro = request.args.get('date_start')
		dend = request.args.get('date_end')
		if place is not None:
			r = result(place)
			if(dfro is not '' and dend is not ''):
				r = result(place,dfro,dend)

			context = dict()
			context['city'] = r['city']
			context['temp'] = r['temp']
			context['max_temp'] = r['max_temp']
			context['min_temp'] = r['min_temp']
			context['pressure'] = r['pres']

			if request.args.get('btnSave') is not None:
				if dend == '':
					dend = None
				record = Record(context['city'], context['temp'], context['max_temp'], context['min_temp'], context['pressure'], dend)
				db.session.add(record)
				db.session.commit()
			return render_template('/result.html', context=context)
	return render_template('/index.html')

@app.route('/saved')
def saved():
	records = Record.query.all()
	return render_template('/saved.html', records=records)

if __name__ == '__main__':
	app.run()