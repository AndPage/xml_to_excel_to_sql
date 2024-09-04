DROP TABLE if EXISTS Buchtitel;
CREATE TABLE Buchtitel
(
	Buchtitel_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Buch_Name VARCHAR(50) NOT NULL
);

DROP TABLE if EXISTS Autor;
CREATE TABLE Autor
(
	Autor_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Name VARCHAR(50) NOT NULL,
	Vorname VARCHAR(50) NOT NULL
);

DROP TABLE if EXISTS Edition_Historie;
CREATE TABLE Edition_Historie
(
	Edition_Historie_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Bezeichnung_Edition VARCHAR(50)
);

DROP TABLE if EXISTS tb_human;
CREATE TABLE tb_human
(
	human_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	create_at DATE,
	modify_at DATE,
	name VARCHAR(50) NOT NULL,
	first_name VARCHAR(50) NOT NULL,
	birthday INTEGER,
	postal_code VARCHAR(10),
	percent REAL
);

DROP TABLE if EXISTS Verlag;
CREATE TABLE Verlag
(
	Verlag_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Verlag VARCHAR(50)
);

DROP TABLE if EXISTS Abteilung;
CREATE TABLE Abteilung
(
	Abteilung_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Abteilungsbezeichnung VARCHAR(50),
	Abteilungsmanager VARCHAR(50),
	Abteilungsbudget VARCHAR(50)
);

DROP TABLE if EXISTS Mahnstufe;
CREATE TABLE Mahnstufe
(
	Mahnstufe_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Mahnstufe VARCHAR(50)
);

DROP TABLE if EXISTS Genre;
CREATE TABLE Genre
(
	Genre_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Genre_Name VARCHAR(50) NOT NULL
);

DROP TABLE if EXISTS Schlagwort;
CREATE TABLE Schlagwort
(
	Schlagwort_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Schlagwort VARCHAR(50)
);

DROP TABLE if EXISTS Edition_Typ;
CREATE TABLE Edition_Typ
(
	Edition_Typ_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Bezeichnung_Typ VARCHAR(50)
);

DROP TABLE if EXISTS Schlagwort_Buchtitel;
CREATE TABLE Schlagwort_Buchtitel
(
	Schlagwort_Buchtitel_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Buchtitel_ID INTEGER NOT NULL,
	Schlagwort_ID INTEGER NOT NULL,
	FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel(Buchtitel_ID),
	FOREIGN KEY (Schlagwort_ID) REFERENCES Schlagwort(Schlagwort_ID)
);

DROP TABLE if EXISTS Kundentyp;
CREATE TABLE Kundentyp
(
	Kundentyp_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Mahnstufe_ID INTEGER NOT NULL,
	Typbezeichnung VARCHAR(50),
	Leihfrist VARCHAR(50),
	Ausleihlimit VARCHAR(50),
	Mahngebühren pro Tag VARCHAR(50),
	Mahndauer VARCHAR(50),
	FOREIGN KEY (Mahnstufe_ID) REFERENCES Mahnstufe(Mahnstufe_ID)
);

DROP TABLE if EXISTS Edition_Zusammenfassung;
CREATE TABLE Edition_Zusammenfassung
(
	Edition_Zusammenfassung_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	ISBN VARCHAR(50),
	Buchtitel_ID INTEGER NOT NULL,
	Edition_Typ_ID INTEGER NOT NULL,
	Edition_Historie_ID INTEGER NOT NULL,
	FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel(Buchtitel_ID),
	FOREIGN KEY (Edition_Typ_ID) REFERENCES Edition_Typ(Edition_Typ_ID),
	FOREIGN KEY (Edition_Historie_ID) REFERENCES Edition_Historie(Edition_Historie_ID)
);

DROP TABLE if EXISTS Autor_Buchtitel;
CREATE TABLE Autor_Buchtitel
(
	Autor_Buchtitel_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Buchtitel_ID INTEGER NOT NULL,
	Autor_ID INTEGER NOT NULL,
	FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel(Buchtitel_ID),
	FOREIGN KEY (Autor_ID) REFERENCES Autor(Autor_ID)
);

DROP TABLE if EXISTS Autor_Kontaktadresse;
CREATE TABLE Autor_Kontaktadresse
(
	Autor_Kontaktadresse_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Autor_ID INTEGER NOT NULL,
	Name VARCHAR(50) NOT NULL,
	Vorname VARCHAR(50) NOT NULL,
	Straße VARCHAR(50),
	Hausnr VARCHAR(50),
	PLZ VARCHAR(50),
	Ort VARCHAR(50),
	FOREIGN KEY (Autor_ID) REFERENCES Autor(Autor_ID)
);

DROP TABLE if EXISTS Genre_Buchtitel;
CREATE TABLE Genre_Buchtitel
(
	Buchtitel_ID INTEGER NOT NULL,
	Genre_ID INTEGER NOT NULL,
	PRIMARY KEY (Buchtitel_ID, Genre_ID),
	FOREIGN KEY (Buchtitel_ID) REFERENCES Buchtitel(Buchtitel_ID),
	FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);

