from rest_framework import generics
from rest_framework import status
import json
from rest_framework.views import Response
from api.views.views import *
import logging

logger = logging.getLogger("ten.server")

class availability(availabilityBase):
    def get(self, request, *arg, **kwargs):    
        try:
            parametersObject = self.checkParameters(request)
        except ValueError as e:
            return Response({"status": "fail", "errorMessage": str(e)}, status=400)
        except Exception as e:
            return Response({"status": "error", "errorMessage": "Something went wrong"}, status=500)

        userData = self.getUserData()

        timeRangeStart = parametersObject['timeRange']['start']
        timeRangeEnd = parametersObject['timeRange']['end']

        availabilityList = []
        for user in parametersObject['users']:
            userEvents = self.squashEvents(userData[user])
            availability = self.findAvailability(userEvents, timeRangeStart, timeRangeEnd)
            availabilityList.append(availability)

        intersections = self.findIntersections(availabilityList)

        return Response({"status": "success", "data": intersections}, status=200)

    def squashEvents(self, userData):
        userEvents = []

        for data in userData:
            for event in data['events']:          
                userEvents.append(event)

        return userEvents