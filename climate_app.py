# # Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

import datetime as dt

from datetime import datetime as dt, timedelta

import numpy as np
import pandas as pd

engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)

# Create our session (link) from Python to the DB
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement 
Station = Base.classes.station 

session = Session(engine)

hello_dict = {"Hello": "World!"}

@app.route("/")
def welcome():
    return (
        f"Welcome to the  API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api.v1.0/precipitation")
def precipitation():
# Design a query to retrieve the last 12 months of precipitation data and plot the results



    min_dt = engine.execute('SELECT min(date) Min_dt  FROM measurement LIMIT 10').fetchall()
    max_dt = engine.execute('SELECT max(date) Max_dt  FROM measurement LIMIT 10').fetchall()
    max_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    d = dt.strptime(max_dt,"%Y-%m-%d")

    # Calculate the date 1 year ago from the last data point in the database
    year_ago = d - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date  >= year_ago).all()

    # Save the query results as a Pandas DataFrame and set the index to the date column
    df = pd.DataFrame(data, columns=['date', 'prcp'])
    prcp_data_dict= df.to_dict(orient='records')

    return jsonify(prcp_data_dict)


@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)



if __name__ == "__main__":
    app.run(debug=True)






