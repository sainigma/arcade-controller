import json
from tkinter import *
from functools import partial
#requires tk

UPDATE_MS = int(1000/6)

buttonLabels = ["BUTTON1", "BUTTON2", "BUTTON3", "BUTTON4", "BUTTON5", "BUTTON6", "RIGHT",    "UP",     "DOWN",   "LEFT"]
buttonPlaces = [(376,248), (430,208), (499,210), (564,218), (180,259), (618,355), (418,115), (348,21), (205,170), (190,66)]

#Maps tk keys to Keyboard.h designations
with open("json/tkmap.json") as jsonFile:
  tkKeymap = json.load(jsonFile)

#Needed for bitmapfont operations
with open("json/keymap.json") as jsonFile:
  keymap = json.load(jsonFile)

class Animation:
  def __init__(self, filepath, filename, filetype, frames):
    self.frame = 0
    self.frames = []
    for i in range(0, frames):
      self.frames.append(PhotoImage(file = "{0}{1}_{2}.{3}".format(filepath,filename,i+1,filetype)))

  def update(self):
    self.frame = self.frame + 1
    self.frame = self.frame % len(self.frames)

  def getFrame(self):
    return self.frames[self.frame]

class FunkyButton:
  def __init__(self, root, size, placement, action, bitmapFont, buttonbg):
    self.crop = (0,0)
    self.size = size
    self.enabled = True
    self.text = ''
    self.bitmapFont = bitmapFont
    self.canvas = Canvas(master=root, width=size[0], height=size[1], bg='#c1b68c', cursor="hand2", highlightthickness=0)
    self.canvas.place(x=placement[0], y=placement[1])
    self.canvas.bind('<Button-1>', action)
    self.buttonbg = buttonbg
    self.update()

  def update(self):
    self.canvas.delete("all")
    if self.buttonbg != None:
      self.canvas.create_image(0,0,image=self.buttonbg.getFrame(), anchor="nw")
    self.canvas.create_image(-self.crop[0] * self.size[0] - 2, -self.crop[1] * self.size[1], image=self.bitmapFont.getFrame(), anchor="nw")

class GUI:
  def __init__(self, glue, port):
    self.glue = glue
    self.root = Tk()
    self.buttons2 = {}
    self.root.title("Arduino Arcade Controller Keybinder")
    
    self.backgroundAnimation = Animation('graphics/', 'background', 'png', 2)
    self.buttonbg = Animation("graphics/", "button", "png", 2)
    self.bitmapFont = Animation("graphics/", "font", "png", 2)

    self.background = Canvas(master=self.root, width=800, height=600, cursor="arrow", relief='ridge')
    self.background.pack(fill = "both", expand = True)
    self.setBackground(self.backgroundAnimation.getFrame())
    self.addRebindButtons()
    comport = port.split('COM')[1]
    self.port = FunkyButton(self.root, (32,32), (160,550), None, self.bitmapFont, None)
    self.port.crop = self.getFontCrop(comport)
    self.port.canvas['cursor'] = ''
    self.port.update()

  def getFontCrop(self, key):
    index = 0
    if len(key) == 1:
      index = ord(key)
    elif key in keymap:
      index = int(keymap[key])
    row = int(index / 16)
    col = index % 16
    crop = (col, row)
    print(index, crop)
    return crop

  def setBackground(self, img):
    self.background.delete("all")
    self.background.create_image(0, 0, image=img, anchor = "nw")

  def addRebindButtons(self):
    for i, placement in enumerate(buttonPlaces):
      
      buttonAction = partial(self.rebindAction, buttonLabels[i])
      self.buttons2[buttonLabels[i]] = FunkyButton(self.root, (32,32), placement, buttonAction,  self.bitmapFont, self.buttonbg)
      

  def enableButtons(self):
    self.background['cursor'] = ''
    for button in self.buttons2:
      self.buttons2[button].enabled = True
      self.buttons2[button].canvas['cursor'] = 'hand2'

  def disableButtons(self):
    self.background['cursor'] = 'none'
    for button in self.buttons2:
      self.buttons2[button].enabled = False
      self.buttons2[button].canvas['cursor'] = 'none'

  def rebindAction(self, buttonId, event):
    if self.buttons2[buttonId].enabled != True:
      return

    self.disableButtons()
    self.previousButtonText = self.buttons2[buttonId].text
    self.buttons2[buttonId].crop = (0,0)
    action = partial(self.rebind, buttonId)
    self.root.bind('<Key>', action)
  
  def rebind(self, buttonId, keyEvent):
    ok = False
    key = keyEvent.keysym
    if key in tkKeymap:
      self.buttons2[buttonId].crop = self.getFontCrop(tkKeymap[key])
      ok = True
    elif len(key) == 1:
      self.buttons2[buttonId].crop = self.getFontCrop(key)
      ok = True
    else:
      self.buttons2[buttonId].crop = self.getFontCrop(self.previousButtonText)
    if ok:
      self.glue(key, buttonId)
    self.root.unbind('<Key>')
    self.enableButtons()

  def setBinding(self, binding):
    for i, button in enumerate(self.buttons2):
      bind = binding[i]
      self.buttons2[button].text = bind
      if bind in keymap:
        self.buttons2[button].crop = self.getFontCrop(bind)
      else:
        self.buttons2[button].crop = self.getFontCrop(bind)

  def update(self, frame):
    frame = frame + 1
    self.backgroundAnimation.update()
    self.buttonbg.update()
    self.bitmapFont.update()
    self.port.update()
    self.setBackground(self.backgroundAnimation.getFrame())
    for button in self.buttons2:
      self.buttons2[button].update()
    self.root.after(UPDATE_MS, self.update, frame)

  def start(self):
    self.root.after(0, self.update, 0)
    self.root.mainloop()