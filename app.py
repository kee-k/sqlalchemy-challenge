# import dependencies
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# ------------------------
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# ------------------------
# Flask Setup
app = Flask(__name__)


# ------------------------
# Flask Routes
@app.route("/")
def home():
    # """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-10-01<br/>"
        f"/api/v1.0/2016-10-01/2016-10-07<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12_mos_prcp = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date).all()

    session.close()
   
    precipitation = []
    for date,prcp in last_12_mos_prcp:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    
    stations1 = session.query(Station.station,Station.name).all()

    session.close()

    stations = list(np.ravel(stations1))
    
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12_mos_temp = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= date).all()

    session.close()

    most_active_tobs = list(np.ravel(last_12_mos_temp))
    
    return jsonify(most_active_tobs)


@app.route("/api/v1.0/2016-10-01")
def vacay_start():
    session = Session(engine)

    date = dt.date(2016,10,1)

    vacay_start_only = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= date).all()

    session.close()

    vacay_start_only1 = list(np.ravel(vacay_start_only))

    return jsonify(vacay_start_only1)


@app.route("/api/v1.0/2016-10-01/2016-10-07")
def vacay():
    session = Session(engine)

    daterange = pd.date_range(start='1/10/2016',end='7/10/2016')

    # vacay_start_date = dt.date(2016,10,1)
    # vacay_end_date = dt.date(2016,10,7)

    for dt in daterange:
        vacay_all = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()

    session.close()

    vacay_all1 = list(np.ravel(vacay_all))

    return jsonify(vacay_all1)
    

if __name__ == '__main__':
    app.run(debug=True)