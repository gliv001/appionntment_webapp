PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE user_level (
	id INTEGER NOT NULL,
	level INTEGER,
	name VARCHAR(64),
	PRIMARY KEY (id),
	UNIQUE (level)
);
CREATE TABLE service (
	id INTEGER NOT NULL,
	name VARCHAR(64) NOT NULL,
	price NUMERIC(6, 2),
	PRIMARY KEY (id)
);
CREATE TABLE appointment_times (
	id INTEGER NOT NULL,
	timeslot DATETIME,
	PRIMARY KEY (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL,
	"userLevelId" INTEGER,
	email VARCHAR(64) NOT NULL,
	password VARCHAR(256) NOT NULL,
	name VARCHAR(64) NOT NULL,
	verified BOOLEAN,
	"creationDate" DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY("userLevelId") REFERENCES user_level (level),
	UNIQUE (email)
);
CREATE TABLE appointment (
	id INTEGER NOT NULL,
	client VARCHAR(64) NOT NULL,
	"serviceId" INTEGER,
	"employeeId" INTEGER,
	"apptDateTime" DATETIME,
	tips NUMERIC(6, 2),
	total NUMERIC(6, 2),
	PRIMARY KEY (id),
	CONSTRAINT _employee_appt_uc UNIQUE ("employeeId", "apptDateTime"),
	FOREIGN KEY("serviceId") REFERENCES service (id),
	FOREIGN KEY("employeeId") REFERENCES employees (id)
);
CREATE TABLE login_history (
	id INTEGER NOT NULL,
	"userId" INTEGER,
	email VARCHAR(64) NOT NULL,
	status VARCHAR(64) NOT NULL,
	"loginTime" DATETIME,
	PRIMARY KEY (id),
	FOREIGN KEY("userId") REFERENCES user (id)
);
CREATE VIEW Employees AS
SELECT ID,
	Name
FROM User
WHERE userLevelId = 2
	OR userLevelId = 3;
COMMIT;