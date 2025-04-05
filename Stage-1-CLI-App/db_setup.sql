-- Drop existing tables (optional - be cautious in production)
DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS device;
DROP FUNCTION IF EXISTS update_reports;
DROP TRIGGER IF EXISTS after_reading_insert ON reading;

-- Create device table
CREATE TABLE device (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    highest FLOAT,
    lowest FLOAT,
    average FLOAT,
    last_reading TIMESTAMP
);

-- Create reading table
CREATE TABLE reading (
    id SERIAL PRIMARY KEY,
    device INTEGER NOT NULL REFERENCES device(id) ON DELETE CASCADE,
    temperature FLOAT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function
CREATE OR REPLACE FUNCTION update_reports()
RETURNS TRIGGER AS $$
DECLARE 
    currentMax FLOAT;
    currentMin FLOAT;
    currentAvg FLOAT;
BEGIN
    SELECT AVG(temperature), MAX(temperature), MIN(temperature)
    INTO currentAvg, currentMax, currentMin
    FROM reading
    WHERE device = NEW.device;

    UPDATE device
    SET average = currentAvg,
        highest = currentMax,
        lowest = currentMin,
        last_reading = NEW.recorded_at
    WHERE id = NEW.device;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to reading inserts
CREATE TRIGGER after_reading_insert
AFTER INSERT ON reading
FOR EACH ROW
EXECUTE FUNCTION update_reports();
