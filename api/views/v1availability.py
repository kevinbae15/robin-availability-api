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

    def findAvailability(self, userEvents, start, end):
        userEvents = self.sortEvents(userEvents)
        availability = []
        eventIndex = 0

        if len(userEvents) == 0:
            return {"start": start, "end": end}

        while eventIndex < len(userEvents):
            currEvent = userEvents[eventIndex]
            eventIndex += 1

            if start >= end:
                break

            # if start time is in between event
            if start > currEvent['start']:

                #if start is before end of event, this event can be ignored
                if start > currEvent['end']:
                    continue
                else:
                    start = currEvent['end']

            elif start == currEvent['start']:
                start = currEvent['end']
                   
            # if start time is before a start of a meeting time, there is an availability 
            else:
                if end > currEvent['start']:
                    availability.append({"start": start, "end": currEvent['start']})
                    start = currEvent['end'] 
                else:
                    availability.append({"start": start, "end": end})
                    start = currEvent['end']
                    break

        if start < end:
            availability.append({"start": start, "end": end}) 

        return availability