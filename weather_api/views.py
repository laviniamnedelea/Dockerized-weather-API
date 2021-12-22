from django.db.models.functions import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from .models import Tari, Orase, Temperaturi


def index(request):
    return HttpResponse("Hello, world. You're at the weather index.")

# Used for /countries/id
@api_view(['PUT', 'DELETE'])
def countries_id(request, id): # id is the route parameter.
    # The id is sent both in the JSON and as a route parameter.
    if request.method == "PUT":
        try:
            data = json.loads(request.body) # Load the received json.
            if (id != data["id"]): # Checking for the ids in the route and
                # in the JSON to be corresponding.
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try: # It is not mandatory to be sent all the parameters for PUT
                # therefore it is required to take into consideration all possibilities.
                nume = data["nume"]
            except:
                nume = None
            try:
                latitudine = data["lat"]
            except:
                latitudine = None
            try:
                longitudine = data["lon"]
            except:
                longitudine = None

            tara = Tari.objects.get(id=id)
            if not tara: # Verify if the country that needs to be modified exists.
                return Response(status=status.HTTP_404_NOT_FOUND)
            if nume: # Change only the existing parameters.
                tara.nume_tara = nume
            if latitudine:
                tara.latitudine = latitudine
            if longitudine:
                tara.longitudine = longitudine
            tara.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try: # Verify if the required field that needs to be deleted exists.
            entry = Tari.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entry.delete()
            return Response(status=status.HTTP_200_OK)
        except: # If the field exists, but another error occured, error 400 is returned.
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Used for /countries
@api_view(['POST', 'GET'])
def countries(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # Load the sent JSON.
            nume = data["nume"]
            latitudine = data["lat"]
            longitudine = data["lon"]
            try:
                latitudine = float(latitudine)
                longitude = float(longitudine)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            tara = Tari(nume_tara=nume, latitudine=latitudine, longitudine=longitudine)
            try:
                tara.save()
            except:
                return Response(status=status.HTTP_409_CONFLICT)
            # If the country already exists in the database.
            res = {"id": tara.id} # If the POST was successful, return the id
            # of the new inserted field.
            return Response(res, status=status.HTTP_201_CREATED)
        except: # Otherwise, return a BAD REQUEST error.
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET': # Get all countries in the database.
        data = Tari.objects.all()
        objs = []
        for i in data: # The data will be returned even if there is no found object
            objs.append({"id": i.id, "nume": i.nume_tara, "lat": i.latitudine, "lon": i.longitudine})
        return Response(objs, status=status.HTTP_200_OK) # 200_OK is always returned for GET
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Used for cities/country/<int:id_Tara>
@api_view(["GET"])
def cities_per_country(request, id_Tara):
    if request.method == "GET": # Returns all cities in a country
        orase = Orase.objects.filter(tara_id=id_Tara) # Find all cities by country id.
        objs = []
        for i in orase:  # The data will be returned even if there is no found object
            objs.append(
                {"id": i.id, "idTara": i.tara_id, "nume": i.nume_oras, "lat": i.latitudine, "lon": i.longitudine})
        return Response(objs, status=status.HTTP_200_OK)

# cities/<int:id>
@api_view(["DELETE", "PUT"])
def cities_id(request, id): # route parameter
    if request.method == "PUT": # Modify the cities
        try:
            data = json.loads(request.body) # Load the received JSON.
            if (id != data["id"]): # Check that the id in the JSON
                # corresponds to the route parameter, otherwise return
                # BAD REQUEST.
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try: # Not all parameters are required. Take each situation
                # into consideration.
                idTara = data["idTara"]
            except:
                idTara = None
            try:
                nume = data["nume"]
            except:
                nume = None

            try:
                latitudine = data["lat"]
                try:
                    latitudine = float(latitudine)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                latitudine = None

            try:
                longitudine = data["lon"]
                try:
                    longitudine = float(longitudine)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                longitudine = None

            oras = Orase.objects.get(id=id)
            if not oras: # Check if the city to be modified exists,
                # otherwise return 404 NOT FOUND.
                return Response(status=status.HTTP_404_NOT_FOUND)
            if idTara: # Check if the country of the city exists,
                # otherwise return 400 BAD REQUEST.
                tara = Tari.objects.get(id=idTara)
                if not tara:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                oras.tara_id = idTara
            if nume:
                oras.nume_oras = nume
            if latitudine:
                oras.latitudine = latitudine
            if longitudine:
                oras.longitudine = longitudine
            oras.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            entry = Tari.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entry.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Used for /cities
@api_view(['POST', 'GET'])
def cities(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # Loads the received JSON
            idTara = data["idTara"]
            nume = data["nume"]
            latitudine = data["lat"]
            longitudine = data["lon"]
            try:
                latitudine = float(latitudine)
                longitudine = float(longitudine)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            tara = Tari.objects.get(id=idTara) # Checks whether the city's country exists
            if not tara:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            oras = Orase(nume_oras=nume, latitudine=latitudine, longitudine=longitudine, tara=tara)
            try:
                oras.save() # Insert the city field, otherwise return 409 CONFLICT
            except:
                return Response(status=status.HTTP_409_CONFLICT)
            res = {"id": oras.id} # If successful, return the id of the inserted field.
            return Response(res, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET': # Get all cities
        data = Orase.objects.all()
        objs = []
        for i in data:
            objs.append(
                {"id": i.id, "idTara": i.tara_id, "nume": i.nume_oras, "lat": i.latitudine, "lon": i.longitudine})
        return Response(objs, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#Used for /temperatures
@api_view(['POST', 'GET'])
def temperatures(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_oras = data["idOras"]
            valoare = data["valoare"]
            oras = Orase.objects.get(id=id_oras) # Check the city of the temperature
            #field to be inserted exists, otherwise return 400 BAD REQUEST
            try:
                valoare = float(valoare)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if not oras:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            temperatura = Temperaturi(valoare=valoare, oras=oras)
            try:
                temperatura.save()
            except:
                return Response(status=status.HTTP_409_CONFLICT)
            res = {"id": temperatura.id}
            return Response(res, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # used for temperatures?lat=Double&lon=Double&from=Date&until=Date
    elif request.method == 'GET':
        # TRy to get each parameter from the request
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        from_ = request.GET.get("from")
        until_ = request.GET.get("until")
        objs = []
        try: # Try every possibility, firstly filtering the fields only by
            # longitude and latitude. After selecting only the fields that match
            # the given inputs for these, the result stored in the objs list
            # will be filtered based on the from and/or until date, if existing.
            if (lat is not None and lon is not None):
                orase = Orase.objects.filter(latitudine=lat, longitudine=lon)
                if orase is not None:
                    for oras in orase:
                        temps = Temperaturi.objects.filter(oras_id=oras.id)
                        for temp in temps:
                            objs.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp
                                         })
            elif (lat is not None):
                orase = Orase.objects.filter(latitudine=lat)
                if orase is not None:
                    for oras in orase:
                        temps = Temperaturi.objects.filter(oras_id=oras.id)
                        for temp in temps:
                            objs.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
            elif (lon  is not None):
                orase = Orase.objects.filter(longitudine=lon)
                if orase is not None:
                    for oras in orase:
                        temps = Temperaturi.objects.filter(oras_id=oras.id)
                        for temp in temps:
                            objs.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
            else:
                temps = Temperaturi.objects.all()
                for temp in temps:
                    objs.append(
                        {"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})

            response = [] # The response list will be the final answer sent back in the response.
            # Based on the objs list, the response will be built, by taking into consideration
            # all possibilities of having the start date and/or the end date (from/until)

            if from_ is not None:
                from_ = datetime.datetime.strptime(from_, "%Y-%m-%d").date()
            if until_ is not None:
                until_ = datetime.datetime.strptime(until_, "%Y-%m-%d").date()

            if (from_ is not None and until_ is not None):
                for temp in objs:
                    if temp["timestamp"].date() >= from_ and temp["timestamp"].date() <= until_:
                        response.append(temp)

            elif (from_ is not None):
                for temp in objs:
                    if temp["timestamp"].date() >= from_:
                        response.append(temp)

            elif (until_ is not None):
                for temp in objs:
                    if temp["timestamp"].date() <= until_:
                        response.append(temp)
            else:
                response = objs

        except:
            response = []

        # The result will be a list of dictionaries/JSON objects
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# used for temperatures/cities/<int:id_oras>?from=Date&until=Date
@api_view(['GET'])
def temperatures_cities(request, id_oras):
    if request.method == 'GET':
        # The situation is the same as the one described above, but only
        # with from and until parameters.
        from_ = request.GET.get("from")
        until_ = request.GET.get("until")

        try:
            if from_ is not None:
                from_ = datetime.datetime.strptime(from_, "%Y-%m-%d").date()
            if until_ is not None:
                until_ = datetime.datetime.strptime(until_, "%Y-%m-%d").date()
            objs = Temperaturi.objects.filter(oras_id=id_oras)
            result = []

            if (from_ is not None and until_ is not None):
                for temp in objs:
                    if (temp.timestamp.date() >= from_ and temp.timestamp.date() <= until_):
                        result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})

            elif (from_ is not None):
                for temp in objs:
                    if (temp.timestamp.date() >= from_):
                        result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})

            elif (until_ is not None):
                for temp in objs:
                    if (temp.timestamp.date() <= until_):
                        result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
            else:
                for temp in objs:
                    result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
        except:
            # The result will be a list of dictionaries/JSON objects
            result = []

        return Response(result, status=status.HTTP_200_OK)


# Used for temperatures/countries/<int:id_tara>?from=Date&until=Date
@api_view(['GET'])
def temperatures_countries(request, id_tara):
    if request.method == 'GET':
        # The same situation as above, only considering each temperature, for each city
        # in a given country
        from_ = request.GET.get("from")
        until_ = request.GET.get("until")

        try:
            if from_ is not None:
                from_ = datetime.datetime.strptime(from_, "%Y-%m-%d").date()
            if until_ is not None:
                until_ = datetime.datetime.strptime(until_, "%Y-%m-%d").date()
            orase = Orase.objects.filter(tara_id=id_tara)
            result = []
            for o in orase:  # For each city
                temps = Temperaturi.objects.filter(oras_id=o.id)  # Get all the temperatures of a city

                if (from_ is not None and until_ is not None):
                    for temp in temps:
                        if (temp.timestamp.date() >= from_ and temp.timestamp.date() <= until_):
                            result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})

                elif (from_ is not None):
                    for temp in temps:
                        if (temp.timestamp.date() >= from_):
                            result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})

                elif (until_ is not None):
                    for temp in temps:
                        if (temp.timestamp.date() <= until_):
                            result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
                else:
                     for temp in temps:
                        result.append({"id": temp.id, "valoare": temp.valoare, "timestamp": temp.timestamp})
        except:
            result = []

        return Response(result, status=status.HTTP_200_OK)

# Used for temperatures/<int:id_temp>
@api_view(['PUT', 'DELETE'])
def temperatures_id(request, id_temp):
    if request.method == 'PUT': # Will modify the given temperature.
        try:
            data = json.loads(request.body)
            if (id_temp != data["id"]): # If the id in the route and JSON are different,
                # return 400 BAD REQUEST
                return Response(status=status.HTTP_400_BAD_REQUEST)
           
            try:
                id_oras = data["idOras"]
                try:
                    id_oras = int(id_oras)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                id_oras = None

            try:
                valoare = data["valoare"]
                try:
                    valoare = float(valoare)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                valoare = None

            try:
                timestamp = data["timestamp"]
            except:
                timestamp = None

            temp = Temperaturi.objects.get(id=id_temp)
            if not temp:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if id_oras:
                oras = Orase.objects.get(id=id_oras)
                if not oras:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                temp.oras_id = id_oras

            if valoare:
                temp.valoare = valoare
            if timestamp:
                temp.timestamp = timestamp
            temp.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            entry = Temperaturi.objects.get(id=id_temp)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            entry.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
