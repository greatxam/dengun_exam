# Dengun Backend Engineering Challenge
***Dengun Backend Engineering Challenge*** is a simple Django app thats can create an email and send it to one or more recipient.

# Main Objects
* Create a simple dashboard with django-admin
* How the information is displayed, is up to you.
* This dashboard will allow me to create simple emails and send them to one or more email destinations.
* This dashboard will allow me to see emails that I've sent previously and their status (sent, failed, pending)
* Emails must be send asynchronously. Use celery to achieve this goal
* Celery will send the emails using www.mailgun.com API (free plan available)
* The entire setup must be done using docker and docker-compose
* Ideally, to test the project, I'll just need to do docker-compose up

# Requirements
* [Python 3.7](https://www.python.org/downloads/)
* [Celery 4.3](http://www.celeryproject.org/)
* [Docker](https://www.docker.com/)

# Starting up the Server
***Creating new super user***
```
docker-compose run app sh -c "./manage.py createsuperuser"
```

***Running the app***
```
docker-compose run up
```
