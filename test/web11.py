import time
from influxdb import InfluxDBClient
 
# Set this variables, influxDB should be localhost on Pi
host = "192.168.43.180"
port = 8086
#user = "root"
#password = "root"
 
# The database we created
dbname = "demo"
# Sample period (s)
interval = 1

#temp = "88"
 
# Create the InfluxDB object
client = InfluxDBClient(host=host, port=port, database=dbname)
 
# Run until keyboard out
try:
    while True:
        t = raw_input("nhap gia tri temperature:\n")
        #print("ban chon: {}".format(t))
        temp = float(t)
        print("ban chon: {}".format(temp))
        json_body = [
            {
            # "demo_temperature" is measurement,which I need to display
                "measurement": "sensor1", 
                "fields": {
                    # temp is value of demo_temperature
                    "value": temp,
                }
            }
        ]
 
        # Write JSON to InfluxDB
        client.write_points(json_body)
        # Wait for next sample
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass
