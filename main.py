#-- import des modules --#
from tkinter import *
from math import sqrt

#-- creation des fonctions --#
def changeCursorMode(mode):
    global cursorMode, scene
    if mode == 'add':
        scene.configure(cursor = 'tcross')
    elif mode == 'del':
        scene.configure(cursor = 'circle')
    elif mode == 'movept':
        scene.configure(cursor = 'hand1')
    elif mode == 'movecan':
        scene.configure(cursor = 'hand1')
    cursorMode = mode

def delAll():
    global pList
    while len(pList) > 0:
        pList[0].delete()
        pList.remove(pList[0])

def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def getIndexClickedPoint(x, y, pL):
    for i in range(len(pL)):
        if distance(pL[i].x, pL[i].y, x, y) <= pL[i].r:
            return i
    return -1

def leftClick(event):
    global cursorMode, pList
    if cursorMode == 'add':
        pList.append(point(event.x, event.y, 10))
    elif cursorMode == 'del':
        i = getIndexClickedPoint(event.x, event.y, pList)
        if i > -1:
            pList[i].delete()
            pList.remove(pList[i])

def releaseLClick(event):
    global ptIndex
    ptIndex = -1

def leftDrag(event):
    global cursorMode, pList, ptIndex
    if cursorMode == 'movept':
        if ptIndex != -1:
            pList[ptIndex].update(event.x, event.y)
        else:
            i = getIndexClickedPoint(event.x, event.y, pList)
            if i != -1:
                ptIndex = i
                pList[ptIndex].update(event.x, event.y)
    elif cursorMode == 'movecan':
        pass

# -- creation des classes --#
class point:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.spawn()
    def spawn(self):
        self.body = scene.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill = '#ffff55')

    def delete(self):
        scene.delete(self.body)

    def update(self, x, y):
        self.x, self.y = x, y
        scene.coords(self.body, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

#-- programme principal --#
root = Tk()
root.title('Bezier Project')
root.attributes('-zoomed', True)
root.configure(bg = '#202020')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

cursorMode = 'none'
pList = []
ptIndex = -1

controls = Frame(root, width = w//3, height = h)
points = Frame(controls, width = w//3, height = h//3)
Label(points, text = 'POINTS').pack()

p_btn = Frame(points, width = w//3)
Button(p_btn, text = 'ajouter', command = lambda: changeCursorMode('add')).pack(side = LEFT)
Button(p_btn, text = 'supprimer', command = lambda: changeCursorMode('del')).pack(padx = 5, side = LEFT)
Button(p_btn, text = 'deplacer', command = lambda: changeCursorMode('movept')).pack(side = LEFT)
Button(p_btn, text = 'reinitialiser', command = delAll).pack(side = RIGHT)
p_btn.pack(ipady = 15)
p_btn.pack_propagate(0)

#faire des inputs pour coords X,Y,Z avec les valeurs du point selectionné notées de base

points.pack(ipadx = 10, ipady = 10)
points.pack_propagate(0)

canvas = Frame(controls,width = w//3, height = h//3)
Label(canvas, text = 'CANVAS').pack()

Button(canvas, text = 'se deplacer', command = lambda: changeCursorMode('movecan')).pack(padx = 5)
zoom = Scale(canvas, from_=-100, to = 100, orient = HORIZONTAL).pack()
rotZ = Scale(canvas, from_=-180, to = 180, orient = HORIZONTAL).pack()
deg = Entry(canvas).pack()
canvas.pack(ipadx = 10, ipady = 10)
canvas.pack_propagate(0)

curve = Frame(controls,width = w//3, height = h//3)
Label(curve, text = 'COURBE').pack()
closed = Checkbutton(curve, text="courbe fermée").pack()
c_btn = Frame(curve, width = w//3)
Button(c_btn, text = 'bezier', command = lambda: curveMode('bezier')).pack(side = LEFT)
Button(c_btn, text = 'spline', command = lambda: curveMode('spline')).pack(padx = 5, side = LEFT)
c_btn.pack(ipady = 15)
c_btn.pack_propagate(0)
curve.pack(side = TOP, ipadx = 10, ipady = 10)
curve.pack_propagate(0)

controls.pack(side = LEFT)
controls.pack_propagate(0)

scene = Canvas(root, width = 2*w//3, height = h, bg = '#f4f4f4')
scene.bind("<Button-1>", leftClick)
scene.bind("<ButtonRelease-1>", releaseLClick)
scene.bind("<B1-Motion>", leftDrag)

scene.pack(side = RIGHT)
root.mainloop()
