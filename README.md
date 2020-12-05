# Backend 

This is the backend part of the test that consist of building a REST API to expose endpoints in order to filter 
the bitcoin price to MXN currency by:

+ year
+ month
+ week
+ last 24 hours
+ range of dates

## What I used

+ django: main server
+ django rest framework: build the rest api
+ pandas: parse a csv file to upload to the local server
+ requests: http request to bitso API and the local server
+ sqlite3: as database, to keep things easier


## How to run it?

**Make sure to run first the backend server to avoid errors in the front end (api calls to localserver).**

Clone the repository:
```sh
$ git clone https://github.com/daniel-sjkdm/backEndCapptu.git
```

Create a virtual environment and activate it:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Install all the dependencies:
```sh
$ pip install -r requirements.txt
```

Run the server:
```sh
$ python manage.py runserver
```


## History data

Since the Bitso API only provides information for the current time the request is made I
chose to download a csv file with data that was recorded since the 2017 year. 

That data is preprocessed with pandas library and then is stored at the database making POST calls
to the django REST API.

[Bitso history data](https://www.CryptoDataDownload.com)

The script to upload the data to the sqlite3 database is __preprocess_bitso_history.py__.


## REST API

The endpoint are the following:

```
  [Get all the records]
  http://localhost:8000/coinz/api/

  [Get the last week's records]
  http://localhost:8000/coinz/api/by-week/

  [Get the last month's records]
  http://localhost:8000/coinz/api/by-month/

  [Get records by years, separated by 7 days each one]
  http://localhost:8000/coinz/api/by-year/

  [Get records of the last 24 hours]
  http://localhost:8000/coinz/api/last-24/

  [Get records for a given date range]
  http://localhost:8000/coinz/api/date-range/?date1=<date1>&date2=<date2>

  [Get the current btc convertion mxn]
  http://localhost:8000/coinz/api/repeat/
```


## Testing the API

The API can be tested using this CLI tools:

+ curl, jq
+ httpie

Example:

```sh
$ curl http://localhost:8000/api/ | jq
```

Output:
```json
{
  "id": 9952,
  "book": "btc_mxn",
  "created_at": "2020/10/22 11:00:00",
  "volume": 19.94,
  "high": 274749.99,
  "low": 272101.51,
  "last": null,
  "vwap": null,
  "ask": null,
  "bid": null
}
```