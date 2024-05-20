CREATE OR REPLACE FUNCTION generate_invoice() 
RETURNS TRIGGER AS $$
DECLARE
    last_month DATE;
    total_energy DECIMAL(10,5);  
    total_amount DECIMAL(10,5);  
    existing_invoice_id INT;
    invoice_billing_period DATE;
    energy_price DECIMAL(10,5); 
BEGIN
    -- Calculate the date for the last month
    last_month := date_trunc('month', NEW.time) - INTERVAL '1 month';
    invoice_billing_period := last_month;

    -- Check if the inserted reading is for the first day of a new month
    IF date_trunc('day', NEW.time) = date_trunc('month', NEW.time) THEN

        -- Check if an invoice for this meter and last month already exists
        SELECT id_invoice
        INTO existing_invoice_id
        FROM Invoice
        WHERE id_meter = NEW.id_meter 
        AND Invoice.billing_period = last_month;

        -- If no existing invoice found, create a new one
        IF existing_invoice_id IS NULL THEN
            -- Sum the energy usage for the last month
            SELECT COALESCE(SUM(used_energy), 0)
            INTO total_energy
            FROM Reading
            WHERE id_meter = NEW.id_meter 
            AND time >= last_month 
            AND time < date_trunc('month', NEW.time);

            -- Calculate a price of kWh.
            SELECT offer.kwh_price
            INTO energy_price
            FROM offer
            INNER JOIN meter
            ON meter.id_offer = offer.id_offer
            WHERE id_meter = NEW.id_meter;

            -- Calculate the amount to pay
            total_amount := total_energy * energy_price;

            -- Insert a record into the Invoice table
            INSERT INTO Invoice (id_meter, date_of_issue, amount_to_pay, used_energy, billing_period, is_it_paid)
            VALUES (NEW.id_meter, now(), total_amount, total_energy, invoice_billing_period, false);
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creating the trigger
CREATE TRIGGER after_insert_reading
AFTER INSERT ON Reading
FOR EACH ROW
EXECUTE FUNCTION generate_invoice();
