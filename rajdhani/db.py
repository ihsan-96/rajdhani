"""
Module to interact with the database.
"""

from . import placeholders
from . import constants
from . import db_ops

db_ops.ensure_db()


def search_stations(q):
    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """
    q = q.lower()
    # query = f"""SELECT name, code FROM
    #                 (SELECT name, code, LOWER(code) || '-' || LOWER(name) as search_index FROM station)
    #             WHERE search_index LIKE '%{q}%'
    #             ORDER BY (CASE WHEN code == '{q.upper()}' THEN 1 ELSE 2 END)
    #             LIMIT 10"""
    query = f"""SELECT name, code FROM
                    (
                        SELECT name, code FROM station WHERE LOWER(code) LIKE '{q}%'
                        UNION
                        SELECT name, code FROM station WHERE LOWER(name) LIKE '%{q}%'
                    )
                LIMIT 10"""
    stations = db_ops.exec_query(query)
    response = [{"name": name, "code": code} for name, code in stations[1]]
    return response


def get_time_slot(time_string):
    """Returns the time slot of a time"""
    time = [int(n) for n in time_string.split(":")]
    time_in_seconds = time[0] * 60 * 60 + time[1] * 60 + time[2]
    for slot in constants.TIME_SLOTS:
        if (time_in_seconds < int(slot)):
            return constants.TIME_SLOTS[slot]
    return "Invalid Slot"

# date info is not there in db.
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
    query = f"""SELECT * from train
                WHERE
                from_station_code == '{from_station_code}'
                AND to_station_code == '{to_station_code}'"""

    if ticket_class:
        query += f"AND {constants.TICKET_CLASSES[ticket_class]} == 1"

    trains = db_ops.exec_query(query)
    response = []
    for train in trains[1]:
        is_valid = True
        train = {trains[0][i]: train[i] for i in range(12) if i not in [2, 3]}

        if len(departure_time):
            print(train)
            departure_slot = get_time_slot(train["departure"])
            if departure_slot not in departure_time:
                is_valid = False

        if len(arrival_time):
            arrival_slot = get_time_slot(train["arrival"])
            if arrival_slot not in arrival_time:
                is_valid = False

        if is_valid:
            response.append(train)

    return response

def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    query = f"SELECT * FROM schedule WHERE train_number == '{train_number}' AND day != ''"
    schedule = db_ops.exec_query(query)
    response = []
    for station in schedule[1]:
        station = {schedule[0][i]: station[i] for i in range(7) if i not in [2, 3]}
        response.append(station)
    return response

def get_from_and_to_of_train(number):
    query = f"SELECT from_station_code, to_station_code FROM train WHERE number = '{number}'"
    _, train_info = db_ops.exec_query(query)
    return train_info[0]

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    from_station_code, to_station_code = get_from_and_to_of_train(train_number)
    query = "INSERT INTO booking (train_number, ticket_class, date, passenger_name, passenger_email, from_station_code, to_station_code) VALUES(?, ?, ?, ?, ?, ?, ?)"
    params = (train_number, ticket_class, departure_date, passenger_name, passenger_email, from_station_code, to_station_code)
    booking_id = db_ops.exec_insert_query(query, params, True)

    return booking_id
    # return placeholders.TRIPS[0]

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    return placeholders.TRIPS
