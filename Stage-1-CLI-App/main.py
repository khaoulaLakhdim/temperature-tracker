from dotenv import load_dotenv
import os

import psycopg2


def registerDevice(name):
        print(name)
        cur.execute("INSERT INTO device (name) VALUES (%s);", (name,))
        conn.commit()
        return 0

def LogTemp(device, temperature):
        print(device, temperature)
        cur.execute("INSERT INTO reading (device , temperature) VALUES (%s,%s);",(device,temperature,))
        conn.commit()
        return 0

def generateRep(id):
        print(id)
        cur.execute("SELECT highest, lowest , average, last_reading FROM device where id = %s",(id,))
        reports = cur.fetchone()
        conn.commit()
        return reports

def check_device(id):
        cur.execute("SELECT 1 FROM device where id = %s",(id,))
        if cur.fetchone():
                return 1
        else:
                return 0
        
def ListAll():
        cur.execute("SELECT *  FROM device;")
        devices = cur.fetchall()
        return devices

load_dotenv()

conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
) 

cur = conn.cursor()
cur.execute("DROP TRIGGER IF EXISTS after_reading_insert ON reading; CREATE OR REPLACE FUNCTION update_reports() RETURNS TRIGGER AS $$ DECLARE currentMax INT; currentMin INT; currentAvg INT; BEGIN SELECT AVG(temperature), MAX(temperature), MIN(temperature) INTO currentAvg, currentMax, currentMin FROM reading WHERE device = NEW.device; UPDATE device SET average = currentAvg, highest = currentMax, lowest = currentMin, last_reading=NEW.recorded_at WHERE id = NEW.device; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER after_reading_insert AFTER INSERT ON reading FOR EACH ROW EXECUTE FUNCTION update_reports();")
conn.commit()
while (1):
        print(
        "Welcome to Device Temperature Logger\n"
        "1 - Register a device\n"
        "2 - Log temperature reading for each device\n"
        "3 - Generate statistical reports\n"
        "4 - List all devices\n"
        "5 - Exit\n"
        )

        choice = int(input("Enter the corresponding number for your desired command: "))

        if choice == 1:
                print("New Device Registration:")
                name = input("Enter the name of the device:")
                registerDevice(name)

        elif choice == 2:
                print("Temperature logging:")
                id = input("Enter the ID of the device:")
                status = check_device(id) 
                if status ==1:
                        temperature = input("Enter the temperature of the device:")
                        LogTemp(id, temperature)
                else:
                        print("You entered an invalid ID!")
                        
        elif choice == 3:
                id = input("Enter the ID of the device:")
                report = generateRep(id)
                print(f"Minimum: {report[0]}, Maximum: {report[1]}, Average {report[2]}, Last Recorded {report[3]}")
        elif choice == 4:
                devices = ListAll()
                for device in devices:
                        print(f"id : {device[0]}, name : {device[1]}, created at : {device[2]}")
                        print(f"Minimum: {device[3]}, Maximum: {device[4]}, Average {device[5]}, Last Recorded {device[6]}\n")
        elif choice == 5:
                break
        else:
                print("Invalid choice. Please enter 1, 2, or 3.")




