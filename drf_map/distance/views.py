from rest_framework.response import Response
from rest_framework import generics
from haversine import haversine, Unit
import os, requests

class GeocodingApiView(generics.GenericAPIView):

    def calculate_distance(self, from_address, to_address):
        key = os.environ.get("api_key")
        from_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={from_address}&key={key}"
        to_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={to_address}&key={key}"
        from_req = requests.get(from_url)
        to_req = requests.get(to_url)
        if from_req.status_code == 200 and to_req.status_code == 200:
            
            f = tuple(from_req.json()["results"][0]["geometry"]["location"].values())
            t = tuple(to_req.json()["results"][0]["geometry"]["location"].values())
            result = haversine(f,t)
            return result

    def get(self, request):
        from_address = request.GET.get("from")
        to_address = request.GET.get("to")
        if from_address and to_address:
            result = self.calculate_distance(from_address, to_address)
            response = f"The distance between {from_address} and {to_address} is {int(result)}km"
            return Response({"distance":response})
        else:
            return Response({"distance":""})


# The Distance Matrix API is a service that provides travel distance and time
# for a matrix of origins and destinations, based on the recommended route
# between start and end points.
class DistanceMatrixApiView(generics.GenericAPIView):

    def send_request(self, from_address, to_address, mode):
        key = os.environ.get("api_key")

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={from_address}&destinations={to_address}&mode={mode}&key={key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

    def calculate_distance(self, api_response):
        if api_response["rows"][0]["elements"][0]["status"] == "OK":
            distance = api_response["rows"][0]["elements"][0]["distance"]["text"]
            return distance
        else:
            return None

    def calculate_duration(self, api_response):
        if api_response["rows"][0]["elements"][0]["status"] == "OK":
            distance = api_response["rows"][0]["elements"][0]["duration"]["text"]
            return distance
        else:
            return None

    def get(self, request):
        # mode = request.GET.get("mode")
        mode = "driving"
        from_address = request.GET.get("from")
        to_address = request.GET.get("to")
        if from_address and to_address:
            api_response = self.send_request(from_address, to_address, mode)
            print(api_response)
            distance = self.calculate_distance(api_response)
            duration = self.calculate_duration(api_response)

            if distance is not None and duration is not None:
                response = f"The distance between {from_address} and {to_address} is {distance}. It will take {duration} to reach there."
                return Response({"distance":response})
            else:
                return Response({"distance":"There are no result for {} mode".format(mode)})
        else:
            return Response({"distance":""})
        
