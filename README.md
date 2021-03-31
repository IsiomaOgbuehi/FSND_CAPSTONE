# FSND_CAPSTONE

## Nutritionists Articles

This project makes nutritional articles available to subscribed clients. Clients get to read nutritional articles posted by their nutritionists. It serves as a capstone project in fullfilment of a fullstack nanodegree with Udacity.

All backend code follows [PEP8 style guidelines.](https://www.python.org/dev/peps/pep-0008/)

As part of the completion requirements, API Endpoints have been developed to handle the following:

1.  Create/Edit Nutritionists
2.  Create/Edit Clients
3.  Create Articles with assigned nutritionist
4.  View/Edit/Delete Articles



## Getting Started

Developers using this project should already have Python3 and pip intalled on their local machines.

### Backend

From the backend folder run pip install requirements.txt preferably in a virtual environment. All required packages are included in the requirements file.

### Setup

Edit database connection in setup.sh if you're using a different database, else create database from psql terminal:

$ sudo -u postgres_user -i
$ createdb fsnd_capstone

From the project directory, run:

$ source setup.sh

### Migration

In project directory, run the following commands for DB Migration:

```bash
flask db init
flask db migrate
flask db upgrade
```

### Run Project
To run the application run the following commands:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
For auto reload, append --reload when running app: 
```
flask run --reload
```

These commands put the application in development. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation.](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/)

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

### Authentication

Three Roles have been created with different access permissions. To generate an access token for each user, use the link and login access below:

(https://dev-isi.us.auth0.com/authorize?response_type=token&client_id=CBW3nYVQaX4PYPNNGYCPb4fqDimF3jGe&redirect_uri=https://127.0.0.1:8080/home&audience=nutrition_article)

1.  App Manager - Has all access permission
    username: appmanager@capsone.com
    password: AppManager@111

2.  Nutritionist Manager
    username: nutritionistmanager@capsone.com
    password: NutritionistManager@111

    Roles:
    create:nutritionist
    edit:nutritionist
    view:nutritionist
    create:article
    read:article
    edit:article
    delete:article
    view:client

3.  Client Manager
    username: clientmanager@capsone.com
    password: ClientManager@111

    Roles:
    create:client
    edit:client
    read:article
    subscribe:client
    view:client
    view:nutritionist

Add access_token to envrironment variable:
```
export JWT_TOKEN=generated_token
```

### Testing

In order to run tests, from app folder and run the following commands:

```bash
python test_app.py
```

## API Reference

### Getting Started

* Base URL: At present, this app can run locally and is also hosted in cloud server. 
Local URL default is: `http://127.0.0.1:5000/`. 
Server URL is: `https://fsnd-nutrition-article.herokuapp.com/`

* Authentication: Generated token must be added to URL headers to test application.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return four error types when requests fail:

* 412: Precondition Failed
* 404: Resource Not Found
* 422: Unprocessed Request
* 500: Internal Server Error

### Endpoints

### POST /nutritionists
* Creates new nutritionist
    * JSON Body: {"name": "Smaklie Brown", "specialization": "Pediatrics", "email": "smaklie@test.com", "rating": 5}
    * Response:

    ```
    {
        "email": "maskot@test.com",
        "message": "Nutritionist Created",
        "success": true
    }
    ```

### GET /nutritionists
* GET all nutritionists
    * Response:

    ```
    {
        "data": [
            {
                "id": 1,
                "name": "Maskot Rise"
            }
        ],
        "success": true
    }
    ```

### GET /nutritionists/<id>
* GET specific nutritionist
    * Response:

    ```
    {
        "data": {
            "email": "maskot@test.com",
            "id": 1,
            "name": "Maskot Rise",
            "rating": 0,
            "specialization": "Pediatrics"
        },
        "success": true
    }
    ```

### POST /clients
* Creates new client
    * JSON BODY: {"name": "Manning Dreake", "country": "Egypt", "email": "manning@test"}
    * Response:

    ```
    {
        "email": "manning@test",
        "message": "client created",
        "success": true
    }
    ```

### GET /clients
* GETS all clients
    * Response:

    ```
    {
        "data": [
            {
                "id": 1,
                "name": "Manning Dreake"
            }
        ],
        "success": true
    }
    ```

### GET /clients/<id>
* GETS specific client
    * Response:

    ```
    {
        "data": {
            "country": "Egypt",
            "email": "manning@test",
            "name": "Manning Dreake"
        },
        "success": true
    }
    ```

### PATCH /clients/<id>
* Update client
    * Response:
    * JSON BODY: {"id": 1, "name": "Manning Client", "country": "Egypt", "email": "manning@test"}
    * Required Field: id
    ```
    {
        "id": 1,
        "message": "User data updated",
        "success": true
    }
    ```

### PATCH /nutritionists
* Creates new nutritionist
    * JSON BODY: {"id": 1, "name": "Smaklie Brown", "specialization": "Pediatrics", "email": "smaklie@test.com", "rating": 5}
    * Required Field: id
    * Response:

    ```
    {
        "id": 1,
        "message": "user data updated",
        "success": true
    }
    ```