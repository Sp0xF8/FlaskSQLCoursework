from .sqlHandeling import Flight, Flash


def departORdest(departure, destination):
    if departure == "":
        print("departure is none")
        mid = Flight.getFlightTo(destination)
    elif destination == "":
        print("destination is none")
        mid = Flight.getFlightFrom(departure)
    else:
        print("both are not none")
        mid = Flight.getFlightFromTo(departure, destination)

    return mid



class Ajax:

    class Flight:
        def search(departure, destination):

            print(f"__{departure}__")
            print(f"__{destination}__")

            mid = departORdest(departure, destination)

            result = {}

            print(mid)
            print("printed mid")

            result.update({999: {
                    "index" : str(len(mid))
                    }
                })
            
            print(result)

            if (len(mid) == 0):
                Flash.error("No flights found")
                return result
            elif (len(mid) > 1):
                Flash.success("Multiple flights found")

                for i in range(len(mid)):
                    flight_id = str(mid[i][0])
                    departure = str(mid[i][1])
                    destination = str(mid[i][2])
                    departure_time = str(mid[i][3])
                    arrival_time = str(mid[i][4])
                    price = str(mid[i][5])
                    seats_left = str(mid[i][6])

                    result.update({i: {
                        "flight_id": flight_id,
                        "departure": departure,
                        "destination": destination,
                        "departure_time": departure_time,
                        "arrival_time": arrival_time,
                        "price": price,
                        "seats_left": seats_left
                    }})
                
                print(result)

                return result

            elif (len(mid) == 1):
                Flash.success("Flight found")

                flight_id = str(mid[0][0])
                departure = str(mid[0][1])
                destination = str(mid[0][2])
                departure_time = str(mid[0][3])
                arrival_time = str(mid[0][4])
                price = str(mid[0][5])
                seats_left = str(mid[0][6])


                result.update({0: {
                        "flight_id": flight_id,
                        "departure": departure,
                        "destination": destination,
                        "departure_time": departure_time,
                        "arrival_time": arrival_time,
                        "price": price,
                        "seats_left": seats_left
                    }})

                print(result)

                return result

