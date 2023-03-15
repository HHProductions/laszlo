import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/database3.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.total_emission
Station = Base.classes.total_emission

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/stations<br/>"
    )
    
##############

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation detail"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    # Create a dictionary from the row data and append to a list of precipitation data
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    # Convert list of tuples into normal list
   # all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

##############

@app.route("/api/v1.0/stations")
def station_name():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list stations"""
    # Query all stations
    results = session.query(Station.Country, Station.longitude).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["2000"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
