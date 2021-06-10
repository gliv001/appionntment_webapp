# Appointment Webapp

Appointment webapp for learning to create a frontend page that allows the user to create appointments and storing it in the backend database

# Setup

## Requirements

Python 3.9.4

virtualenv, if not installed run below command to install:

`$ pip install virtualenv`

## Database

Create a new postgres database then go ahead and dump the `postgresDb.sql` into that database to initialize it.

`$ psql apptDb < postgresDb.sql`

Also remember to set your environment variable correctly for the database

`export SQLALCHEMY_DATABASE_URI=postgresql://postgres:georgeliv@test/apptDb`

## Installation

Make sure to setup the virtual environment and install the `requirements.txt`

To do this follow the steps below:

`$ virtualenv env`

`$ source env/bin/activate`

`$ pip install -r requirements.txt`

## Configuration

Setup a configuration file `.envrc` that will add environment variables that will be used in the webapp, take a look at `.envrc_dummy` for an example.

I used `direnv` ([link](https://direnv.net/)) to load the `.envrc` to the environment when in the webapp root directory, example with direnv:

```
$ cd ~/path/to/appointment_webapp/
direnv: loading ~/path/to/appointment_webapp/.envrc
direnv: export +ACCOUNT_EXPIRE_VERIFY_TIME +ADMIN_EMAIL +ADMIN_PASS +DB_NAME +MAIL_PASSWORD +MAIL_PORT +MAIL_SERVER +MAIL_USERNAME +MAIL_USE_SSL +MAIL_USE_TSL +SECRET_KEY +SQLALCHEMY_DATABASE_URI +SQLALCHEMY_TRACK_MODIFICATIONS
```

## Email Setup

Setup an email to allow you to send emails, then add your email configurations in the `.envrc`:

```
export MAIL_SERVER=smtp.gmail.com
export MAIL_USERNAME=dummy@gmail.com
export MAIL_PASSWORD=dummy_password
export MAIL_PORT=465
export MAIL_USE_SSL=True
export MAIL_USE_TSL=False
```

# Run Appointment Webapp

run the webapp:

`$ cd ~/path/to/appointment_webapp`

`$ python main.py`

# Troubleshoot

If getting issues with postgres on Mac M1 chip use this [link](https://github.com/psycopg/psycopg2/issues/1216#issuecomment-767892042)
