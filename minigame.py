#-- import des modules --#
from tkinter import *
from os import system
from useful import *
from math import sqrt

#-- variables locales --#

#-- creation des fonctions --#
def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def moving():
    global plyr, ismoving, keyhist, jump
    for key in keyhist:
        if key == 'Up':
            keyhist.remove('Up')
            if jump < 2:
                jump += 1
                plyr.v[1] = -10
        elif key == 'Left':
            plyr.v[0] = -plyr.speed
        elif key == 'Right':
            plyr.v[0] = plyr.speed
    ismoving = root.after(20, moving)

def controls(event):
    global holdkey, keyhist
    holdkey = event.keysym
    if not(holdkey in keyhist):
        keyhist.append(holdkey)

def releasecontrols(event):
    global holdkey, ismoving, plyr, keyhist, jump
    if event.keysym != 'Up':
        keyhist.remove(event.keysym)
    if keyhist == []:
        plyr.v[0] = 0

# -- creation des classes --#
class perso(object):
    def __init__(self, x, y):
        global size
        self.a = [0,1]
        self.v = [0,0]
        self.speed = 3
        self.x = x
        self.y = y
        self.w = 3*size/4
        self.body = c.create_rectangle(self.x-self.w, self.y-self.w, self.x+self.w, self.y+self.w, fill = '#27ADF9')
        self.update()

    def show(self):
        global w, h
        c.coords(self.body, self.x-self.w, self.y-self.w, self.x+self.w, self.y+self.w)

    def ishitting(self):
        global size, jump
        for i in coins:
            if distance(self.x, self.y, i.x, i.y) < size+self.w:
                c.delete(i.body)
                coins.remove(i)
            if len(coins) == 0:
                root.quit()
        for i in terrain:
            if self.v[1] < 0 and distance(self.x, 0, (i.x+i.X)/2, 0) < size+self.w:
                if distance(self.y, 0, i.Y, 0) < size:
                    self.v[1] = 0
                    self.y = i.Y+self.w
            elif self.v[1] > 0 and distance(self.x, 0, (i.x+i.X)/2, 0) < size+self.w:
                if distance(self.y, 0, i.y, 0) < size:
                    self.v[1] = 0
                    self.y = i.y-self.w
                    jump = 0
                elif distance(self.y, 0, i.y, 0) == size:
                    self.v[1] = 0
                    jump = 0

            if self.v[0] < 0 and distance(self.y, 0, (i.y+i.Y)/2, 0) < size+self.w:
                if distance(self.x, 0, i.X, 0) < size:
                    self.v[0] = 0
                    if self.v[1] >= 0:
                        self.v[1] = 0.2
                    self.x = i.X + self.w
                    jump = 1
                elif distance(self.x, 0, i.X, 0) == size:
                    self.v[0] = 0
                    jump = 1
            elif self.v[0] > 0 and distance(self.y, 0, (i.y+i.Y)/2, 0) < size+self.w:
                if distance(self.x, 0, i.x, 0) < size:
                    self.v[0] = 0
                    if self.v[1] >= 0:
                        self.v[1] = 0.2
                    self.x = i.x - self.w
                    jump = 1
                elif distance(self.x, 0, i.x, 0) == self.w:
                    self.v[0] = 0
                    jump = 1
            if self.x + self.w < 0 or self.x - self.w > w or self.y + self.w < 0 or self.y - self.w > h:
                root.quit()

    def update(self):
        self.v[0] += self.a[0]
        self.v[1] += self.a[1]
        self.ishitting()
        self.x += self.v[0]
        self.y += self.v[1]
        self.show()
        root.after(20, self.update)

class block:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.X, self.Y = x+2*size, y+2*size
        self.body = c.create_rectangle(x, y, self.X, self.Y, fill = '#202020', outline = '#202020')

class coin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.body = c.create_oval(x-size, y-size, x+size, y+size, fill ='yellow')


#-- programme principal --#
mapArray = lire_txt('terrain.data')
size = 10
h = len(mapArray)*2*size
w = len(mapArray[0])*2*size
holdkey = 'none'
ismoving = None
keyhist = []
jump = 0

system('xset r off')

root = Tk()
root.title('mini_game')
c = Canvas(root, width = w, height = h, bg = 'white')
c.focus_set()
c.bind('<KeyPress>', controls)
c.bind('<KeyRelease>', releasecontrols)

terrain = []
coins = []
for i in range(len(mapArray)):
    for j in range(len(mapArray[0])):
        if mapArray[i][j] == '#':
            terrain.append(block(2*j*size, 2*i*size))
        elif mapArray[i][j] == 'P':
            plyr = perso(2*j*size+size, 2*i*size+size)
        elif mapArray[i][j] == 'C':
            coins.append(coin(2*j*size+size, 2*i*size+size))
if len(coins) == 0:
    nocoins = True
else:
    nocoins = False
moving()

c.pack()
root.mainloop()
system('xset r on')
if len(coins) == 0 and not(nocoins):
    print('Vous avez gagné')
else:
    print('Vous avez perdu')
