#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import dependencies

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify


# In[4]:


# Set up database
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


# In[10]:


# Create references

measurement = Base.classes.measurement
station = Base.classes.station

# print(measurement)
# print(station)


# In[11]:


# Create session link 

session = Session(engine)


# In[13]:


# Flast setup

app = Flask(__name__)

@app.route("/")

def welcome():
    return (
        f"Hawaii Climate Analysis<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")

def climate():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    climate = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()
    precipitation = {date: prcp for date, prcp in climate}
    return jsonify(precipitation)

@app.route("/api.v1.0/station")

def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_obs():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).filer(measurement.station == 'USC00519281').filter(measurement.date >= last_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/start/end<br/>")

def temps():
    temp = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    results = session.query(measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


# In[ ]:


if __name__ == '__main__':
    app.run()

