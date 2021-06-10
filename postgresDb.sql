--
-- PostgreSQL database init
--
CREATE TABLE IF NOT EXISTS user_level (
    id serial PRIMARY KEY,
    ulevel bigint,
    uname character varying(64),
    UNIQUE (ulevel)
);
CREATE TABLE IF NOT EXISTS services (
    id serial PRIMARY KEY,
    sname character varying(64) NOT NULL,
    price numeric(6, 2)
);
CREATE TABLE IF NOT EXISTS appt_users (
    id serial PRIMARY KEY,
    userlevelid bigint REFERENCES user_level(ulevel),
    email character varying(64) NOT NULL,
    upassword character varying(256) NOT NULL,
    uname character varying(64) NOT NULL,
    verified boolean,
    creationdate timestamp without time zone,
    UNIQUE (email)
);
CREATE TABLE IF NOT EXISTS appointments (
    id serial PRIMARY KEY,
    client character varying(64) NOT NULL,
    serviceid bigint,
    employeeid bigint,
    apptdatetime timestamp without time zone,
    tips numeric(6, 2),
    total numeric(6, 2),
    CONSTRAINT fk_employee_id FOREIGN KEY(employeeid) REFERENCES appt_users(id),
    CONSTRAINT fk_service_id FOREIGN KEY(serviceid) REFERENCES services(id)
);
CREATE TABLE IF NOT EXISTS login_history (
    id serial PRIMARY KEY,
    userid bigint,
    email character varying(64) NOT NULL,
    loginstatus character varying(64) NOT NULL,
    logintime timestamp without time zone,
    CONSTRAINT fk_user_id FOREIGN KEY(userid) REFERENCES appt_users(id)
);
CREATE OR REPLACE VIEW employees AS
SELECT id,
    uname
FROM appt_users
WHERE userlevelid >= 2;