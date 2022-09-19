"""
Module to interact with the database.
"""

from . import placeholders
from . import db_ops

db_ops.ensure_db()


def search_stations(q):
    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """

    query = f"SELECT name, code FROM (SELECT name, code, LOWER(name) || LOWER(code) as search_index FROM station) WHERE search_index LIKE '%{q.lower()}%' limit 10"
    stations = db_ops.exec_query(query)
    response = [{"name": name, "code": code} for name, code in stations[1]]
    return response

def search_trains(
        from_station_code,
        to_station_code,
        ticket_class=None,
        departure_date=None,
        departure_time=[],
        arrival_time=[]):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """
    query = f"SELECT * from train WHERE from_station_code == '{from_station_code}' AND to_station_code == '{to_station_code}'"
    trains = db_ops.exec_query(query)
    response = []
    for train in trains[1]:
        response.append({trains[0][i]: train[i] for i in range(12) if not i in [2, 3]})

    return response

def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    return placeholders.SCHEDULE

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    # TODO: make a db query and insert a new booking
    # into the booking table

    return placeholders.TRIPS[0]

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    return placeholders.TRIPS
