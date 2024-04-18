-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-04-18 22:09:38.451

-- tables
-- Table: Address
CREATE TABLE Address (
    id_address int  NOT NULL,
    street varchar(50)  NOT NULL,
    house_number varchar(5)  NOT NULL,
    zip_code varchar(6)  NOT NULL,
    city varchar(50)  NOT NULL,
    additional_info varchar(50)  NULL,
    CONSTRAINT Address_pk PRIMARY KEY (id_address)
);

-- Table: Client
CREATE TABLE Client (
    id_client int  NOT NULL,
    username varchar(50)  NOT NULL,
    name varchar(50)  NOT NULL,
    surname varchar(50)  NOT NULL,
    pesel varchar(11)  NOT NULL,
    id_clients_mailing_address int  NOT NULL,
    email varchar(50)  NOT NULL,
    password text  NOT NULL,
    CONSTRAINT Client_pk PRIMARY KEY (id_client)
);

-- Table: Comment
CREATE TABLE Comment (
    id_comment int  NOT NULL,
    text text  NOT NULL,
    date_created timestamp  NOT NULL,
    id_post int  NOT NULL,
    id_author int  NOT NULL,
    CONSTRAINT Comment_pk PRIMARY KEY (id_comment)
);

-- Table: Meter
CREATE TABLE Meter (
    id_meter int  NOT NULL,
    id_owner int  NOT NULL,
    id_meters_place_address int  NOT NULL,
    ranking_points int  NOT NULL,
    CONSTRAINT Meter_pk PRIMARY KEY (id_meter)
);

-- Table: Offer
CREATE TABLE Offer (
    id_offer int  NOT NULL,
    name varchar(50)  NOT NULL,
    tarrif varchar(50)  NOT NULL,
    pv_installation char(1)  NOT NULL,
    CONSTRAINT Offer_pk PRIMARY KEY (id_offer)
);

-- Table: OfferForMeter
CREATE TABLE OfferForMeter (
    id_offer_for_meter int  NOT NULL,
    id_offers_type int  NOT NULL,
    id_meter int  NOT NULL,
    start_date date  NOT NULL,
    end_date date  NULL,
    CONSTRAINT OfferForMeter_pk PRIMARY KEY (id_offer_for_meter)
);

-- Table: Post
CREATE TABLE Post (
    id_post int  NOT NULL,
    text text  NOT NULL,
    date_created timestamp  NOT NULL,
    id_author int  NOT NULL,
    CONSTRAINT Post_pk PRIMARY KEY (id_post)
);

-- Table: Reading
CREATE TABLE Reading (
    id_reading int  NOT NULL,
    time timestamp  NOT NULL,
    used_energy decimal(2,0)  NOT NULL,
    id_meter int  NOT NULL,
    CONSTRAINT Reading_pk PRIMARY KEY (id_reading)
);

-- foreign keys
-- Reference: Client_Address (table: Client)
ALTER TABLE Client ADD CONSTRAINT Client_Address
    FOREIGN KEY (id_clients_mailing_address)
    REFERENCES Address (id_address)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Comment_Client (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT Comment_Client
    FOREIGN KEY (id_author)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Comment_Post (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT Comment_Post
    FOREIGN KEY (id_post)
    REFERENCES Post (id_post)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Meter_Address (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT Meter_Address
    FOREIGN KEY (id_meters_place_address)
    REFERENCES Address (id_address)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Meter_Client (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT Meter_Client
    FOREIGN KEY (id_owner)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: OfferForMeter_Meter (table: OfferForMeter)
ALTER TABLE OfferForMeter ADD CONSTRAINT OfferForMeter_Meter
    FOREIGN KEY (id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: OfferForMeter_Offer (table: OfferForMeter)
ALTER TABLE OfferForMeter ADD CONSTRAINT OfferForMeter_Offer
    FOREIGN KEY (id_offers_type)
    REFERENCES Offer (id_offer)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Post_Client (table: Post)
ALTER TABLE Post ADD CONSTRAINT Post_Client
    FOREIGN KEY (id_author)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Reading_Meter (table: Reading)
ALTER TABLE Reading ADD CONSTRAINT Reading_Meter
    FOREIGN KEY (id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

