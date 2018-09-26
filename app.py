from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


# Define /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base() # reflect an existing database into a new model
    Base.prepare(engine, reflect=True) # reflect the tables
    Measurement = Base.classes.measurement # Save reference to tables
    session = Session(engine) # Create session (link) from Python to the DB

    # Determine dates from 1 year ago
    today_str = session.query(func.max(Measurement.date)).first()[0]
    today = dt.datetime.strptime(today_str, '%Y-%m-%d').date()
    today_1y = today - dt.timedelta(days=365.25)

    # Query for precipitation for dates
    prec = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > today_1y).filter(Measurement.date <= today)

    # Convert to dataframe
    prec_df = pd.read_sql(prec.statement, session.bind, index_col = 'date')

    # Convert dataframe to dictionary
    prec_dict = prec_df.to_dict()

    return jsonify(prec_dict)


# Define /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base() # reflect an existing database into a new model
    Base.prepare(engine, reflect=True) # reflect the tables
    Station = Base.classes.station # Save reference to tables
    session = Session(engine) # Create session (link) from Python to the DB

    # Query station table
    stat = session.query(Station.station).all()

    # Convert tuple to list
    stat_list = list(np.ravel(stat))

    return jsonify(stat_list)


# Define /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base() # reflect an existing database into a new model
    Base.prepare(engine, reflect=True) # reflect the tables
    Measurement = Base.classes.measurement # Save reference to tables
    session = Session(engine) # Create session (link) from Python to the DB

    # Determine dates from 1 year ago
    today_str = session.query(func.max(Measurement.date)).first()[0]
    today = dt.datetime.strptime(today_str, '%Y-%m-%d').date()
    today_1y = today - dt.timedelta(days=365.25)

    # Query for tobs for dates
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > today_1y).filter(Measurement.date <= today)

    # Convert to dataframe
    tobs_df = pd.read_sql(tobs.statement, session.bind, index_col = 'date')

    # Convert dataframe to dictionary
    tobs_dict = tobs_df.to_dict()

    return jsonify(tobs_dict)


# Define /api/v1.0/<start> route
@app.route("/api/v1.0/<start>")
def start(start):

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base() # reflect an existing database into a new model
    Base.prepare(engine, reflect=True) # reflect the tables
    Measurement = Base.classes.measurement # Save reference to tables
    session = Session(engine) # Create session (link) from Python to the DB

    # Determine dates from 1 year ago
    today_str = session.query(func.max(Measurement.date)).first()[0]
    today = dt.datetime.strptime(today_str, '%Y-%m-%d').date()
    today_1y = today - dt.timedelta(days=365.25)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = today

    stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    stats_df = pd.read_sql(stats.statement, session.bind)

    stats_dict = stats_df.to_dict(orient='records')

    return jsonify(stats_dict)


# Define /api/v1.0/<start>/<end>  route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base() # reflect an existing database into a new model
    Base.prepare(engine, reflect=True) # reflect the tables
    Measurement = Base.classes.measurement # Save reference to tables
    session = Session(engine) # Create session (link) from Python to the DB

    # Determine dates from 1 year ago
    today_str = session.query(func.max(Measurement.date)).first()[0]
    today = dt.datetime.strptime(today_str, '%Y-%m-%d').date()
    today_1y = today - dt.timedelta(days=365.25)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()

    stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    stats_df = pd.read_sql(stats.statement, session.bind)

    stats_dict = stats_df.to_dict(orient='records')

    return jsonify(stats_dict)

if __name__ == '__main__':
    app.run(debug=True)
