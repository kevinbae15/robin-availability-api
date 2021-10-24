from rest_framework import generics
from rest_framework import status
import json
from datetime import datetime
from rest_framework.views import Response
from api.views.views import *
from api.views.v1availability import availability as v1availability
import logging

logger = logging.getLogger("ten.server")

class availability(v1availability):
    def get(self, request, *arg, **kwargs):    
        _, parametersObject, _ = self.checkParameters(request)
        userData = self.getUserData()

        timeRangeStart = parametersObject['timeRange']['start']
        timeRangeEnd = parametersObject['timeRange']['end']

        allUsersAvailabilityList = []
        for user in parametersObject['users']:
            userAvailabilityList = []
            for data in userData[user]:
                workStart = dp.parse(data['working_hours']['start'] + " " + data['time_zone'])
                workEnd = dp.parse(data['working_hours']['end'] + " " + data['time_zone'])

                try: 
                    availability = self.findDayAvailability(data['events'], workStart, workEnd)
                    userAvailabilityList.append(availability)
                except Exception as e:
                    return Response({"status": "error", "errorMessage": "Something went wrong"}, status=500)

            cleanedUserAvailibilityList = self.cleanUpAvailability(userAvailabilityList, timeRangeStart, timeRangeEnd)
            allUsersAvailabilityList.append(cleanedUserAvailibilityList)

        intersections = self.findIntersections(allUsersAvailabilityList)

        return Response({"status": "success", "data": intersections}, status=200)

    def cleanUpAvailability(self, availabilityList, timeRangeStart, timeRangeEnd):
        newList = []
        for a in availabilityList:
            newList += a

        newList = self.sortEvents(newList)
        newList = self.findIntersectionOfTwoAvailabilities(newList, [{"start": timeRangeStart, "end": timeRangeEnd }])
        return newList


    def findDayAvailability(self, userEvents, start, end):
        if len(userEvents) == 0
            raise TypeError("insertAttributes: productObject is not valid")

        userEvents = self.sortEvents(userEvents)
        
        year = userEvents[0]['start'].year
        month = userEvents[0]['start'].month
        day = userEvents[0]['start'].day
        start = start.replace(year=year, month=month, day=day)
        end = end.replace(year=year, month=month, day=day)

        
        return self.findAvailability(userEvents, start, end)