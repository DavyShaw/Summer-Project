from flask import Flask, render_template, g, jsonify, request
import config
from sqlalchemy import create_engine
import MySQLdb
import json
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

@app.route("/")
def main():
    with open('static/dublinbus_routes.json') as data_file:    
        json_file_routes = json.load(data_file)
        
    with open('static/routes.json') as data_file:
        json_routes = json.load(data_file)
        
    with open('static/all_stops_and_routesDB.json') as data_file:
        json_file_stops = json.load(data_file)
    
    return render_template("index.html", json_file_routes = json_file_routes, json_file_stops = json_file_stops, json_routes = json_routes)

@app.route("/routes", methods=['GET','POST'])
def routes():
    chosenroute = request.form.get('chosenroute')
    chosenorigin = request.form.get('chosenorigin')
    chosendestination = request.form.get('chosendestination')
    chosenday = request.form.get('chosenday')
    chosentime = request.form.get('chosentime')
    chosenweather = request.form.get('chosenweather')
    
    with open('static/dublinbus_routes.json') as data_file:    
        json_file_routes = json.load(data_file)
        
    with open('static/routes.json') as data_file:
        json_routes = json.load(data_file)
        
    with open('static/all_stops_and_routesDB.json') as data_file:
        json_file_stops = json.load(data_file)
    
    return render_template("display.html", json_file_routes = json_file_routes, json_file_stops = json_file_stops, json_routes = json_routes, chosenroute = chosenroute)

#    return(str(chosenroute +" "+ chosenorigin+" "+ chosendestination+" "+ chosenday+" "+ chosentime+" "+ chosenweather)) 
#    return render_template("index.html")

#@app.route("/routes", methods=['GET','POST'])
#def routes():
#    chosenroute = request.form.get('chosenroute')
#    chosenorigin = request.form.get('chosenorigin')
#    chosendestination = request.form.get('chosendestination')
#    chosenday = request.form.get('chosenday')
#    chosentime = request.form.get('chosentime')
#    chosenweather = request.form.get('chosenweather')
#
#    return render_template('index.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        


if __name__ == "__main__":
    app.run(debug=True)
