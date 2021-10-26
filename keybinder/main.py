import json
from utils.keybinder import keybinder
from gui.gui import GUI

buttonMap = {"BUTTON1":0, "BUTTON2":1, "BUTTON3":2, "BUTTON4":3, "BUTTON5":4, "BUTTON6":5, "RIGHT": 6, "UP": 7, "DOWN": 8, "LEFT": 9}
with open("json/tkmap.json") as jsonFile:
  tkKeymap = json.load(jsonFile)

def glue(bind, index):
  print("moi!",bind,buttonMap[index])
  binding[buttonMap[index]] = bind
  kbinder.setBinding(binding, tkKeymap)

kbinder = keybinder('Arduino Leonardo')

binding = kbinder.getBinding()

gui = GUI(glue)
gui.setBinding(binding)
gui.start()