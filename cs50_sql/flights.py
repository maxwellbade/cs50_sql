import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/flights")
def flights():
    flights = db.execute(SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists details about a single flight."""

#make sure flight exists
flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
if flight is None:
    return render_template("error.html", message="No such flight.")

#get all Passengers
passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
    {"flight_id": flight_id}).fetchall()
return render_template("flight.html",flight=flight, passengers=passengers)
