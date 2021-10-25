from rest_framework import generics
from rest_framework import status
import json
from datetime import datetime
from rest_framework.views import Response
from datetime import datetime as dt
import dateutil.parser as dp
import logging

logger = logging.getLogger("ten.server")


# fixes to data
# - normalize from -> start, to -> end
# - add comma
# - normalize timestamp timezones +0000 -> +00:00
# - add user_id 4 for day 2, work start and end time for user_id 3 made no sense

class availabilityBase(generics.ListCreateAPIView):

    # assumptions: 
    # there is no order to the data
    # one user object represents 1 day
    # there will always be one event in a single day (otherwise we would not know what day the work hours pertain to)
    def getUserData(self):
        dataFile = open('user_data.json', 'r')
        data = json.load(dataFile)

        newUserData = {}

        for chunk in data:
            userId = chunk['user_id']
            del chunk['user_id']
            for event in chunk['events']:
                event['start'] = dp.isoparse(event['start'])
                event['end'] = dp.isoparse(event['end'])
                          

            if userId in newUserData:
                newUserData[userId].append(chunk)
            else:
                newUserData[userId] = [chunk]

        return newUserData


    # Nice to haves: more robust parameter checks and transparent error handling
    def checkParameters(self, request):
        parametersObject = json.loads(request.body.decode("utf-8"))

        if 'users' not in parametersObject:
            raise ValueError("users array must be defined")

        if 'timeRange' not in parametersObject:
            raise ValueError("timeRange must be defined")

        if 'start' not in parametersObject['timeRange']:
            raise ValueError("timeRange start must be defined")

        if 'end' not in parametersObject['timeRange']:
            raise ValueError("timeRange end must be defined")

        parametersObject['timeRange']['start'] = dp.isoparse(parametersObject['timeRange']['start'])
        parametersObject['timeRange']['end'] = dp.isoparse(parametersObject['timeRange']['end'])

        return parametersObject


    def findIntersections(self, availabilityList):
        if len(availabilityList) < 2:
            return []

        currentAvailability = availabilityList[0]
        currentAvailabilityIndex = 1

        while currentAvailabilityIndex < len(availabilityList):
            currentAvailability = self.findIntersectionOfTwoAvailabilities(currentAvailability, availabilityList[currentAvailabilityIndex])
            currentAvailabilityIndex += 1

        return currentAvailability

    def findIntersectionOfTwoAvailabilities(self, availability1, availability2):
        intersections = []
        a1Index = 0
        a2Index = 0
        while a1Index < len(availability1) and a2Index < len(availability2):
            a1 = availability1[a1Index]
            a2 = availability2[a2Index]

            # grab the earlier availability and swap objects if needed
            if a1['start'] > a2['start']:
                availability1, availability2 = availability2, availability1
                a1, a2 = a2, a1
                a1Index, a2Index = a2Index, a1Index

            if a1['end'] > a2['start']:
                if a1['end'] >= a2['end']:
                    intersections.append({"start": a2['start'], "end": a2['end']})
                    a2Index += 1
                else:
                    intersections.append({"start": a2['start'], "end": a1['end']})
                    a1Index += 1
            else:
                a1Index += 1


        return intersections

    def sortEvents(self, data):
        data.sort(key = lambda x: x['start'])
        return data