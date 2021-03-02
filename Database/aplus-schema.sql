USE aplus;


DROP TABLE IF EXISTS courses CASCADE;
CREATE TABLE courses (
    CRN         INT,
    Subject     VARCHAR (255),
    Course      VARCHAR (255),
    Section     INT,
    Title       VARCHAR (255),
    Days        VARCHAR (255),
    Time        VARCHAR (255),
    Instructors VARCHAR (255),
    Type        VARCHAR (255),
    Seats       INT,
    Enrollment  INT
);

DROP TABLE IF EXISTS pre_courses CASCADE;
CREATE TABLE pre_courses (
    CRN         INT,
    Subject     VARCHAR (255),
    Course      VARCHAR (255),
    Section     INT,
    Title       VARCHAR (255),
    Days        VARCHAR (255),
    Time        VARCHAR (255),
    Instructors VARCHAR (255),
    Type        VARCHAR (255),
    Seats       INT,
    Enrollment  INT
);


DROP TABLE IF EXISTS account CASCADE;
CREATE TABLE account (
	name         VARCHAR (255),
	email     VARCHAR (255),
	id			VARCHAR (255),
	year		VARCHAR (255),
	password      VARCHAR (255),
	userType     VARCHAR (1)
);

DROP TABLE IF EXISTS wishlist CASCADE;
CREATE TABLE wishlist (
	email         VARCHAR (255),
	wish      INT
);

DROP TABLE IF EXISTS courselist CASCADE;
CREATE TABLE courselist (
    email         VARCHAR (255),
    course      INT
);

