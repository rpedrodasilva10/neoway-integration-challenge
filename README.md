# Website API 

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
- `"zipcode":str`- Fight digit text zipcode

**Response**
- `200 OK` - In success
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

## Update the website column in the database table companie


**Definition**

`POST /company`

``` json
{
    "csvpath": "q2_clientData.csv"
}

```


**Arguments**

- `"csvpath":str` - Name of the csv file to be processed

**Response**
- `200 OK` - In success
- `400 BAD REQUEST` - When the csv file is not valid


``` json
{
    "message": "Success",
    "updated": [
       {
            "company_name": "TOLA SALES GROUP",
            "zipcode": "78229",
            "website": "http://repsources.com"
        },
        {
            "company_name": "SAINT PAUL RADIOLOGY",
            "zipcode": "55109",
            "website": "http://stpaulradiology.com"
        }...
    ]
}

```
