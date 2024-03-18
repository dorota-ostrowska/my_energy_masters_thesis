INSERT INTO address(id_address, street, house_number, zip_code, city, additional_info)
VALUES 
	(1, 'Koszykowa', 64, '03-765', 'Sopot', ''),
	(2, 'Kwiatowa', 12, '03-353', 'Sopot', '11th level'),
	(3, 'Jesionowa', 4, '06-245', 'Szczecin', ''),
	(4, 'Robaczkowa', 76, '06-145', 'Szczecin', 'building A'),
	(5, 'Brzoskwiniowa', 34, '06-865', 'Szczecin', '');

INSERT INTO client(id_client, name, surname, pesel, address_id_address, email, password)
VALUES 
	(1, 'Dawid', 'Sikora', '98050372564', 1, 'dawid.sikora@gmail.com', 'Haslo123!'),
	(2, 'Aleksandra', 'Nowak', '74638593645', 1, 'aleksandra.nowak@gmail.com', 'Haslo123!'),
	(3, 'Olga', 'Kowalska', '84736257378', 2, 'olga.kowalska@gmail.com', 'Haslo123!'),
	(4, 'Tomasz', 'Rogalski', '57639574626', 2, 'tomasz.rogalski@gmail.com', 'Haslo123!'),
	(5, 'Mateusz', 'Ostrowski', '87536475965', 3, 'mateusz.ostrowski@gmail.com', 'Haslo123!'),
	(6, 'Dorota', 'Mosakowska', '98765456789', 3, 'dorota.mosakowska@gmail.com', 'Haslo123!'),
	(7, 'Natalia', 'Pomidor', '78654356782', 4, 'natalia.pomidor@gmail.com', 'Haslo123!'),
	(8, 'Anna', 'Rakowska', '90873648563', 4, 'anna.rakowska@gmail.com', 'Haslo123!'),
	(9, 'Bogdan', 'Tokarski', '89765678107', 5, 'bogdan.tokarski@gmail.com', 'Haslo123!'),
	(10, 'Maria', 'Bananowa', '97648290065', 5, 'maria.bananowa@gmail.com', 'Haslo123!');

INSERT INTO meter(id_meter, client_id_client, address_id_address, ranking_points)
VALUES 
	(1, 1, 1, 67),
	(2, 1, 1, 54),
	(3, 1, 2, 76),
	(4, 1, 2, 12),
	(5, 2, 2, 0),
	(6, 3, 3, 8),
	(7, 4, 4, 76),
	(8, 4, 1, 43),
	(9, 4, 4, 23),
	(10, 5, 1, 8),
	(11, 5, 5, 9),
	(12, 5, 5, 1),
	(13, 5, 5, 4),
	(14, 6, 1, 65),
	(15, 7, 2, 103),
	(16, 7, 3, 49),
	(17, 8, 3, 2),
	(18, 9, 4, 43),
	(19, 9, 4, 24),
	(20, 10, 5, 65);

INSERT INTO offer(id_offer, tarrif, pv_installation)
VALUES 
	(1, 'G11', 'n'),
	(2, 'G11', 'y'),
	(3, 'G12', 'n'),
	(4, 'G12', 'y'),
	(5, 'G12w', 'n'),
	(6, 'G12w', 'y');

INSERT INTO offersformeter(id_offersformeter, offer_id_offer, meter_id_meter, start_date, end_date)
VALUES 
	(1, 1, 1, '2020-01-01', '2020-12-31'),
	(2, 1, 1, '2021-01-01', '2021-06-28'),
	(3, 1, 1, '2021-06-29', null),
	(4, 1, 2, '2023-06-13', null),
	(5, 3, 3, '2021-06-13', '2022-01-23'),
	(6, 4, 3, '2022-01-24', null),
	(7, 5, 4, '2020-07-15', null),
	(8, 6, 5, '2022-01-09', null),
	(9, 6, 6, '2021-11-11', null),
	(10, 2, 7, '2023-01-01', '2023-04-17'),
	(11, 2, 7, '2023-04-18', null),
	(12, 2, 8, '2024-01-01', null),
	(13, 2, 9, '2024-01-01', null),
	(14, 2, 10, '2024-01-01', null),
	(15, 4, 11, '2020-10-01', '2020-10-31'),
	(16, 5, 11, '2020-11-01', '2022-07-29'),
	(17, 6, 12, '2024-04-01', null),
	(18, 1, 13, '2023-01-01', null),
	(19, 1, 14, '2021-01-08', null),
	(20, 1, 15, '2020-01-01', '2021-07-06'),
	(21, 1, 15, '2021-07-07', null),
	(22, 1, 16, '2022-01-01', '2023-04-25'),
	(23, 1, 16, '2023-04-26', null),
	(24, 1, 17, '2024-01-01', null),
	(25, 1, 18, '2022-03-01', null),
	(26, 1, 19, '2020-01-02', null),
	(27, 1, 20, '2021-06-23', null);
