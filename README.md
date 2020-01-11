# Website API 

# Running the API

We recommend using this inside a virtual environment.

On a Linux system:
If you want to create one and use: 

    virtualenv venv -p python3
    source venv/bin/activate

with pip installed:

    make run

this command will install all dependencies, run tests and start the API.

# API Usage

All responses will have the form:

``` json
{
    "message": "message describing what happened",
    "data": "data returned" 
}
```

# ENDPOINTS

## Information about a company


**Definition**

`GET /company`

    http://localhost:5000/company?company_name=HUT&zipcode=44667

**Arguments**

- `"company_name":str` - Company name
- `"zipcode":str`- Five digit text zipcode

**Responses**
- `200 OK` - In success (If zipcode or company_name are not passed, retrieves all companies)
- `404 NOT FOUND` - When a resource is not found


``` json
{
    "message": "Success", 
    "data": [
        {
            "id": 6, 
            "company_name": "PIZZA HUT", 
            "zipcode": "44667", 
            "website": "https://www.pizzahut.com"
        }
    ]
}
```
## Updates the website column based on a given CSV file


**Definition**

`PUT /company`

``` json
{
    "csvpath": "q2_clientData.csv"
}

```


**Arguments**

- `"csvpath":str` - Name of the csv file to be processed

**Responses**
- `200 OK` - Success, companies added
- `400 BAD REQUEST` - Cannot process the given file
- `404 NOT FOUND` - File doesn't exist/ There is no data to update in the database


``` json
{
  "message": "Success",
  "updated": [
    {
      "id": 1,
      "company_name": "TOLA SALES GROUP",
      "zipcode": "78229",
      "website": "http://repsources.com"
    },
    {
      "id": 5,
      "company_name": "SAINT PAUL RADIOLOGY",
      "zipcode": "55109",
      "website": "http://stpaulradiology.com"
    },
    {
      "id": 6,
      "company_name": "PIZZA HUT",
      "zipcode": "44667",
      "website": "https://www.pizzahut.com"
    },

```

## Loads companies into the database, based on a CSV file


**Definition**

`POST /company/data`

``` json
{
    "csvpath": "q1_catalog.csv"
}

```


**Arguments**

- `"csvpath":str` - Name of the csv file to be processed

**Responses**
- `201 CREATED` - Success, companies added
- `400 BAD REQUEST` - Cannot process the given file



``` json
{ 
   "message":"Success, companies added",
   "data":[ 
      { 
         "id":1,
         "company_name":"TOLA SALES GROUP",
         "zipcode":"78229",
         "website":null
      },
      { 
         "id":2,
         "company_name":"FOUNDATION CORRECTIONS INC",
         "zipcode":"94002",
         "website":null
      },
      { 
         "id":3,
         "company_name":"DWIGHT HARRISON VW",
         "zipcode":"30078",
         "website":null
      }
   ]
}
```

## Deletes all data from the database


**Definition**

`DELETE /company/data`


**Arguments**

- This endpoint takes no arguments

**Responses**
- `200 OK` - Success, database cleared



``` json
{
  "message": "Success, database cleared",
  "data": []
}
```
