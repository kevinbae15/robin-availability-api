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
