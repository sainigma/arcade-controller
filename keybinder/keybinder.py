import re, sys, json, serial
import serial.tools.list_ports
# pyserial required

def readSpecialKeys(filepath):
  with open(filepath) as jsonFile:
    return json.load(jsonFile)

def getPort(pattern):
  for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
    if re.match('^{0}.*'.format(boardDesc), desc):
      return port
  return None

def getSerial():
  try:
    ser = serial.Serial(port)
    return ser
  except serial.serialutil.SerialException:
    return None

def getBinding():
  ser = getSerial()
  if (ser == None):
    return

  ser.write(b'GET')
  binding = ser.readline()
  ser.close()
  return binding

def setBinding(binding):
  msg = bytearray()
  for c in binding:
    if len(c) == 1:
      msg.extend(c.encode())
    elif c in specialKeys:
      msg.extend(int(specialKeys[c]).to_bytes(1, byteorder='big'))

  ser = getSerial()
  if (ser == None):
      return
  ser.write(msg)
  ser.close()

boardDesc = 'Arduino Leonardo'
port = getPort(boardDesc)

if port == None:
  sys.exit()

binding = ["z", "x", "c", "v", "b", "n", "RIGHT", "UP", "DOWN", "LEFT"]
specialKeys = readSpecialKeys('keymap.json')
setBinding(binding)