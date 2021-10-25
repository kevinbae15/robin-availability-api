# robin-availability-api
> Api that takes in user data and provides available times for users to meet


## Setup

### Setup virtual environment

```
python3 -m venv dev
. dev/bin/activate
pip3 install -r requirements.txt
```

### Start

```
python3 manage.py runserver <port_number>
```

## Endpoints
- GET  `/api/v1/availability`
- GET  `/api/v2/availability`
- GET  `/api/v3/availability`


### GET `/api/v[X]/availability`

Parameters:
```
{
    "users": [1,2,3],
    "timeRange": {
        "start": "2019-01-02T00:00:00+00:00",
        "end": "2019-01-03T00:00:00+00:00"
    }
} 
```

Success Response Example:

```
{
    "status": "success",
    "data": [
        {
            "start": "2019-01-02T13:00:00Z",
            "end": "2019-01-02T14:00:00Z"
        }
    ]
}
```


Fail Response Example:

```
{
  "status": "error",
  "errorMessage": "Number of events cannot be empty"
}
```


## Reflections

My thought proccess with the first two challenges were finding every user's available times by finding the complement of the event time ranges. From there, we can filter out availability by work hours and get the intersection of availabilities for all users. I realized on the third challenge, this approach would call for a very inefficient solution where we would have find intersections of every single combination of availability time range. 

My thought process went to utilizing two min heaps and linearly going through each available times in order. One to keep track of time ranges we did not encounter yet and another to keep track of time ranges that have not ended yet. They two would be heapified by start time and end time of the time ranges, respectively. I would continue to utilize past solutions to find every user's availability time ranges. However, I think I got caught up on the complexity of the problem and ended up getting stuck.

After taking a step back, my thought process went only utlizing a single min heap, which would be heapified by start time. After inserting all availabilties, we would pop the first item in the heap and keep track of the next item. If they overlap, we can add this to our result, but we need to continue through the popped item's time range, to check if there are additional availabilities overlapping. We can utilize some form of recursion to push an object with time ranges and user ids in a cascading style. However, if they not overlap, we can move onto the next time range by popping the heap again. Keep going until the heap has only 1 range left.

There would need to be additional logic, such as preventing duplicate time ranges by using memoization or skipping time ranges that are completely encapsulated for optimization.

Some additional functionality that would be nice is better user parameter checking to prevent bad requests and optimizing some of the logic behind finding availabilities (adding boundaries from user provided time range before processing) and intersections (using similar logic to above to find time ranges where all users are present).