import random
import rpg
import battle
import gui
import character
import sys
import time

def Mapper():
    table=[]
    app.wait_variable(app.inputVariable)
    size = app.inputVariable.get()
    for i in range (size):
      row=[]
      for j in range (size):
        row.append(".")
      table.append(row)

    x = y = 0
    table[y][x] = 'x'
    xb = yb = roll = random.randint(0, size)
    table[yb][xb] = 'h'
    for row in table:
      print(''.join(row))
    app.wait_variable(self.app.inputVariable)
    line = app.inputVariable.get()
    while line:
      table[y][x] = '.'
      if line.strip() == 'right':
        x += 1
      elif line.strip() == 'left':
        x -= 1
      elif line.strip() == 'up':
        y -= 1
      elif line.strip() == 'down':
        y += 1
      elif line.strip() == 'quit':
          app.quit()
      else:
          app.write('Please input a valid direction')
          app.wait_variable(self.app.inputVariable)
          line = app.inputVariable.get()
      table[y][x] = 'x'
      for row in table:
        self.app.write(''.join(row))
      app.wait_variable(self.app.inputVariable)
      line = app.inputVariable.get()
      if x and y == xb and yb:
          mapper = battle.Battle(player, enemies, app)
          return mapper
