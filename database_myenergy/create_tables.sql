-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-05-02 20:25:52.867

-- tables
-- Table: Address
CREATE TABLE Address (
    id_address int  NOT NULL,
    street varchar(50)  NOT NULL,
    house_number varchar(5)  NOT NULL,
    local_number varchar(5)  NOT NULL,
    zip_code varchar(6)  NOT NULL,
    city varchar(50)  NOT NULL,
    additional_info varchar(50)  NULL,
    CONSTRAINT Address_pk PRIMARY KEY (id_address)
);

-- Table: Challange
CREATE TABLE Challange (
    id_challange int  NOT NULL,
    name varchar(50)  NOT NULL,
    type_small_big char(1)  NOT NULL,
    description text  NOT NULL,
    customizing_function varchar(50)  NOT NULL,
    CONSTRAINT Challange_pk PRIMARY KEY (id_challange)
);

-- Table: Client
CREATE TABLE Client (
    id_client int  NOT NULL,
    username varchar(50)  NULL,
    name varchar(50)  NOT NULL,
    surname varchar(50)  NOT NULL,
    pesel varchar(11)  NOT NULL,
    id_clients_mailing_address int  NOT NULL,
    email varchar(50)  NULL,
    password text  NULL,
    member_of_challange boolean  NULL,
    number_of_rooms int  NULL,
    number_of_residents int  NULL,
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

-- Table: CustomizedChallange
CREATE TABLE CustomizedChallange (
    id_customized_challange int  NOT NULL,
    id_client int  NOT NULL,
    id_challange int  NOT NULL,
    is_done boolean  NOT NULL,
    points_scored int  NOT NULL,
    start_date timestamp  NULL,
    end_date timestamp  NULL,
    CONSTRAINT CustomizedChallange_pk PRIMARY KEY (id_customized_challange)
);

-- Table: Favourite
CREATE TABLE Favourite (
    id_like int  NOT NULL,
    date_created timestamp  NOT NULL,
    id_post int  NOT NULL,
    id_author int  NOT NULL,
    CONSTRAINT Favourite_pk PRIMARY KEY (id_like)
);

-- Table: Invoice
CREATE TABLE Invoice (
    id_invoice int  NOT NULL,
    id_meter int  NOT NULL,
    date_of_issue timestamp  NOT NULL,
    amount_to_pay decimal(2,0)  NOT NULL,
    used_energy decimal(2,0)  NOT NULL,
    CONSTRAINT Invoice_pk PRIMARY KEY (id_invoice)
);

-- Table: Meter
CREATE TABLE Meter (
    id_meter int  NOT NULL,
    id_client int  NOT NULL,
    ppe varchar(18)  NOT NULL,
    id_offer int  NOT NULL,
    CONSTRAINT Meter_pk PRIMARY KEY (id_meter)
);

-- Table: Offer
CREATE TABLE Offer (
    id_offer int  NOT NULL,
    name varchar(50)  NOT NULL,
    tarrif varchar(50)  NOT NULL,
    pv_installation boolean  NOT NULL,
    CONSTRAINT Offer_pk PRIMARY KEY (id_offer)
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
-- Reference: CustomizedChallange_Client (table: CustomizedChallange)
ALTER TABLE CustomizedChallange ADD CONSTRAINT CustomizedChallange_Client
    FOREIGN KEY (id_client)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: client_address (table: Client)
ALTER TABLE Client ADD CONSTRAINT client_address
    FOREIGN KEY (id_clients_mailing_address)
    REFERENCES Address (id_address)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: comment_client (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT comment_client
    FOREIGN KEY (id_author)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: comment_post (table: Comment)
ALTER TABLE Comment ADD CONSTRAINT comment_post
    FOREIGN KEY (id_post)
    REFERENCES Post (id_post)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: customizedchallange_challange (table: CustomizedChallange)
ALTER TABLE CustomizedChallange ADD CONSTRAINT customizedchallange_challange
    FOREIGN KEY (id_challange)
    REFERENCES Challange (id_challange)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: favourite_client (table: Favourite)
ALTER TABLE Favourite ADD CONSTRAINT favourite_client
    FOREIGN KEY (id_author)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: favourite_post (table: Favourite)
ALTER TABLE Favourite ADD CONSTRAINT favourite_post
    FOREIGN KEY (id_post)
    REFERENCES Post (id_post)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: meter_client (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT meter_client
    FOREIGN KEY (id_client)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: meter_invoice (table: Invoice)
ALTER TABLE Invoice ADD CONSTRAINT meter_invoice
    FOREIGN KEY (id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: meter_offer (table: Meter)
ALTER TABLE Meter ADD CONSTRAINT meter_offer
    FOREIGN KEY (id_offer)
    REFERENCES Offer (id_offer)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: meter_reading (table: Reading)
ALTER TABLE Reading ADD CONSTRAINT meter_reading
    FOREIGN KEY (id_meter)
    REFERENCES Meter (id_meter)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: post_client (table: Post)
ALTER TABLE Post ADD CONSTRAINT post_client
    FOREIGN KEY (id_author)
    REFERENCES Client (id_client)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

