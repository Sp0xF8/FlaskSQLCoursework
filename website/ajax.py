from .sqlHandeling import Flight, Flash, Passenger


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
            mid = departORdest(departure, destination)

            result = {}

            result.update({999: {
                    "index" : str(len(mid))
                    }
                })
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
                return result

        def getPassengerDetailsByID(passenger_id):
            passengerInvalid = []


            for ids in passenger_id:
               passengerInvalid.append(Passenger.getPassengerByUIDandPID(ids))

            passengerValid = {}

            passengerValid.update({999: {
                "index" : str(len(passengerInvalid))
                }
            })
            if (len(passengerInvalid) == 0):
                Flash.error("No Passenger found")
                return passengerValid
            elif (len(passengerInvalid) > 1):
                Flash.success("Multiple flights found")

                for i in range(len(passengerInvalid)):
                    passenger_id = str(passengerInvalid[i][0])
                    user_id = str(passengerInvalid[i][1])
                    first_name = str(passengerInvalid[i][2])
                    last_name = str(passengerInvalid[i][3])
                    date_of_birth = str(passengerInvalid[i][4])
                    gender = str(passengerInvalid[i][5])
                    passport_number = str(passengerInvalid[i][6])

                    passengerValid.update({i: {
                        "passenger_id": passenger_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": date_of_birth,
                        "gender": gender,
                        "passport_number": passport_number
                    }})

                return passengerValid
            elif (len(passengerInvalid) == 1):
                Flash.success("Flight found")

                passenger_id = str(passengerInvalid[0][0])
                user_id = str(passengerInvalid[0][1])
                first_name = str(passengerInvalid[0][2])
                last_name = str(passengerInvalid[0][3])
                date_of_birth = str(passengerInvalid[0][4])
                gender = str(passengerInvalid[0][5])
                passport_number = str(passengerInvalid[0][6])


                passengerValid.update({0: {
                        "passenger_id": passenger_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": date_of_birth,
                        "gender": gender,
                        "passport_number": passport_number
                    }})
                return passengerValid
        
            


            

