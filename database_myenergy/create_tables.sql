-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-03-17 11:21:04.999

-- tables
-- Table: Address
CREATE TABLE Address (
    id_address int  NOT NULL,
    street varchar(50)  NOT NULL,
    house_number int  NOT NULL,
    zip_code varchar(50)  NOT NULL,
    city varchar(50)  NOT NULL,
    additional_info varchar(50)  NULL,
    CONSTRAINT Address_pk PRIMARY KEY (id_address)
);

-- Table: Client
CREATE TABLE Client (
    id_client int  NOT NULL,
    name varchar(50)  NOT NULL,
    surname varchar(50)  NOT NULL,
    pesel varchar(11)  NOT NULL,
    Address_id_address int  NOT NULL,
    email varchar(50)  NOT NULL,
    password varchar(50)  NOT NULL,
    CONSTRAINT Client_pk PRIMARY KEY (id_client)
);

-- Table: Meter
CREATE TABLE Meter (
    id_meter int  NOT NULL,
    Client_id_client int  NOT NULL,
    Address_id_address int  NOT NULL,
    ranking_points int  NOT NULL,
    CONSTRAINT Meter_pk PRIMARY KEY (id_meter)
);

-- Table: Offer
CREATE TABLE Offer (
    id_offer int  NOT NULL,
    tarrif varchar(50)  NOT NULL,
    pv_installation char(1)  NOT NULL,
    CONSTRAINT Offer_pk PRIMARY KEY (id_offer)
);

-- Table: OffersForMeter
CREATE TABLE OffersForMeter (
    id_offersformeter int  NOT NULL,
    Offer_id_offer int  NOT NULL,
    Meter_id_meter int  NOT NULL,
    start_date date  NOT NULL,
    end_date date  NULL,
    CONSTRAINT OffersForMeter_pk PRIMARY KEY (id_offersformeter)
);

-- Table: Reading
CREATE TABLE Reading (
    id_reading int  NOT NULL,
    time timestamp  NOT NULL,
    used_energy decimal(2,0)  NOT NULL,
    Meter_id_meter int  NOT NULL,
    CONSTRAINT Reading_pk PRIMARY KEY (id_reading)
);

-- foreign keys
-- Reference: Client_Address (table: Client)
ALTER TABLE Client ADD CONSTRAINT Client_Address
    FOREIGN KEY (Address_id_address)
    REFERENCES Address (id_address)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Meter_Address (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT Meter_Address
    FOREIGN KEY (Address_id_address)
    REFERENCES Address (id_address)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Meter_Client (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT Meter_Client
    FOREIGN KEY (Client_id_client)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: OffersForMeter_Meter (table: OffersForMeter)
ALTER TABLE OffersForMeter ADD CONSTRAINT OffersForMeter_Meter
    FOREIGN KEY (Meter_id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: OffersForMeter_Offer (table: OffersForMeter)
ALTER TABLE OffersForMeter ADD CONSTRAINT OffersForMeter_Offer
    FOREIGN KEY (Offer_id_offer)
    REFERENCES Offer (id_offer)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Reading_Meter (table: Reading)
ALTER TABLE Reading ADD CONSTRAINT Reading_Meter
    FOREIGN KEY (Meter_id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

