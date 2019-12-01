# obd-json-logger
Scripts to capture OBD-II data into JSON format for analytics.

# prerequisites
You'll need an OBD-II to USB serial interface to read the data.  I'm using a Scantool OBDLink SX.

The scripts are developed and tested on Raspberry Pi platform.  It will work with any model Pi, though you'll need a car charger to power it.

# installation
Install Python 3 and the obd package (pip3 install obd)

Plug in the OBD-II connector and try running the script.  It should start outputting JSON data to the /home/pi directory.

To start the script automatically, copy the obdii.service file to /lib/systemd/system and run:

sudo systemctl enable obdii

You can also start it immediately with sudo systemctl start obdii

# output
The obd library will scan for valid codes, and the script will read all Mode 1 diagnostic codes continuously (or, as fast as the interface can supply them, plus a short delay).

The library is documented at https://python-obd.readthedocs.io/en/latest/

The JSON output can be read by any engine that supports JOSN input.  For example, load the data into Vertica (http://www.vertica.com/) with:

CREATE FLEX TABLE obd();

COPY obd FROM LOCAL 'obd-file' PARSER FJSONPARSER();

SELECT COMPUTE_FLEXTABLE_KEYS_AND_BUILD_VIEW('obd');

SELECT * FROM obd_view LIMIT 10;
