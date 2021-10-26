import json
from tkinter import *
from functools import partial
#requires tk

buttonLabels = ["BUTTON1", "BUTTON2", "BUTTON3", "BUTTON4", "BUTTON5", "BUTTON6", "RIGHT", "UP", "DOWN", "LEFT"]
buttonPlaces = [(376,248), (430,208), (499,210), (564,218), (190,259), (618,355), (418,87), (348,21), (210,133), (200,46)]

with open("json/tksymbols.json", encoding='utf8') as jsonFile:
  buttonSymbols = json.load(jsonFile)
print(buttonSymbols)
class GUI:
  def __init__(self, glue):
    self.glue = glue
    self.root = Tk()
    self.buttons = {}
    self.root.title("Arduino Arcade Controller Keybinder")
    self.bg = PhotoImage(file = "graphics/background.png")
    self.background = Canvas(master=self.root, width=800, height=600)
    self.background.pack(fill = "both", expand = True)
    self.background.create_image(0, 0, image = self.bg, anchor = "nw")
    self.addRebindButtons()

  def addRebindButtons(self):
    for i, placement in enumerate(buttonPlaces):
      buttonAction = partial(self.rebindAction, buttonLabels[i])
      self.buttons[buttonLabels[i]] = Button(self.root, text="a", command=buttonAction)
      self.buttons[buttonLabels[i]].place(x=placement[0], y=placement[1], width=25, height=40)

  def enableButtons(self):
    for button in self.buttons:
      self.buttons[button]['state'] = 'normal'

  def disableButtons(self):
    for button in self.buttons:
      self.buttons[button]['state'] = 'disabled'

  def rebindAction(self, buttonId):
    self.disableButtons()
    self.buttons[buttonId]['text'] = '...'
    action = partial(self.rebind, buttonId)
    self.root.bind('<Key>', action)
  
  def rebind(self, buttonId, keyEvent):
    key = keyEvent.keysym
    if key in buttonSymbols:
      self.buttons[buttonId]['text'] = buttonSymbols[key]
      print(buttonSymbols[key])
    else:
      self.buttons[buttonId]['text'] = key
    self.root.unbind('<Key>')
    self.enableButtons()
    self.glue(key, buttonId)

  def setBinding(self, binding):
    for i, button in enumerate(self.buttons):
      if binding[i] in buttonSymbols:
        self.buttons[button]['text'] = buttonSymbols[binding[i]]
      else:
        self.buttons[button]['text'] = binding[i]

  def start(self):
    self.root.mainloop()