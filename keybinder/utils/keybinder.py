import re, sys, json, serial
import serial.tools.list_ports
# pyserial required

def readSpecialKeys(filepath):
  with open(filepath) as jsonFile:
    return json.load(jsonFile)

def getPort(description):
  for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
    if re.match('^{0}.*'.format(description), desc):
      return port
  return None

def getSerial(port):
  try:
    ser = serial.Serial(port)
    return ser
  except serial.serialutil.SerialException:
    return None

class keybinder:
  def __init__(self, boardDescription):
    self.desc = boardDescription
    self.port = getPort(self.desc)
    self.specialKeys = readSpecialKeys('json/keymap.json')
    self.reverseSpecialKeys = {v: k for k, v in self.specialKeys.items()}

  def getBinding(self):
    ser = getSerial(self.port)
    if (ser == None):
      return

    ser.write(b'GET')
    binding = ser.readline().decode().split(' ')
    ser.close()

    result = []
    for bind in binding:
      try:
        bind = int(bind)
        if bind < 128:
          result.append(chr(bind))
        elif bind in self.reverseSpecialKeys:
          result.append(self.reverseSpecialKeys[bind])
      except:
        pass

    return result

  def setBinding(self, binding, additionalMap=None):
    msg = bytearray()
    for c in binding:
      if len(c) == 1:
        msg.extend(c.encode())
      else:
        if additionalMap != None and c in additionalMap:
          c = additionalMap[c]
        if c in self.specialKeys:
          msg.extend(int(self.specialKeys[c]).to_bytes(1, byteorder='big'))

    ser = getSerial(self.port)
    if (ser == None):
        return
    ser.write(msg)
    ser.close()