DROP TABLE if EXISTS Mitarbeiter;
CREATE TABLE Mitarbeiter
(
	Mitarbeiter_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Abteilung_ID INTEGER NOT NULL,
	human_id INTEGER NOT NULL,
	Name VARCHAR(50) NOT NULL,
	Vorname VARCHAR(50) NOT NULL,
	Geburtsdatum VARCHAR(50),
	Straße VARCHAR(50),
	Hausnr VARCHAR(50),
	PLZ VARCHAR(50),
	Ort VARCHAR(50),
	asdfg VARCHAR(50),
	Gehalt VARCHAR(50),
	vorgesetzter_Mitarbeiter_id INTEGER NOT NULL,
	FOREIGN KEY (Abteilung_ID) REFERENCES Abteilung(Abteilung_ID),
	FOREIGN KEY (human_id) REFERENCES tb_human(human_id),
	FOREIGN KEY (vorgesetzter_Mitarbeiter_id) REFERENCES Mitarbeiter(Mitarbeiter_ID)
);

DROP TABLE if EXISTS Kunde;
CREATE TABLE Kunde
(
	Kunde_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Kundentyp_ID INTEGER NOT NULL,
	human_id INTEGER NOT NULL,
	Name VARCHAR(50) NOT NULL,
	Vorname VARCHAR(50) NOT NULL,
	Geburtsdatum VARCHAR(50),
	Straße VARCHAR(50),
	Hausnr VARCHAR(50),
	PLZ VARCHAR(50),
	Ort VARCHAR(50),
	Ausweisnummer VARCHAR(50),
	Kontostand VARCHAR(50),
	FOREIGN KEY (Kundentyp_ID) REFERENCES Kundentyp(Kundentyp_ID),
	FOREIGN KEY (human_id) REFERENCES tb_human(human_id)
);

DROP TABLE if EXISTS Verlag_Edition_Zusammenfassung;
CREATE TABLE Verlag_Edition_Zusammenfassung
(
	Verlag_Edition_Zusammenfassung_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Edition_Zusammenfassung_ID INTEGER NOT NULL,
	Verlag_ID INTEGER NOT NULL,
	FOREIGN KEY (Edition_Zusammenfassung_ID) REFERENCES Edition_Zusammenfassung(Edition_Zusammenfassung_ID),
	FOREIGN KEY (Verlag_ID) REFERENCES Verlag(Verlag_ID)
);

DROP TABLE if EXISTS Vertretung;
CREATE TABLE Vertretung
(
	Vertretung_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Vertreter_Mitarbeiter_ID INTEGER NOT NULL,
	Vertretener_Mitarbeiter_ID INTEGER NOT NULL,
	Von VARCHAR(50),
	Bis VARCHAR(50),
	Vertretungsgrund VARCHAR(50),
	FOREIGN KEY (Vertreter_Mitarbeiter_ID) REFERENCES Mitarbeiter(Mitarbeiter_ID),
	FOREIGN KEY (Vertretener_Mitarbeiter_ID) REFERENCES Mitarbeiter(Mitarbeiter_ID)
);

DROP TABLE if EXISTS Exemplar;
CREATE TABLE Exemplar
(
	Exemplar_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Zustand	 VARCHAR(50),
	Anschaffungsdatum VARCHAR(50)
);

DROP TABLE if EXISTS Ausleihe;
CREATE TABLE Ausleihe
(
	Ausleihe_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Kunde_ID INTEGER NOT NULL,
	Mitarbeiter_ID INTEGER NOT NULL,
	Ausleihdatum VARCHAR(50),
	FOREIGN KEY (Kunde_ID) REFERENCES Kunde(Kunde_ID),
	FOREIGN KEY (Mitarbeiter_ID) REFERENCES Mitarbeiter(Mitarbeiter_ID)
);

DROP TABLE if EXISTS Ausleihposition;
CREATE TABLE Ausleihposition
(
	Ausleihposition_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Exemplar_ID INTEGER NOT NULL,
	Ausleihe_ID INTEGER NOT NULL,
	zurueckgegeben_at DATE,
	FOREIGN KEY (Exemplar_ID) REFERENCES Exemplar(Exemplar_ID),
	FOREIGN KEY (Ausleihe_ID) REFERENCES Ausleihe(Ausleihe_ID)
);

DROP TABLE if EXISTS Mahnung;
CREATE TABLE Mahnung
(
	Mahnung_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	Ausleihposition_ID INTEGER NOT NULL,
	Mahnstufe_ID INTEGER NOT NULL,
	Sendedatum VARCHAR(50),
	FOREIGN KEY (Ausleihposition_ID) REFERENCES Ausleihposition(Ausleihposition_ID),
	FOREIGN KEY (Mahnstufe_ID) REFERENCES Mahnstufe(Mahnstufe_ID)
);
