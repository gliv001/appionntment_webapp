# Appointment Webapp
Appointment webapp for learning to create a frontend page that allows the user to create appointments and storing it in the backend database

# Backend database tables
To build the backend.db:

``` $ python models.py ```

## Appointment Table
| AppointmentID | ClientName  | ServiceID | EmployeeID | Appointment | Tips          | Total         |
|---------------|-------------|-----------|------------|-------------|---------------|---------------|
| int           | varchar(64) | int       | int        | datetime    | decimal(10,2) | decimal(10,2) |

## Employee Table
| EmployeeID | Name         |
|------------|--------------|
| int        | varchar(64)  |

## Service Table
| ServiceID | Name        | Pricing       |
|-----------|-------------|---------------|
| int       | varchar(64) | decimal(10,2) |

# Frontend pages
## Appointment
TODO

## Employees
TODO

## Services
TODO

