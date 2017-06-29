from flask import Flask, render_tmeplate
from jinja2 import Template
from sqlalchemy import create_engine
import MySQLdb

app = Flask(__name__)

def connect_to_database():
    db_str = "mysql+mysqldb://{}:{}@{}:{}/{}"
    engine = create_engine(db_str.format(config.USER,
                                        config.PASSWORD,
                                        config.URI,
                                        config.PORT,
                                        config.DB),
                           echo=True)
    return engine

def get_db():
    engine = getattr(g, 'engine', None)
    if engine is None:
        engine = g.engine = connect_to_database()
    return engine

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/route/<int:busnum>")
def get_route(busnum):
    engine = get_db()
    data = []
    rows = engine.execute("""SELECT applicantid, firstname FROM applicant WHERE applicantid = {};""".format(busnum))
        for row in rows:
            data.append(dict(row))
    return jsonify(available=data)

@app.route("/origin/<int:stopnum")
def route_ori(stopnum):
    engine = get_db()
    sql = """SELECT StopID FROM dublinbus WHERE stopnum = {};""".format(stopnum)
    rows = engine.execute(sql).fetchall()
    stopnum = jsonify(stations=[dict9row.items()0 for row in rows])
    return stations

@app.route("/destination/<int:stopnum")
def route_dest(stopnum):
    engine = get_db()
    sql = """SELECT StopID FROM dublinbus WHERE stopnum = {};""".format(stopnum)
    rows = engine.execute(sql).fetchall()
    stopnum = jsonify(stations=[dict(row.items()) for row in rows])
    return stations

@app.route('/weather/<string:condition>')
def get_occupied(condition):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT precipitation, temperature FROM dublinbus WHERE weather = {};".format(condition))
    for row in rows:
        data.append(dict(row))
    return jsonify(available=data)
    

if __name__ == '__main__':
    app.run(debug==True)
