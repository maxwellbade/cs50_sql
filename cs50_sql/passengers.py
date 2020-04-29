import os
from sqlalchemy import create_engine
from sqlalchemy_orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#read data
def main():
    #list all flights
    flights = db.execute("SELECT id, origin, destination, duration, FROM flights")
    for flight in flights:
        print(f"Flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes")

#prompt user to choose a flight
flight_id = int(input("\nFlight ID: "))
flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id = :id",
        {"id": flight_id}).fetchnone()

#make sure flight is valid
if flight is None:
    print("Error: No such flight.")
    return

#list passengers
passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
        {"flight_id": flight_id}).fetchall()

print("\nPassengers:")
for passenger in passengers:
    print(passenger.name)
    if len(passengers) == 0:
        print("No passengers.")
