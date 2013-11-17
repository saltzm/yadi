CREATE DATABASE "Cinema" ;

CREATE TABLE movie (
    _0 character varying(30) PRIMARY KEY,
    _1 character varying(30) NOT NULL,
    _2 bigint NOT NULL,
    _3 bigint
);

CREATE TABLE featuring (
    _0 character varying(30) NOT NULL,
    _1 character varying(30) NOT NULL,
    _2 character varying(15) NOT NULL,
    PRIMARY KEY(_0,_1)
);


INSERT INTO movie VALUES ('Home Alone', 'Chris Columbus', 103, 1990);
INSERT INTO movie VALUES ('Life Is Beautiful', 'Roberto Benigni', 116, 1997);
INSERT INTO movie VALUES ('Casino', 'Martin Scorsese', 178, 1995);
INSERT INTO movie VALUES ('Toy Story', 'John Lasseter', 81, 1995);
INSERT INTO movie VALUES ('No Country for Old Men', 'Ethan Coen', 122, 2007);


INSERT INTO featuring VALUES ('Home Alone', 'Macaulay Culkin', 'Kevin');
INSERT INTO featuring VALUES ('Life Is Beautiful', 'Roberto Benigni', 'Guido');
INSERT INTO featuring VALUES ('Casino', 'Robert De Niro', 'Sam');
INSERT INTO featuring VALUES ('Toy Story', 'Hom Hanks', 'Woody');
INSERT INTO featuring VALUES ('No Country for Old Men', 'Tommy Lee Jones', 'Ed Tom Bell');
