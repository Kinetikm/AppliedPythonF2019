from mysite.orm import Flight

flights = {
    0: {
        "departure": "22:31",
        "arrival": "6:44",
        "travel_time": "8:13",
        "destination": "Tokyo",
        "aircraft_type": "Syknoi SuperJet"
    },
    1: {
        "departure": "20:31",
        "arrival": "5:44",
        "travel_time": "9:13",
        "destination": "Jamaica",
        "aircraft_type": "Snoop-Dog Airbus A320"
    },
    2: {
        "departure": "7:31",
        "arrival": "13:44",
        "travel_time": "6:13",
        "destination": "Riyadh",
        "aircraft_type": "Snoop-Dog Airbus A320"
    }
}

def test():
    for flight in flights.items():
        flightdb = Flight()
        flightdb.departure = flight["departure"]
        flightdb.arrival = flight["arrival"]
        flightdb.travel_time = flight["travel_time"]
        flightdb.destination = flight["destination"]
        flightdb.aircraft_type = flight["aircraft_type"]
        flightdb.save()

    allf = Flight.objects.all()
    print(allf)
