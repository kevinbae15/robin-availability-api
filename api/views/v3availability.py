from rest_framework import generics
from rest_framework import status
import json
from datetime import datetime, timezone
from rest_framework.views import Response
from api.views.views import *
from api.views.v2availability import availability as v2availability
import heapq
import copy
import logging

logger = logging.getLogger("ten.server")

class availability(v2availability):
    def get(self, request, *arg, **kwargs):    
        _, parametersObject, _ = self.checkParameters(request)
        userData = self.getUserData()

        timeRangeStart = parametersObject['timeRange']['start']
        timeRangeEnd = parametersObject['timeRange']['end']

        allUsersAvailabilityList = {}
        for user in parametersObject['users']:
            userAvailabilityList = []
            for data in userData[user]:
                workStart = dp.parse(data['working_hours']['start'] + " " + data['time_zone'])
                workEnd = dp.parse(data['working_hours']['end'] + " " + data['time_zone'])

                availability = self.findDayAvailability(data['events'], workStart, workEnd)
                userAvailabilityList.append(availability)

            cleanedUserAvailibilityList = self.cleanUpAvailability(userAvailabilityList, timeRangeStart, timeRangeEnd)
            allUsersAvailabilityList[user] = cleanedUserAvailibilityList

        # test case
        allUsersAvailabilityList = {
          1: [{'start': datetime(2019, 1, 2, 9, 0), 'end': datetime(2019, 1, 2, 12, 0)}], 
          2: [{'start': datetime(2019, 1, 2, 10, 0), 'end': datetime(2019, 1, 2, 14, 0)}], 
          3: [{'start': datetime(2019, 1, 2, 13, 0), 'end': datetime(2019, 1, 2, 17, 0)}], 
          4: [{'start': datetime(2019, 1, 2, 0, 0), 'end': datetime(2019, 1, 2, 17, 0)}],
        }


        intersections = self.findAllIntersections(allUsersAvailabilityList)

        return Response({"status": "success", "data": intersections}, status=200)

    def findAllIntersections(self, availabilityList):
        res = []
        start_heap = []

        for user, availability in availabilityList.items():
            for a in availability:
                start_heap.append((a['start'], a['end'], user))
                
        heapq.heapify(start_heap)
        currAvailability = heapq.heappop(start_heap)

        currStart = currAvailability[0]
        currEnd = currAvailability[1]
        currUserId = currAvailability[2]

        currOverlap = {
            "start": currStart,
            "end": None,
            "userIds": [currUserId]
        }

        # Idea is to utilize one min heap sorted by start
        # All availabilities are inserted into start_heap
        # Grab the first item (A) from start_heap as basis
        # Grab the next item (B) from start_heap to compare
        # There are two cases:
        #   1) If A's end time is less then or equal to B's start time, we can move on from A. Use B as basis from now on
        #   2) Otherwise, there is overlap. Keep track of these time ranges in an object. Now, we would have to run a recursive function to check if there 
        #      are additional items that start before B's end time. We would setup our function so that if we find another item, we add the current 
        #      state of the tracking object to our result and then continue building it by adding the new item. Recursve again.
        # Some additional logic is if item B or any subsequent items are encapsulated by item A's range, we would remove them from the heap as they no longer need processing
        # And we would also need to check for duplicates in the result 


        return res

    def retrieveNextAvailability(self, start_heap):
        nextAvailability = heapq.heappop(start_heap)
        nextStart = nextAvailability[0]
        nextEnd = nextAvailability[1]
        nextUserId = nextAvailability[2]

        return start_heap, nextStart, nextEnd, nextUserId
