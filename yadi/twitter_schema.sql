CREATE Database twitter;

CREATE SEQUENCE u_id_seq;

CREATE TABLE IF NOT EXISTS tuser
(
  _0 bigint PRIMARY KEY default nextval('u_id_seq'),   
  _1 character varying(30) UNIQUE NOT NULL,
  _2 character varying(10) NOT NULL,
  _3 character varying(15) NOT NULL
);

CREATE SEQUENCE t_id_seq;

CREATE TABLE  IF NOT EXISTS tweet
(
  _0 bigint PRIMARY KEY default nextval('t_id_seq'),
  _1 character varying(80),
  _2 timestamp(2) without time zone,
  _3 bigint REFERENCES tuser (_0),
  CONSTRAINT datetime_constraint CHECK (_2 < now())
);


CREATE TABLE  IF NOT EXISTS hashTag
(
  _0 bigserial PRIMARY KEY,
  _1 character varying(50) UNIQUE NOT NULL
);

CREATE TABLE  IF NOT EXISTS taginTweet
(
  _0 bigint NOT NULL REFERENCES hashTag (_0),
  _1 bigint NOT NULL REFERENCES tweet (_0),
  PRIMARY KEY(_0,_1)
);


CREATE TABLE  IF NOT EXISTS mention
(
  _0 bigint NOT NULL REFERENCES tweet (_0),
  _1 bigint NOT NULL REFERENCES tuser (_0),
  PRIMARY KEY(_0,_1)  
);


CREATE TABLE  IF NOT EXISTS follower
(
  _0 bigint NOT NULL REFERENCES tuser (_0),
  _1 bigint NOT NULL REFERENCES tuser (_0),
  PRIMARY KEY(_0,_1)
);
