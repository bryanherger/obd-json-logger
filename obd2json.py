import json
import math
import obd
import time

sessionId = math.floor(time.time())

ports = obd.scan_serial()      # return list of valid USB or RF ports
print (ports)                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']

connection = obd.OBD() # auto connect
if connection.status() != obd.OBDStatus.CAR_CONNECTED:
    quit()
print (connection.status())
sourceFile = open('/home/pi/obd-'+str(time.time())+'.json', 'a')
while connection.status() == obd.OBDStatus.CAR_CONNECTED:
    ts = math.floor(time.time())
    obdDict = {}
    obdDict["sessionId"] = str(sessionId)
    obdDict["timestamp"] = str(ts)
    for pid in connection.supported_commands:
        pidName = str(pid.name)
        pidCmd = pid.command
        if pidCmd[1] == 49:
            resp = connection.query(pid)
            if hasattr(resp.value, 'units'):
                obdDict[pidName+'_'+str(resp.value.units)] = resp.value.magnitude
            else:
                obdDict[pidName] = str(resp.value)
    obdJson = json.dumps(obdDict)
    print(obdJson, file = sourceFile)
    sourceFile.flush()
    time.sleep(1)
sourceFile.flush()
sourceFile.close()

