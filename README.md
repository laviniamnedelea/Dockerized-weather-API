# REST API 

This weather API provides a mean to handle data and perform CRUD operations such as retrieving temperatures 
based on one or more parameters like city, country, latitude and longitude.
It is implemented with Django for the backend, PostgreSQL as a SQL database and pgAdmin as a GUI for manipulating 
the database in an easier manner. 

The 3 services are isolated in 3 Docker containers: web, db and pgadmin, and they are each running separately from each-other.
 The configurations are done using a docker-compose file.

# 1. web service
- The port 6000 on the container is mapped to the port 6000 on the host, making sure to run the commands responsible for 
creating migration files, propagating the changes to the database and running the emulated server locally. 
- The .env.dev file will contain the environment variables, which are sensitive information like the secret key, database
 name, user, password etc. 
- A named volume (migrations-volume) is used in order to copy the date from ```/weather_api/weather_api/migrations/``` locally.
 By doing this, we make sure the migrations' history persists. 
- The web container depends on the database one to be started and it will be restarted until the operation is successful. 
(with a maximum of possible tries and an increasing waiting time inbetween)
- The web container is deployed in the backend and frontend networks. 

# 2. db service
- The database is built using PostgreSQL, which is officially suported by Django, making use of the "postgres:11" image. 
- A bind mount is used in order to persist data, with the host path './database/postgres_data'. This directory will be
ignored in .dockerignore and created automatically on each host machine.
- The 5432 port on the container will be mapped to 5432 to the host. An important note here is we should make sure 
that psql is not already running on that port, in which case an error will be returned. If so, 
run ```sudo service postgresql stop```.
- The db container is deployed in the backend network. 

# 3. pgadmin service
- pgAdmin is an open source tool which provides a GUI for handling and managing the database in an easier manner. 
- The container will run the dpage/pgadmin4 image from Docker Hub
- The port 5050 on the host machine will be mapped on the 80 port in the container. 
- The e-mail ```pgadmin4@pgadmin.org``` and the password ```root``` will be the credentials for the GUI tool.
- The tool will only be started once the db service started and it will be restarted until the operation is successful. 
- The pgadmin container is deployed in the backend network. 

# Usage

1. The following are needed on the host machine:
a. Postman (for testing purposes)
b. Docker
c. Docker-compose

For running/testing the weather api the following steps have to be followed:
1. ```docker-compose up -d``` or, as an alternative 
  ``` docker-compose up --build -d``` (note this will rebuild the images every time is used, even if not needed)
  Starting the containers might take up to 20 seconds, since the web and pgadmin services depend on how long it takes for the database to start. If building is done as well, the time will increase.
  In case of permission erros, use ```sudo```.

2. Run the tests in Postman on port 6000.

3. Open pgAdmin. 
 3.1. In browser type:  ```http://localhost:5050/``` and log in with the credentials: 
- pgadmin4@pgadmin.org
- root
 3.2. Add New Server.
    In General: 
- Name = a name of your choice
    In Connection:
- Host name/address: db
- Port: 5432
- Username: student
- Password: root

# Testing
The API can be tested using Postman with the Test_data collection. Import it and make sure the tests are run in the following order: 
<img src="https://i.imgur.com/dplg0oT.png" width="400" height="500" />

If Postman is not run locally, make sure to replace "localhost" with your address. 

