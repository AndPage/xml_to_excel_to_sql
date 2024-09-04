CREATE TABLE Autor
(
    Autor_ID INTEGER AUTOINCREMENT NOT NULL,
    Name     VARCHAR(50)           NOT NULL,
    Vorname  VARCHAR(50)           NOT NULL,
    PRIMARY KEY (Autor_ID)
);

CREATE TABLE Buchtitel
(
    Buchtitel_ID INTEGER AUTOINCREMENT NOT NULL,
    Buch_Name    VARCHAR(50)           NOT NULL,
    PRIMARY KEY (Buchtitel_ID)
);

CREATE TABLE Mensch
(
    UniqueID VARCHAR(50),
    Row 1 VARCHAR(50),
    Row 2 VARCHAR(50),
    Row 3 VARCHAR(50),
    PRIMARY KEY (UniqueID)
);

CREATE TABLE Edition_Historie
(
    Edition_Historie_ID INTEGER AUTOINCREMENT NOT NULL,
    Bezeichnung_Edition VARCHAR(50),
    PRIMARY KEY (Edition_Historie_ID)
);

CREATE TABLE Verlag
(
    Verlag_ID INTEGER AUTOINCREMENT NOT NULL,
    Verlag    VARCHAR(50),
    PRIMARY KEY (Verlag_ID)
);

CREATE TABLE Abteilung
(
    Abteilung_ID          INTEGER AUTOINCREMENT NOT NULL,
    Abteilungsbezeichnung VARCHAR(50),
    Abteilungsmanager     VARCHAR(50),
    Abteilungsbudget      VARCHAR(50),
    PRIMARY KEY (Abteilung_ID)
);

CREATE TABLE Mahnstufen
(
    Mahnstufen_ID INTEGER AUTOINCREMENT NOT NULL,
    Mahnstufen    VARCHAR(50),
    PRIMARY KEY (Mahnstufen_ID)
);

CREATE TABLE Genre
(
    Genre_ID   INTEGER AUTOINCREMENT NOT NULL,
    Genre_Name VARCHAR(50)           NOT NULL,
    PRIMARY KEY (Genre_ID)
);

CREATE TABLE Schlagwort
(
    Schlagwort_ID INTEGER AUTOINCREMENT NOT NULL,
    Schlagwort    VARCHAR(50),
    PRIMARY KEY (Schlagwort_ID)
);

CREATE TABLE Edition_Typ
(
    Edition_Typ_ID  INTEGER AUTOINCREMENT NOT NULL,
    Bezeichnung_Typ VARCHAR(50),
    PRIMARY KEY (Edition_Typ_ID)
);

CREATE TABLE Schlagwort_Buchtitel
(
    Schlagwort_Buchtitel_ID INTEGER AUTOINCREMENT NOT NULL,
    Buchtitel_ID            INTEGER,
    Schlagwort_ID           INTEGER,
    PRIMARY KEY (Schlagwort_Buchtitel_ID),
    FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel (Buchtitel_ID),
    FOREIGN KEY (Schlagwort_ID) REFERENCES Schlagwort (Schlagwort_ID)
);

CREATE TABLE Kundentyp
(
    Kundentyp_ID   INTEGER AUTOINCREMENT NOT NULL,
    Mahnstufen_ID  INTEGER,
    Typbezeichnung VARCHAR(50),
    Leihfrist      VARCHAR(50),
    Ausleihlimit   VARCHAR(50),
    Mahngebühren   pro Tag VARCHAR(50),
    Mahndauer      VARCHAR(50),
    PRIMARY KEY (Kundentyp_ID),
    FOREIGN KEY (Mahnstufen_ID) REFERENCES Mahnstufen (Mahnstufen_ID)
);

CREATE TABLE Autor_Buchtitel
(
    Autor_Buchtitel_ID INTEGER AUTOINCREMENT NOT NULL,
    Buchtitel_ID       INTEGER,
    Autor_ID           INTEGER,
    PRIMARY KEY (Autor_Buchtitel_ID),
    FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel (Buchtitel_ID),
    FOREIGN KEY (Autor_ID) REFERENCES Autor (Autor_ID)
);

CREATE TABLE Edition_Zusammenfassung
(
    Edition_Zusammenfassung_ID INTEGER AUTOINCREMENT NOT NULL,
    ISBN                       VARCHAR(50),
    Buchtitel_ID               INTEGER,
    Edition_Typ_ID             INTEGER,
    Edition_Historie_ID        INTEGER,
    PRIMARY KEY (Edition_Zusammenfassung_ID),
    FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel (Buchtitel_ID),
    FOREIGN KEY (Edition_Typ_ID) REFERENCES Edition_Typ (Edition_Typ_ID),
    FOREIGN KEY (Edition_Historie_ID) REFERENCES Edition_Historie (Edition_Historie_ID)
);

