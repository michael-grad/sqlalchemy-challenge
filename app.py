# SQLalchemy homework
# import dependencies
from flask import Flask, jsonify

#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# - Declare a Base using `automap_base()`
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




app = Flask(__name__)

# Create Routes
# VERIFIED AS WORKING
@app.route("/")
def home():
    print("Home Page")
    home_page = {'Home': '/', 'Precipitation': "/api/v1.0/precipitation", 'Stations': '/api/v1.0/stations', 'TOBS': '/api/v1.0/tobs', \
        'Start Date': '/api/v1.0/<start>', 'Start and End Date': '/api/v1.0/<start>/<end>'}
    # DEBUG!! -- lines with <br/> do not print on separate rows
    # DEBUG!! -- home_page printed on webpage in alphabetical order instead of sequenced as is
    return jsonify(home_page
        #f"Available Routes:<br/>"
        #f"/<br/>"
        #f"/api/v1.0/precipitation<br/>"
        #f"/api/v1.0/stations<br/>"
        #f"/api/v1.0/tobs<br/>"
        #f"/api/v1.0/<start><br/>"
        #f"/api/v1.0/<start>/<end>"
    )

# VERIFIED AS WORKING
@app.route("/api/v1.0/precipitation")
def prcp():

    prcp_score = session.query(Measurement.prcp, \
                           Measurement.date\
                          ).order_by(Measurement.date).all()
    print("Precipitation")
    # DEBUG!!:  How to convert to a dictionary?
    prcp_dict = {}
    for element in prcp_score:
        key = element[1]
        value = element[0]
        # update dictionary sourced from https://thispointer.com/python-how-to-add-append-key-value-pairs-in-dictionary-using-dict-update/
        prcp_dict.update({key: value})

    prcp = {'date':  'prcp value'}
    return jsonify(prcp_dict)

# VERIFIED AS WORKING
# DEBUG!! - SOMETIMES IT WORKS AND SOMETIMES IT DOESN'T
@app.route("/api/v1.0/stations")
def stations():
    print("Stations")
    station_name_id = session.query(Station.id, Station.name).group_by(Station.name).order_by(Station.id).all()
    station_dict = {}
    for element in station_name_id:
        key = element[0]
        value = element[1]
        # update dictionary
        station_dict.update({key: value})
    return jsonify(station_dict)

# VERIFIED AS WORKING
@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most active station for the last year of data
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    print("Tobs")

    most_frequent_last_12 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()
    tobs_dict = {}
    for element in most_frequent_last_12:
        key = element[0]
        value = element[1]

        # update dictionary
        tobs_dict.update({key: value})
    return jsonify(tobs_dict)
    
# DEBUG!! -- NEED TO DO after ipynb is fixed
# DEBUG!! -- change .id=1 to most frequent station
# DEBUG!! -- 
# -- .all produces n(0n for each value in record[0], record[1], record[2], record[3] and also only produces 1 record
# -- .first produces eNno for each value in record[0], record[1], record[2], record[3] and also only produces 1 record
# -- .first previously produced 87.2 for each value in record[0], record[1], record[2], record[3] and also only produces 1 record
@app.route("/api/v1.0/<start>")
def start(start):
    print(f"{start}")
    # most_freq_tobs_dict = {}
    station_3_obs = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).first()

    # Create a list of dictionaries where each dictionary contains tobs data for a single date
    # DEBUG!! type error:  "TypeError: 'float' object is not subscriptable"
    # Per stack overflow solution is to convert float object to a string
    # Another stack overflow solution is to assign dictionary values instead of using append
    # sourced from https://stackoverflow.com/questions/27453396/typeerror-float-object-is-not-subscriptable-while-saving-a-dict
    from_start_date_only = []
    start_dict = {}
    for record in station_3_obs:
        start_dict['Date'] = str(record)[0]
        start_dict['Min'] = str(record)[1]
        start_dict['Max'] = str(record)[2]
        start_dict['Avg'] = str(record)[3]
        from_start_date_only.append(start_dict)
        # above code returns 87.2 for only 1 record

#    most_frequent_last_12 = session.query(Measurement.date, Measurement.tobs).\
#        filter(Measurement.date >= start).all()
#    for element in station_3_obs:
#        key = element[0]
#        value = element[1]
        # update dictionary
#        most_freq_tobs_dict.update({key: value})
    return jsonify(start_dict)

# DEBUG!! -- 
@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    # return temp_list for range
    example_temp_list = {'min': 53, 'avg': 67, 'max': 83}
    station_start_and_end_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).filer(Measurement.date <= end).all()

    from_start_date_end_date = []
    start_and_end_dict = {}
    for record in station_start_and_end_dates:
        start_and_end_dict['Date'] = str(record)[0]
        start_and_end_dict['Min'] = str(record)[1]
        start_and_end_dict['Max'] = str(record)[2]
        start_and_end_dict['Avg'] = str(record)[3]
        from_start_date_only.append(start_and_end_dict)
    return jsonify(start_date_end_date)


if __name__ == "__main__":
    app.run(debug=True)