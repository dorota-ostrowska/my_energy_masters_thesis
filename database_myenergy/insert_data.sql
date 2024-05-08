INSERT INTO address(id_address, street, house_number, local_number, zip_code, city, additional_info)
VALUES 
	(1, 'Koszykowa', 64, '1c', '03-765', 'Sopot', ''),
	(2, 'Kwiatowa', 12, '1c', '03-353', 'Sopot', '11th level'),
	(3, 'Jesionowa', 4, '1c', '06-245', 'Szczecin', '');


INSERT INTO client(id_client, username, name, surname, pesel, id_clients_mailing_address, 
	email, password, member_of_challenge, number_of_rooms, number_of_residents)
VALUES 
	(1, null, 'Dorota', 'Ostrowska', '12345678999', 1, null, null, null, null, null),
	(2, null, 'Aleksandra', 'Nowak', '74638593645', 2, null, null, null, null, null),
	(3, null, 'Olga', 'Kowalska', '84736257378', 3, null, null, null, null, null);


INSERT INTO offer(id_offer, name, tarrif, pv_installation)
VALUES 
	(1, 'oszczedna zwykla', 'G11', 'n'),
	(2, 'oszczedna pv', 'G11', 'y');


INSERT INTO meter(id_meter, id_client, ppe, id_offer)
VALUES 
	(1, 1, '123456789999999999', 1),
	(2, 3, '983856789999999999', 2),
	(3, 2, '647892009999999999', 1);


INSERT INTO challenge(id_challenge, name, type_small_big, description, customizing_function)
VALUES 
	(
		1, 
		'Replace inefficient bulbs 💡', 
		'S',
		'Look for light bulbs in your home that consume a lot of energy and replace them with energy-saving equivalents that use much less energy 👌🍀 and at the same time provide equally bright and comfortable lighting 🔋💡. Your actions not only impact your wallet, but also reduce greenhouse gas emissions and protect the natural environment 🥳💰. Changing one light bulb may be a small step for you, but a giant leap for the planet! Will you be able to complete this task and make your home more ecological? Discover this by completing the task ⚡! Assuming that the bulb is used every day for a year for 4 hours, an old-type bulb consumes approximately {cost_old_type_bulb} zlotys, while an LED with the corresponding power consumes {cost_led} zlotys each year. When we take into account the number of rooms in your house ({number_of_rooms}) and assume that there is one regular bulb per room and all light bulbs are on for 4 hours every day for a year, this gives the amounts {cost_for_household_oldtype_bulb} PLN and {cost_for_household_led} PLN, for old-type bulbs and LEDs respectively. You can save even {subtract} zlotys per year.',
		'get_task_replace_bulbs'
	),
	(
		2, 
		'Dry your laundry outside 💦', 
		'S',
		'Your goal is to avoid using electric clothes dryer 🤖 by using natural drying methods outdoors like clothes racks 🌱 if the weather is apropriate. Can you avoid using a clothes dryer and choose more sustainable drying methods 💦? Check it this week if it is possible 💚. {weather_today}',
		'get_task_dry_laundry_outside'
	),
	(
		3, 
		'Set sleep mode 🖥️', 
		'S',
		'The task is to configure the computer to automatically enter sleep mode after an extended period of inactivity 🖥️. This is to save energy and reduce electricity consumption 💻. Through this simple change, you can significantly reduce costs and have a positive impact on the environment ⏰⌛. How to configure it? 🧐🤔 link: {link_guide}',
		'get_task_sleep_mode'
	);
        