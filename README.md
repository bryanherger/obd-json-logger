# obd-json-logger
Scripts to capture OBD-II data into JSON format for analytics.

Additional scripts and service examples are provided for JSON logging from gpsd/gpspipe (gpspipe.py) and accelerometer data (9dof.py) using Adafruit 9-DOF ACCEL/MAG/GYRO+TEMP BREAKOUT BOARD - LSM9DS1 from https://www.adafruit.com/product/3387

# prerequisites
You'll need an OBD-II to USB serial interface to read the data.  I'm using a Scantool OBDLink SX.

The scripts are developed and tested on Raspberry Pi platform.  It should work with any model Pi, though you'll need a car USB charger for power.

If you'd also like to collect GPS data to complement the OBD-II readout, there's a service and script to collect data from a USB GPS device supported by gpsd.  I'm using a u-Blox 7 GPS/GLONASS receiver.

# installation
Install Python 3 and the obd package (pip3 install obd)

Plug in the OBD-II connector and try running the script with "python3 obd2json.py".  It should start outputting JSON data to a log file in the /home/pi directory.

To start the script automatically, copy the obdii.service file to /lib/systemd/system and run:

sudo systemctl enable obdii

You can also start it immediately with sudo systemctl start obdii

If you have a GPS device attached, you can add the included gpspipe service and script to collect GPS data.  The GPS and OBD data will be logged as JSON to separate files currently.

# output
The obd library will scan for valid codes, and the script will read all Mode 1 diagnostic codes continuously (or, as fast as the interface can supply them, plus a short delay).

The library is documented at https://python-obd.readthedocs.io/en/latest/

The JSON output can be read by any engine that supports JSON input.  For example, load the data into Vertica (http://www.vertica.com/) with:

CREATE FLEX TABLE obd();

COPY obd FROM LOCAL 'obd-file' PARSER FJSONPARSER();

SELECT COMPUTE_FLEXTABLE_KEYS_AND_BUILD_VIEW('obd');

-- If using vsql, you may wish to set \x to read the OBD fields more easily

SELECT * FROM obd_view LIMIT 10;
