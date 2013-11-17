INSERT INTO tuser(_1, _2, _3) VALUES ('francisco','francisco', 'Lyon');
INSERT INTO tuser(_1, _2, _3) VALUES ('matthew','matthew', 'Lyon');
INSERT INTO tuser(_1, _2, _3) VALUES ('nishara','nishara', 'Paris');
INSERT INTO tuser(_1, _2, _3) VALUES ('jorge','jorge', 'Paris');
INSERT INTO tuser(_1, _2, _3) VALUES ('manuel','manuel', 'Nantes');
INSERT INTO tuser(_1, _2, _3) VALUES ('caio','caio', 'Nantes');
INSERT INTO tuser(_1, _2, _3) VALUES ('user7','user7', 'geotag7');
INSERT INTO tuser(_1, _2, _3) VALUES ('user8','user8', 'geotag8');
INSERT INTO tuser(_1, _2, _3) VALUES ('user9','user9', 'geotag9');
INSERT INTO tuser(_1, _2, _3) VALUES ('user10','user10', 'geotag10');

INSERT INTO tweet(_1, _2, _3) VALUES ('working on ADB','2013-10-15 08:00:00',1);
INSERT INTO tweet(_1, _2, _3) VALUES ('@nishara yeah me too','2013-10-15 09:00:00',2);
INSERT INTO tweet(_1, _2, _3) VALUES ('Hello..how are you guys?','2013-10-16 08:00:00',3);
INSERT INTO tweet(_1, _2, _3) VALUES ('working on ADB','2013-10-16 10:00:00',4);
INSERT INTO tweet(_1, _2, _3) VALUES ('Feeling awesome..in #Nantes','2013-10-17 11:00:00',5);
INSERT INTO tweet(_1, _2, _3) VALUES ('@jorge Hellooo..','2013-10-17 14:00:00',3);
INSERT INTO tweet(_1, _2, _3) VALUES ('New to tweet','2013-10-18 09:00:00',6);
INSERT INTO tweet(_1, _2, _3) VALUES ('@user6 welcome to tweeter','2013-10-18 10:00:00',4);
INSERT INTO tweet(_1, _2, _3) VALUES ('Studying for the #exam.','2013-10-20 08:00:00',7);
INSERT INTO tweet(_1, _2, _3) VALUES ('I am on Twitter','2013-10-21 09:00:00',8);


INSERT INTO follower VALUES (1, 2);
INSERT INTO follower VALUES (1, 4);
INSERT INTO follower VALUES (1, 8);
INSERT INTO follower VALUES (2, 1);
INSERT INTO follower VALUES (2, 4);
INSERT INTO follower VALUES (4, 9);
INSERT INTO follower VALUES (2, 5);
INSERT INTO follower VALUES (3, 2);
INSERT INTO follower VALUES (3, 10);
INSERT INTO follower VALUES (6, 7);
INSERT INTO follower VALUES (8, 4);
INSERT INTO follower VALUES (5, 9);


INSERT INTO hashtag VALUES (1, 'Nantes');
INSERT INTO hashtag VALUES (2, 'exam');
INSERT INTO hashtag VALUES (3, 'project');

INSERT INTO tagintweet VALUES (1, 5);
INSERT INTO tagintweet VALUES (2, 9);

INSERT INTO mention VALUES (2, 1);
INSERT INTO mention VALUES (6, 2);
INSERT INTO mention VALUES (8, 6);



