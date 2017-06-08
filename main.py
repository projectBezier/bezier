#-- import des modules --#
from tkinter import *
from math import sqrt, factorial

#-- variables locales --#
global cursorMode, curveMode, scene, pList, curvePts, curveLns, radius, ptIndex

#-- creation des fonctions --#
def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def moyenne(a,b):
    return (a+b)/2

def getIndexClickedPoint(x, y, pL):
    for i in range(len(pL)):
        if distance(pL[i].x, pL[i].y, x, y) <= pL[i].r:
            return i
    return -1

def changeCursorMode(mode):
    global cursorMode
    if mode == 'add':
        scene.configure(cursor = 'tcross')
    elif mode == 'del':
        scene.configure(cursor = 'circle')
    elif mode == 'mvpt':
        scene.configure(cursor = 'hand1')
    elif mode == 'mvcan':
        scene.configure(cursor = 'hand1')
    cursorMode = mode

def rotate(event):
    pass

def listeMilieux(pL):
    temp = []
    count = 0
    for i in range(len(pL)-1):
        x = (pL[i].x + pL[i+1].x)/2
        y = (pL[i].y + pL[i+1].y)/2
        pt = point(x,y,1)
        temp.append(pt)
    return temp

def bezierbern(l):
    n=len(l)-1
    points = []
    t = 0
    factN = factorial(n)
    while t <= 1:
        Px = Py = 0
        for i in range(n+1):
            if i == 0:
                factI = 1
                factNI = factN
            else:
                factI = factI*i
                factNI = factNI / (n-i+1)
            B=((factN)/(factI*factNI))*t**(i)*(1-t)**(n-i)
            Px+=B*l[i].x
            Py+=B*l[i].y
        points.append(point(Px, Py, 0))
        t += 0.01
    return points


def getCurve():
    global curveMode
    for i in curveLns:
        scene.delete(i)
    if curveMode == 'bezier':
        fpts = bezierbern(pList)
    elif curveMode == 'spline':
        pass
    for i in range(len(fpts)-1):
        curveLns.append(scene.create_line(fpts[i].x, fpts[i].y, fpts[i+1].x, fpts[i+1].y, width = 2))

def changeCurveMode(m):
    global curveMode
    curveMode = m
    getCurve()

def leftClick(event):
    global curveMode
    if cursorMode == 'add':
        pList.append(point(event.x, event.y, radius, outline = 'black'))
    elif cursorMode == 'del':
        i = getIndexClickedPoint(event.x, event.y, pList)
        if i > -1:
            pList[i].delete()
            pList.remove(pList[i])
    if curveMode != '':
        getCurve()

def delAll():
    while len(pList) > 0:
        pList[0].delete()
        pList.remove(pList[0])
    if curveMode != '':
        getCurve()

def leftDrag(event):
    global ptIndex, curveMode
    if cursorMode == 'mvpt':
        if ptIndex != -1:
            pList[ptIndex].update(event.x, event.y)
        else:
            i = getIndexClickedPoint(event.x, event.y, pList)
            if i != -1:
                ptIndex = i
                pList[ptIndex].update(event.x, event.y)
    elif cursorMode == 'mvcan':
        scene.coords(ALL, event.x, event.y)
    if curveMode != '':
        getCurve()

def releaseLClick(event):
    global ptIndex
    ptIndex = -1

def zoom(event):
    global radius
    if event.num == 4:
        radius = radius * 1.1
        scene.scale("all", event.x, event.y, 1.1, 1.1)
    else:
        radius = radius * 0.9
        scene.scale("all", event.x, event.y, 0.9, 0.9)

    for i in range(len(pList)):
        x = moyenne(scene.coords(pList[i].body)[0], scene.coords(pList[i].body)[2])
        y = moyenne(scene.coords(pList[i].body)[1], scene.coords(pList[i].body)[3])
        pList[i].update(x, y, radius)

# -- creation des classes --#
class point:
    def __init__(self, x, y, r = 0, color = 'blue', outline = ''):
        self.x = x
        self.y = y
        self.r = r
        self.body = scene.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill = color, outline= outline)

    def update(self, x, y, r = 'none'):
        if r != 'none':
            self.r = r
        self.x, self.y = x, y
        scene.coords(self.body, x-self.r, y-self.r, x+self.r, y+self.r)

    def changeColor(self, color):
        scene.itemconfig(self.body, fill = color)

    def delete(self):
        scene.delete(self.body)

#-- programme principal --#
root = Tk()
root.title('Bezier Project')
root.attributes('-zoomed', True)
root.configure(bg = '#202020')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
color1 = '#202020'
color2 = '#f4f4f4'
closedCurve = False
degree = 1
cursorMode = ''
pList = []
curveLns = []
curveMode = ''
radius = 10
ptIndex = -1

controls = Frame(root, bg = color1, width = 600, height = h-150)

c_pts = LabelFrame(controls, bg = color1, fg = color2, text = 'Points', width = 200)

Button(c_pts, text = 'ajouter', command = lambda:changeCursorMode('add'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'supprimer', command = lambda:changeCursorMode('del'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'deplacer', command = lambda:changeCursorMode('mvpt'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'reinitialiser', command = delAll, relief = FLAT).pack(side = RIGHT, padx = 5, pady = 5)
c_pts.pack(padx = 10, pady = 5)
c_can = LabelFrame(controls, bg = color1, fg = color2, text = 'Canvas', width = 200)

Button(c_can, text = 'se deplacer', command = lambda:changeCursorMode('mvcan'), relief = FLAT).grid(row = 0, sticky = W, padx = 5, pady = 5)
Scale(c_can, from_ = -180, to = 180, label = 'rotation', bg = color1, fg = color2, length = 150, sliderrelief = FLAT, orient = HORIZONTAL, command = rotate).grid(row = 0, column = 1, padx = 5, pady = 5)
c_can.pack(padx = 10, pady = 5)
c_crv = LabelFrame(controls, bg = color1, fg = color2, text = 'Courbe', width = 200)

Button(c_crv, text = 'bezier', command = lambda:changeCurveMode('bezier'), relief = FLAT).grid(row = 0, column = 0, padx = 5, pady = 5)
Button(c_crv, text = 'spline', command = lambda:changeCurveMode('spline'), relief = FLAT).grid(row = 1, column = 0, padx = 5, pady = 5)
Checkbutton(c_crv, text = 'courbe fermee', bg = color1, fg = color2, selectcolor = color1, variable = closedCurve, onvalue = True, offvalue = False).grid(row = 0, column = 1, padx = 5, pady = 5)
Entry(c_crv, textvariable = degree, width = 14).grid(row = 1, column = 1, padx = 5, pady = 5)
c_crv.pack(padx = 10, pady = 5)

Button(controls, text='quitter', bg = color1, fg = color2, command = root.quit, relief = FLAT).pack(side = BOTTOM, pady = 10)
controls.pack(side = LEFT, padx = 15)
controls.pack_propagate(0)

scene = Canvas(root, width = w-600, height = h-150)
scene.bind("<Button-1>", leftClick)
scene.bind("<ButtonRelease-1>", releaseLClick)
scene.bind("<B1-Motion>", leftDrag)
scene.bind("<Button-4>", zoom)
scene.bind("<Button-5>", zoom)

scene.pack(side = RIGHT, padx = 15)
root.mainloop()