CREATE TABLE Genre_Buchtitel
(
    Genre_Buchtitel_ID INTEGER AUTOINCREMENT NOT NULL,
    Buchtitel_ID       INTEGER,
    Genre_ID           INTEGER,
    PRIMARY KEY (Genre_Buchtitel_ID),
    FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel (Buchtitel_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre (Genre_ID)
);

CREATE TABLE Autor_Kontaktadresse
(
    Autor_Kontaktadresse_ID INTEGER AUTOINCREMENT NOT NULL,
    Autor_ID                INTEGER,
    Name                    VARCHAR(50)           NOT NULL,
    Vorname                 VARCHAR(50)           NOT NULL,
    Straße                  VARCHAR(50),
    Hausnr                  VARCHAR(50),
    PLZ                     VARCHAR(50),
    Ort                     VARCHAR(50),
    PRIMARY KEY (Autor_Kontaktadresse_ID),
    FOREIGN KEY (Autor_ID) REFERENCES Autor (Autor_ID)
);

CREATE TABLE Mitarbeiter
(
    Mitarbeiter_ID              INTEGER AUTOINCREMENT NOT NULL,
    Abteilung_ID                INTEGER,
    Name                        VARCHAR(50)           NOT NULL,
    Vorname                     VARCHAR(50)           NOT NULL,
    Geburtsdatum                VARCHAR(50),
    Straße                      VARCHAR(50),
    Hausnr                      VARCHAR(50),
    PLZ                         VARCHAR(50),
    Ort                         VARCHAR(50),
    asdfg                       VARCHAR(50),
    Gehalt                      VARCHAR(50),
    Mitarbeiter_id_vorgesetzter VARCHAR(50),
    PRIMARY KEY (Mitarbeiter_ID),
    FOREIGN KEY (Abteilung_ID) REFERENCES Abteilung (Abteilung_ID),
    FOREIGN KEY (Mitarbeiter_id_vorgesetzter) REFERENCES Mitarbeiter (Mitarbeiter_ID)
);

CREATE TABLE Kunde
(
    Kunde_ID      INTEGER AUTOINCREMENT NOT NULL,
    Kundentyp_ID  INTEGER,
    Name          VARCHAR(50)           NOT NULL,
    Vorname       VARCHAR(50)           NOT NULL,
    Geburtsdatum  VARCHAR(50),
    Straße        VARCHAR(50),
    Hausnr        VARCHAR(50),
    PLZ           VARCHAR(50),
    Ort           VARCHAR(50),
    Ausweisnummer VARCHAR(50),
    Kontostand    VARCHAR(50),
    PRIMARY KEY (Kunde_ID),
    FOREIGN KEY (Kundentyp_ID) REFERENCES Kundentyp (Kundentyp_ID)
);

CREATE TABLE Verlag_Edition_Zusammenfassung
(
    Verlag_Edition_Zusammenfassung_ID INTEGER AUTOINCREMENT NOT NULL,
    Edition_Zusammenfassung_ID        INTEGER,
    Verlag_ID                         INTEGER,
    PRIMARY KEY (Verlag_Edition_Zusammenfassung_ID),
    FOREIGN KEY (Edition_Zusammenfassung_ID) REFERENCES Edition_Zusammenfassung (Edition_Zusammenfassung_ID),
    FOREIGN KEY (Verlag_ID) REFERENCES Verlag (Verlag_ID)
);

CREATE TABLE Vertretung
(
    Vertretung_ID              INTEGER AUTOINCREMENT NOT NULL,
    Mitarbeiter_ID_Vertreter   VARCHAR(50),
    Mitarbeiter_ID_Vertretener VARCHAR(50),
    Von                        VARCHAR(50),
    Bis                        VARCHAR(50),
    Vertretungsgrund           VARCHAR(50),
    PRIMARY KEY (Vertretung_ID),
    FOREIGN KEY (Mitarbeiter_ID_Vertreter) REFERENCES Mitarbeiter (Mitarbeiter_ID),
    FOREIGN KEY (Mitarbeiter_ID_Vertretener) REFERENCES Mitarbeiter (Mitarbeiter_ID)
);

CREATE TABLE Exemplar
(
    Exemplar_ID       INTEGER AUTOINCREMENT NOT NULL,
    Zustand           VARCHAR(50),
    Anschaffungsdatum VARCHAR(50),
    PRIMARY KEY (Exemplar_ID)
);

CREATE TABLE Ausleihe
(
    Ausleihe_ID    INTEGER AUTOINCREMENT NOT NULL,
    Kunde_ID       INTEGER,
    Mitarbeiter_ID INTEGER,
    Ausleihdatum   VARCHAR(50),
    PRIMARY KEY (Ausleihe_ID),
    FOREIGN KEY (Kunde_ID) REFERENCES Kunde (Kunde_ID),
    FOREIGN KEY (Mitarbeiter_ID) REFERENCES Mitarbeiter (Mitarbeiter_ID)
);

CREATE TABLE Ausleihposition
(
    Ausleihposition_ID INTEGER AUTOINCREMENT NOT NULL,
    Exemplar_ID        INTEGER,
    Ausleihe_ID        INTEGER,
    zurueckgegeben_am  VARCHAR(50),
    PRIMARY KEY (Ausleihposition_ID),
    FOREIGN KEY (Exemplar_ID) REFERENCES Exemplar (Exemplar_ID),
    FOREIGN KEY (Ausleihe_ID) REFERENCES Ausleihe (Ausleihe_ID)
);

CREATE TABLE Mahnung
(
    Mahnung_ID         INTEGER AUTOINCREMENT NOT NULL,
    Ausleihposition_ID INTEGER,
    Mahnstufe_ID       INTEGER,
    Sendedatum         VARCHAR(50),
    PRIMARY KEY (Mahnung_ID),
    FOREIGN KEY (Ausleihposition_ID) REFERENCES Ausleihposition (Ausleihposition_ID),
    FOREIGN KEY (Mahnstufe_ID) REFERENCES X
);
