# Appointment Webapp
Appointment webapp for learning to create a frontend page that allows the user to create appointments and storing it in the backend database

# Setup

## Environment
Make sure to setup the virtual environment and install the ```requirements.txt```

To do this follow the steps below:

``` $ virtualenv env ```

``` $ source env/bin/activate ```

``` $ pip install -r requirements.txt ```

## Backend database
To build the ```backend.db```:

``` $ python models.py ```

# Run Appointment Webapp
Once ```requirements.txt``` is installed and the database ```backend.db``` has been created, run the webapp:

``` $ python app.py ```

# Database Information
### Appointment Table
| AppointmentID | ClientName  | ServiceID | EmployeeID | Appointment | Tips          | Total         |
|---------------|-------------|-----------|------------|-------------|---------------|---------------|
| int           | varchar(64) | int       | int        | datetime    | decimal(10,2) | decimal(10,2) |

### Employee Table
| EmployeeID | Name         |
|------------|--------------|
| int        | varchar(64)  |

### Service Table
| ServiceID | Name        | Pricing       |
|-----------|-------------|---------------|
| int       | varchar(64) | decimal(10,2) |

## Frontend pages
### Appointment
TODO

### Employees
TODO

### Services
TODO

