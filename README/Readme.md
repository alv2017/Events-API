# Events Management API

## Implemented Requirements

1) Users must be able to register an account.

2) Users must be able to log in into their .

3) A system of token rotation must be implemented. For this the API needs to provide a user with access_token 
and a refresh_token, as well as a way to refresh and validate the access_token. The lifetime of the access_token 
should be 1 hour and the lifetime of the refresh_token 1 day.

4) Users must be able to create events in the app's database (sqlite).

5) Users must be able to see the list of events they have created.

6) Users must be able to see a list of all events.

7) Users must be able to edit the events they have created but not the ones created by other users.

8) Users must be able to register to an event or un-register. This can only be done in future events 
and not in past events.


## Implemented Extras

1) Events filtering: by date, by query parameter t (future events, today's events, past events).
2) Unit tests added.
3) GitHub Actions pipeline added: basic_code_checks.yml
4) Logging added:
    - log everything to a default log file (env. variable $LOG_DEFAULT);
    - log failed login attempts to auth log file (env. variable $LOG_AUTH)


## How to Run the API on a Local Computer?

#### Step 1: Clone this repository to your local computer and install all project dependencies

cloning git repository:
```
git clone https://github.com/alv2017/Events-API.git
```
installing dependencies
```
pip install -r requirements-dev.txt
```

#### Step 2: Start Django development server

if migrations are not applied yet
```
python manage.py migrate
```

create superuser account (if it is not created yet)
```
python manage.py createsuperuser
```

start local development server
```
python manage.py runserver
```

It is also possible to run the api using gunicorn server
```
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --reload
```

#### Step 3: Use any API client to access the API endpoints.

#### Step 4: If you want to use Django Admin remember to collect static files

Create directory called *static*, and run the command to collect static files
```
python manage.py collectstatic
```


# How to Run a Local Development in Docker?

It is possible to run a local development environmen in a Docker container.

#### Step 1: Build the docker containers
```
docker compose build
```

#### Step2: Start the application
```
docker compose up
```

#### Step3: Stop the application
```
docker compose down
```