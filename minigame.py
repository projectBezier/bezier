#-- import des modules --#
from tkinter import *
from os import system
from useful import *
from math import sqrt

#-- variables locales --#

#-- creation des fonctions --#
def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def moving():
    global plyr, ismoving, keyhist, jump
    for key in keyhist:
        if key == 'z':
            keyhist.remove('z')
            if jump < 2:
                jump += 1
                plyr.v[1] = -10
        elif key == 'q':
            plyr.v[0] = -plyr.speed
        elif key == 'd':
            plyr.v[0] = plyr.speed
    ismoving = root.after(50, moving)

def controls(event):
    global holdkey, keyhist
    holdkey = event.keysym
    if not(holdkey in keyhist):
        keyhist.append(holdkey)

def releasecontrols(event):
    global holdkey, ismoving, plyr, keyhist, jump
    if event.keysym != 'z':
        keyhist.remove(event.keysym)
    if keyhist == []:
        plyr.v[0] = 0

# -- creation des classes --#
class perso(object):
    def __init__(self):
        global size
        self.a = [0,1]
        self.v = [0,0]
        self.speed = 3
        self.x = w/2
        self.y = h/2
        self.pv = 3
        self.color = 'red'
        self.body = c.create_rectangle(self.x-size, self.y-size, self.x+size, self.y+size, fill = self.color)
        self.update()

    def show(self):
        global w, h
        if self.pv == 3:
            self.color = 'red'
        elif self.pv == 2:
            self.color = 'orange'
        elif self.pv == 1:
            self.color = 'black'

        if self.pv > 0:
            c.coords(self.body, self.x-size, self.y-size, self.x+size, self.y+size)
            c.itemconfig(self.body, fill = self.color)
        else:
            c.delete(self.body)


    def hitsurface(self):
        global terrain, size
        for i in terrain:
            if distance(self.x, 0, i.x, 0) <= size:
                pass

    def update(self):
        self.v[0] += self.a[0]
        self.v[1] += self.a[1]
        self.x +=  self.v[0]
        self.y += self.v[1]
        self.hitsurface()
        self.show()
        root.after(33, self.update)

class block(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.body = c.create_rectangle(x, y, x+size, y+size, fill = 'white')


#-- programme principal --#
mapArray = lire_txt('terrain.data')
size = 10
h = len(mapArray)*size
if h > 0:
    w = len(mapArray[0])*size
else:
    w = 640
holdkey = 'none'
ismoving = None
keyhist = []
jump = 0

system('xset r off')

root = Tk()
root.title('mini_game')
c = Canvas(root, width = w, height = h)
c.focus_set()
c.bind('<KeyPress>', controls)
c.bind('<KeyRelease>', releasecontrols)

terrain = []
for i in range(len(mapArray)):
    for j in range(len(mapArray[0])):
        if mapArray[i][j] == '#':
            print(i, j)
            terrain.append(block(j*size, i*size))

plyr = perso()
moving()

c.pack()
root.mainloop()
system('xset r on')
