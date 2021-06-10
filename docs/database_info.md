# Database Information

### Appointment Table

| id  | Client      | ServiceID | EmployeeID | AppotDateTime | Tips          | Total         |
| --- | ----------- | --------- | ---------- | ------------- | ------------- | ------------- |
| int | varchar(64) | int       | int        | datetime      | decimal(10,2) | decimal(10,2) |

### ApptUsers Table

| id  | Userlevelid | Email       | Password     | Name        | Verified | Creationdate |
| --- | ----------- | ----------- | ------------ | ----------- | -------- | ------------ |
| int | int         | varchar(64) | varchar(256) | varchar(64) | boolean  | datetime     |

### User_Level Table

| id  | level | name        |
| --- | ----- | ----------- |
| int | int   | varchar(64) |

### Service Table

| id  | Name        | Pricing       |
| --- | ----------- | ------------- |
| int | varchar(64) | decimal(10,2) |

### Login_History Table

| id  | Userid | Email       | Status      | Logintime |
| --- | ------ | ----------- | ----------- | --------- |
| int | int    | varchar(64) | varchar(64) | datetime  |

### Employee View

| id  | Name        |
| --- | ----------- |
| int | varchar(64) |

## Frontend pages

### Appointment

TODO

### Employees

TODO

### Services

TODO
