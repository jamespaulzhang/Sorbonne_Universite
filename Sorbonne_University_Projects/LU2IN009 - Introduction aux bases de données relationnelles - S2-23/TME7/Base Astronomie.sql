drop all objects;

CREATE TABLE Categorie (
  idC NUMBER(10) PRIMARY KEY,
  nom Varchar2(15) NOT NULL
);
 
INSERT INTO Categorie VALUES (10,'étoile');
INSERT INTO Categorie VALUES (11,'planète');
INSERT INTO Categorie VALUES (12,'satellite');
 
CREATE TABLE Astre (
  idA NUMBER(10) PRIMARY KEY,
  nom Varchar2(15) NOT NULL,
  rayon NUMBER(10) NOT NULL,
  idC NUMBER(10) NOT NULL REFERENCES Categorie(idC)
);
-- rayon en km
INSERT INTO Astre VALUES (100,'Soleil',696342, (SELECT idC FROM Categorie WHERE nom='étoile'));
INSERT INTO Astre VALUES (101,'Terre',   6371, (SELECT idC FROM Categorie WHERE nom='planète'));
INSERT INTO Astre VALUES (102,'Lune',    1737, (SELECT idC FROM Categorie WHERE nom='satellite'));
INSERT INTO Astre VALUES (103,'Mars',    3390, (SELECT idC FROM Categorie WHERE nom='planète'));
 
 
CREATE TABLE TourneAutour (
  idA1 NUMBER(10) PRIMARY KEY REFERENCES Astre (idA),
  idA2 NUMBER(10)  NOT NULL REFERENCES Astre (idA),
  POSITION NUMBER(3) NOT NULL
);
 
INSERT INTO TourneAutour VALUES (101,100,3);
INSERT INTO TourneAutour VALUES (102,101,1);
INSERT INTO TourneAutour VALUES (103,100,4);
 
CREATE TABLE Observation (
  idO NUMBER(10),
  idA NUMBER(10) NOT NULL,
  dateObs DATE,
  valObs NUMBER(5),
  CONSTRAINT pk PRIMARY KEY(idO),
  CONSTRAINT fk FOREIGN KEY(idA) REFERENCES Astre (idA),
  CONSTRAINT ck CHECK ( valObs BETWEEN 100 AND 20000)
);
 
 
-- Solution H2 yyyy-MM-dd
INSERT INTO Observation VALUES (90,100,'2010-05-10',12001);
INSERT INTO Observation VALUES (91,100,'2010-05-10',12003);
INSERT INTO Observation VALUES (92,101,'2013-12-18',8005);
INSERT INTO Observation VALUES (93,102,'2014-08-27',3007);
