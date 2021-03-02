## API built with Flask-Restful, JWT, SQLAlchemy, Heroku, and Marshmallow

In this project I built a RESTful API using the Flask library Flask-Restful, which allows for a more organized architecture. 

### Run APP
The main application is app.py which can be run locally. It works with SQLite when local, else, it uses the root database from heroku.
run.py precedes app.py when we use heroku, due to the uwsgi.ini (run:app). run.py runs app.py and creates the database.

app.py instantiates the RESTful API, and it exposes the endpoints:

### Security
The JWT library is used to provide a level of security for the app.
endpoints:
/register - (POST) it expects username and password, unless another username is already there.
/user - (GET) expects user_id
/user - (DELETE) expects user_id

### Resources
app.py calls resources. Each resources has an endpoint.
The resources are the HTTP verbs (POST, GET, PUT, DELETE)


### Models
The resources modules call models. These models reduce the verbose in the resources, and mostly interact with the db.

The models modules serve as tools for the resources. These models do the following:
* Create a schema for the resource
* Creates a table and specifies the columns, including columns from foreign tables
* Defines columns to be expected from the class
* It also provides additional methods (find_all, find_by_name, save, delete) that require interaction with the database