INSERT INTO address(id_address, street, house_number, local_number, zip_code, city, additional_info)
VALUES 
	(1, 'Koszykowa', 64, '1c', '03-765', 'Sopot', ''),
	(2, 'Kwiatowa', 12, '1c', '03-353', 'Sopot', '11th level'),
	(3, 'Jesionowa', 4, '1c', '06-245', 'Szczecin', ''),
	(4, 'Robaczkowa', 76, '1c', '06-145', 'Szczecin', 'building A'),
	(5, 'Brzoskwiniowa', 34, '1c', '06-865', 'Szczecin', '');

INSERT INTO client(id_client, username, name, surname, pesel, id_clients_mailing_address, email, password)
VALUES 
	(1, 'dawidek123', 'Dawid', 'Sikora', '98050372564', 1, 'dawid.sikora@gmail.com', 'Haslo123!'),
	(2, 'olcia-energy', 'Aleksandra', 'Nowak', '74638593645', 1, 'aleksandra.nowak@gmail.com', 'Haslo123!'),
	(3, 'olgaaa876', 'Olga', 'Kowalska', '84736257378', 2, 'olga.kowalska@gmail.com', 'Haslo123!'),
	(4, 'pociag-tomek', 'Tomasz', 'Rogalski', '57639574626', 2, 'tomasz.rogalski@gmail.com', 'Haslo123!'),
	(5, 'matiooooo', 'Mateusz', 'Ostrowski', '87536475965', 3, 'mateusz.ostrowski@gmail.com', 'Haslo123!'),
	(6, 'doris123321', 'Dorota', 'Mosakowska', '98765456789', 3, 'dorota.mosakowska@gmail.com', 'Haslo123!'),
	(7, 'natka-latka', 'Natalia', 'Pomidor', '78654356782', 4, 'natalia.pomidor@gmail.com', 'Haslo123!'),
	(8, 'ania43rako', 'Anna', 'Rakowska', '90873648563', 4, 'anna.rakowska@gmail.com', 'Haslo123!'),
	(9, 'bodziooo43', 'Bogdan', 'Tokarski', '89765678107', 5, 'bogdan.tokarski@gmail.com', 'Haslo123!'),
	(10, 'maryska320', 'Maria', 'Bananowa', '97648290065', 5, 'maria.bananowa@gmail.com', 'Haslo123!');

INSERT INTO meter(id_meter, id_owner, id_meters_place_address, member_of_challange, ranking_points, number_of_rooms, number_of_residents)
VALUES 
	(1, 1, 1, FALSE, 0, null, null),
	(2, 1, 1, FALSE, 0, null, null),
	(3, 1, 2, FALSE, 0, null, null),
	(4, 1, 2, FALSE, 0, null, null),
	(5, 2, 2, FALSE, 0, null, null),
	(6, 3, 3, FALSE, 0, null, null),
	(7, 4, 4, FALSE, 0, null, null),
	(8, 4, 1, FALSE, 0, null, null),
	(9, 4, 4, FALSE, 0, null, null),
	(10, 5, 1, FALSE, 0, null, null),
	(11, 5, 5, FALSE, 0, null, null),
	(12, 5, 5, FALSE, 0, null, null),
	(13, 5, 5, FALSE, 0, null, null),
	(14, 6, 1, FALSE, 0, null, null),
	(15, 7, 2, FALSE, 0, null, null),
	(16, 7, 3, FALSE, 0, null, null),
	(17, 8, 3, FALSE, 0, null, null),
	(18, 9, 4, FALSE, 0, null, null),
	(19, 9, 4, FALSE, 0, null, null),
	(20, 10, 5, FALSE, 0, null, null);

INSERT INTO offer(id_offer, name, tarrif, pv_installation)
VALUES 
	(1, 'oszczedna zwykla', 'G11', 'n'),
	(2, 'oszczedna pv', 'G11', 'y'),
	(3, 'oszczedna zwykla', 'G12', 'n'),
	(4, 'oszczedna pv', 'G12', 'y'),
	(5, 'oszczedna zwykla', 'G12w', 'n'),
	(6, 'oszczedna pv', 'G12w', 'y');

INSERT INTO offerformeter(id_offer_for_meter, id_offers_type, id_meter, start_date, end_date)
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

INSERT INTO challange(id_challange, name, type_small_big, description)
VALUES 
	(
		1, 
		'Reduce energy consumption by 10% per week 🌍', 
		'B', 
		'Your goal is to reduce energy consumption by 10% in a week ⚡️. You can achieve this by making conscious choices about the use of electrical appliances and lighting 💡, turning off unused equipment and using natural daylight whenever possible 🌞. Try to make these changes and observe how they will affect your everyday comfort, while caring for the environment 🌍. Currently, your average weekly electricity consumption is approximately {current_weekly_consumption} kWh. If you reduced them by only 10% (it is easy - trust me), you could save approximately {expected_annual_savings} PLN per year. That is a lot, is not it? :)'
	),
	(
		2, 
		'Replace inefficient bulbs 💡', 
		'S',
		'Look for light bulbs in your home that consume a lot of energy and replace them with energy-saving equivalents that use much less energy 👌🍀 and at the same time provide equally bright and comfortable lighting 🔋💡. Your actions not only impact your wallet, but also reduce greenhouse gas emissions and protect the natural environment 🥳💰. Changing one light bulb may be a small step for you, but a giant leap for the planet! Will you be able to complete this task and make your home more ecological? Discover this by completing the task ⚡! Assuming that the bulb is used every day for a year for 4 hours, an old-type bulb consumes approximately {cost_old_type_bulb} zlotys, while an LED with the corresponding power consumes {cost_led} zlotys each year. When we take into account the number of rooms in your house ({number_of_rooms}) and assume that there is one regular bulb per room and all light bulbs are on for 4 hours every day for a year, this gives the amounts {cost_for_household_oldtype_bulb} PLN and {cost_for_household_led} PLN, for old-type bulbs and LEDs respectively. You can save even {cost_for_household_oldtype_bulb-cost_for_household_led} zlotys per year.'
	),
	(
		3, 
		'Dry your laundry outside 💦', 
		'S',
		'Your goal is to avoid using electric clothes dryer 🤖 by using natural drying methods outdoors like clothes racks 🌱 if the weather is apropriate. Can you avoid using a clothes dryer and choose more sustainable drying methods 💦? Check it this week if it is possible 💚. {weather_today}'
		),
	(
		4, 
		'Set sleep mode 🖥️', 
		'S',
		'The task is to configure the computer to automatically enter sleep mode after an extended period of inactivity 🖥️. This is to save energy and reduce electricity consumption 💻. Through this simple change, you can significantly reduce costs and have a positive impact on the environment ⏰⌛. How to configure it? 🧐🤔 link: {link_guide}'
	);


        