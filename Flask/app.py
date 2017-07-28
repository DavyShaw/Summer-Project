from flask import Flask, render_template, g, jsonify, request
import config
from sqlalchemy import create_engine
import MySQLdb
import json
import pandas as pd
import sklearn
import pickle
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn import model_selection
from sklearn.model_selection import train_test_split
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

#@app.route("/routes", methods=['GET','POST'])
#def routes():
#    chosenroute = request.form.get('chosenroute')
#    chosenorigin = request.form.get('chosenorigin')
#    chosendestination = request.form.get('chosendestination')
#    chosenday = request.form.get('chosenday')
#    chosentime = request.form.get('chosentime')
#    chosenweather = request.form.get('chosenweather')
#    
##    with open('static/dublinbus_routes.json') as data_file:    
##        json_file_routes = json.load(data_file)
#        
#    with open('static/routes.json') as data_file:
#        json_routes = json.load(data_file)
#        
#    with open('static/all_stops_and_routesDB.json') as data_file:
#        json_file_stops = json.load(data_file)
#    
#    return render_template("display.html", json_file_stops = json_file_stops, json_routes = json_routes, chosenroute = chosenroute)


@app.route("/routes", methods=['GET','POST'])
def routes():
#    list=[]
    chosenroute = request.form.get('chosenroute')
#    newroute=re.findall(r'[+-]?\d+', chosenroute)
#    chosenroute.split(':')
#    list.append(chosenroute)
    chosenorigin = request.form.get('chosenorigin')
#    neworigin=re.findall(r'[+-]?\d+', chosenorigin)
#    list.append(chosenorigin)
    chosendestination = request.form.get('chosendestination')
#    newdest=re.findall(r'[+-]?\d+', chosendestination)
#    list.append(chosendestination)
    chosenday = request.form.get('chosenday')
#    newday=re.findall(r'[+-]?\d+', chosenday)
#    list.append(chosenday)
    chosentime = request.form.get('chosentime')
#    list.append(chosentime)
    chosentemp = request.form.get('chosentemp')
    chosenhumid = request.form.get('chosenhumid')
    chosenpres = request.form.get('chosenpres')
#    newweather=re.findall(r'[+-]?\d+', chosenweather)
#    list.append(chosenweather)
    string = (chosenroute +" "+ chosenorigin +" "+ chosendestination +" "+ chosenday +" "+ chosentime +" "+ chosentemp + chosenhumid+chosenpres)
    newstring=re.findall(r'[+-]?\d+', string)
    list=[]
    chosenroute = float(newstring[0])
    list.append(chosenroute)
    chosenorigin = float(newstring[1])
    list.append(chosenorigin)
    chosendestination = float(newstring[2])
    list.append(chosendestination)
    chosenday = float(newstring[3])
    list.append(chosenday)
    chosentime = float(newstring[4])
    list.append(chosentime)
    chosentemp = float(newstring[5])
    list.append(chosentemp)
    chosenhumid = float(newstring[6])
    list.append(chosenhumid)
    chosenpres = float(newstring[7])
    list.append(chosenpres)
#    list.append(0)
    dataframe = pd.read_csv('cleangps.csv')
    array = dataframe.values
    X = array[:,0:8]
    Y = array[:,8]
    test_size = 0.33
    seed = 7
    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)
    # Fit the model on 33%
    model = RandomForestRegressor()  
    model.fit(X_train, Y_train)
    # save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(list)
    
    with open('static/routes.json') as data_file:
        json_file_routes = json.load(data_file)
        
    with open('static/routes.json') as data_file:
        json_routes = json.load(data_file)
        
    with open('static/routes_and_stops.json') as data_file:
        json_file_stops = json.load(data_file)
    
    return render_template("display.html", json_file_routes = json_file_routes, json_file_stops = json_file_stops, json_routes = json_routes, chosenroute = chosenroute)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        


if __name__ == "__main__":
    app.run(debug=True)
