CREATE TABLE Ogloszenia (
    id uuid  NOT NULL DEFAULT gen_random_uuid(),
    tytul text  NOT NULL,
    tresc text  NOT NULL,
    Uzytkownik_id uuid  NOT NULL,
    Zwierzeta_id uuid  NOT NULL,
    CONSTRAINT Ogloszenia_pk PRIMARY KEY (id)
);


CREATE TABLE Uzytkownik (
    id uuid  NOT NULL DEFAULT gen_random_uuid(),
    email text  NOT NULL,
    password text  NOT NULL,
    CONSTRAINT Uzytkownik_pk PRIMARY KEY (id)
);


CREATE TABLE Zwierzeta (
    id uuid  NOT NULL DEFAULT gen_random_uuid(),
    imie text  NOT NULL,
    typ text  NOT NULL,
    Uzytkownik_id uuid  NOT NULL,
    CONSTRAINT Zwierzeta_pk PRIMARY KEY (id)
);


ALTER TABLE Ogloszenia ADD CONSTRAINT Ogloszenia_Uzytkownik
    FOREIGN KEY (Uzytkownik_id)
    REFERENCES Uzytkownik (id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;


ALTER TABLE Ogloszenia ADD CONSTRAINT Ogloszenia_Zwierzeta
    FOREIGN KEY (Zwierzeta_id)
    REFERENCES Zwierzeta (id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;


ALTER TABLE Zwierzeta ADD CONSTRAINT Zwierzeta_Uzytkownik
    FOREIGN KEY (Uzytkownik_id)
    REFERENCES Uzytkownik (id)
    NOT DEFERRABLE
    INITIALLY IMMEDIATE
;

