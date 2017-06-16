#-- import des modules --#
from tkinter import *
from math import sqrt, factorial
from useful import *
from numpy import *
from random import randint
from os import system

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

def bezierbern(temp):
    global closedCurve
    l = list(copy(temp))
    n=len(l)-1
    if closedCurve.get() and n > 0:
        l.append(l[0])
        n += 1
    points = []
    if n > 0:
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
        points.append(l[-1])
    return points

def splinequad(temp):
    global closedCurve
    l = list(copy(temp))
    if closedCurve.get():
        l.append(l[0])
    points = []
    a0 = 0
    for i in range(1,len(l)):
        a=2*(l[i].y-l[i-1].y)/(l[i].x-l[i-1].x)-a0
        b=l[i-1].y+a0*(l[i].x-l[i-1].x)/2
        s=l[i-1].x
        if s < l[i].x:
            while s <= l[i].x:
                Pi=b+(a*(s-l[i-1].x)**2 -a0*(s-l[i].x)**2)*1/(2*(l[i].x-l[i-1].x))
                points.append(point(s, Pi))
                s += 5
        else:
            while s >= l[i].x:
                Pi=b+(a*(s-l[i-1].x)**2 -a0*(s-l[i].x)**2)*1/(2*(l[i].x-l[i-1].x))
                points.append(point(s, Pi))
                s += -5
        a0=a
    return points

def splineb(l,T,d):
    n=len(l)
    points = []
    if n > 2:
        t = 0
        while t <= 1:
            Px = Py = 0
            for i in range(n):
                A=B(i,d,t,T)
                Px+=A*l[i].x
                Py+=A*l[i].y
            points.append(point(Px, Py, 0))
            t += 0.01
        points.append(l[-1])
    return points

def B(i,d,t,T):
    if d==0:
        if T[i] <= t< T[i+1]:
            b=1
        else:
            b=0
    else:
        if T[i+d]-T[i]==0:
            b=(T[i+d+1]-t)/(T[i+d+1]-T[i+1])*B(i+1,d-1,t,T)
        elif T[i+d+1]-T[i+1]==0:
            b=(t-T[i])/(T[i+d]-T[i])*B(i,d-1,t,T)
        else :
            b=(t-T[i])/(T[i+d]-T[i])*B(i,d-1,t,T)+(T[i+d+1]-t)/(T[i+d+1]-T[i+1])*B(i+1,d-1,t,T)
    return b

def splinec(temp):
    global closedCurve
    l = list(copy(temp))
    if closedCurve.get():
        l.append(l[0])
    points=[]
    ti=l[1].x
    tj=l[0].x
    Qi=l[1].y
    Qj=l[0].y
    Ti=(l[2].y-l[0].y)/(l[2].x-l[0].x)
    a=array([[tj**3,tj**2,tj,1],[6*tj,2,0,0],[ti**3,ti**2,ti,1],[3*ti**2,2*ti,1,0]])
    b=array([Qj,0,Qi,Ti])
    x = linalg.solve(a,b)
    s=l[0].x
    if s < l[1].x:
        while s <= l[1].x:
            P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
            points.append(point(s, P))
            s += 5
    else:
        while s >= l[1].x:
            P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
            points.append(point(s, P))
            s += -5
    for i in range(2,len(l)-1):
        ti=l[i].x
        tj=l[i-1].x
        Qi=l[i].y
        Qj=l[i-1].y
        Ti=(l[i+1].y-l[i-1].y)/(l[i+1].x-l[i-1].x)
        Tj=(l[i].y-l[i-2].y)/(l[i].x-l[i-2].x)
        a=array([[tj**3,tj**2,tj,1],[3*tj**2,2*tj,1,0],[ti**3,ti**2,ti,1],[3*ti**2,2*ti,1,0]])
        b=array([Qj,Tj,Qi,Ti])
        x = linalg.solve(a,b)
        s=l[i-1].x
        if s < l[i].x:
            while s <= l[i].x:
                P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
                points.append(point(s, P))
                s += 5
        else:
            while s >= l[i].x:
                P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
                points.append(point(s, P))
                s += -5
    n=len(l)-1
    ti=l[n].x
    tj=l[n-1].x
    Qi=l[n].y
    Qj=l[n-1].y
    Tj=(l[n].y-l[n-2].y)/(l[n].x-l[n-2].x)
    a=array([[tj**3,tj**2,tj,1],[3*tj**2,2*tj,1,0],[ti**3,ti**2,ti,1],[6*ti,2,0,0]])
    b=array([Qj,Tj,Qi,0])
    x = linalg.solve(a,b)
    s=l[n-1].x
    if s < l[n].x:
        while s <= l[n].x:
            P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
            points.append(point(s, P))
            s += 10
    else:
        while s >= l[n].x:
            P=x[0]*s**3+x[1]*s**2+x[2]*s+x[3]
            points.append(point(s, P))
            s += -10
    return points

def getCurve():
    global curveMode, w, h, radius
    for i in curveLns:
        scene.delete(i)
    if curveMode == 'bezier':
        fpts = bezierbern(pList)
    elif curveMode == 'spline':
        fpts = splinequad(pList)
    elif curveMode == 'splinec':
        while len(pList) < 3:
            pList.append(point(randint(0, w-600), randint(0, h-150), radius))
        fpts = splinec(pList)
    elif curveMode == 'bspline':
        changed = False
        while len(pList) < 2*bspl.degree.get()+1:
            changed = True
            pList.append(point(randint(radius, w-700), randint(radius, h-250), radius))
        if changed:
            bspl.updatecan(0)
        fpts = splineb(pList, bspl.getValues(), bspl.degree.get())
    for i in range(len(fpts)-1):
        curveLns.append(scene.create_line(fpts[i].x, fpts[i].y, fpts[i+1].x, fpts[i+1].y, width = 2))

def changeCurveMode(m):
    global curveMode, bspl
    curveMode = m
    if curveMode == 'bspline' and bspl == None:
        bspl = bsnds()
    elif curveMode != 'bspline' and bspl != None:
        bspl.c.destroy()
        bspl.degreescale.destroy()
        bspl = None

    getCurve()

def leftClick(event):
    global curveMode, ptIndex, bspl
    if cursorMode == 'add':
        pList.append(point(event.x, event.y, radius, outline = 'black'))
        if bspl != None:
            bspl.updatecan(0)
    elif cursorMode == 'del':
        i = getIndexClickedPoint(event.x, event.y, pList)
        if i > -1:
            pList[i].delete()
            pList.remove(pList[i])
            if bspl != None:
                bspl.updatecan(0)
    elif cursorMode == 'mvpt':
        i = getIndexClickedPoint(event.x, event.y, pList)
        if i != -1:
            ptIndex = i
    if curveMode != '':
        getCurve()

def delAll():
    while len(pList) > 0:
        pList[0].delete()
        pList.remove(pList[0])
    if bspl != None:
        bspl.updatecan(0)
    if curveMode != '':
        getCurve()

def leftDrag(event):
    global ptIndex, curveMode, tempevent
    if cursorMode == 'mvpt':
        if ptIndex != -1:
            pList[ptIndex].update(event.x, event.y)
        else:
            i = getIndexClickedPoint(event.x, event.y, pList)
            if i != -1:
                ptIndex = i
                pList[ptIndex].update(event.x, event.y)
    elif cursorMode == 'mvcan':
        if tempevent != None:
            scene.move('all', event.x-tempevent[0], event.y-tempevent[1])
            for i in range(len(pList)):
                x = moyenne(scene.coords(pList[i].body)[0], scene.coords(pList[i].body)[2])
                y = moyenne(scene.coords(pList[i].body)[1], scene.coords(pList[i].body)[3])
                pList[i].update(x, y, radius)
        tempevent = event.x, event.y
    if curveMode != '':
        getCurve()

def releaseLClick(event):
    global ptIndex, tempevent
    tempevent = None
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

def launchminigame():
    system('python3 mapCreator.py')

# -- creation des classes --#
class point:
    def __init__(self, x, y, r = 0, color = 'blue', outline = '', parent = None):
        self.x = x
        self.y = y
        self.r = r
        if parent == None:
            self.parent = scene
        else:
            self.parent = parent
        self.body = self.parent.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill = color, outline= outline)

    def update(self, x, y, r = 'none'):
        if r != 'none':
            self.r = r
        self.x, self.y = x, y
        self.parent.coords(self.body, x-self.r, y-self.r, x+self.r, y+self.r)

    def changeColor(self, color):
        self.parent.itemconfig(self.body, fill = color)

    def delete(self):
        self.parent.delete(self.body)

class pointSelector:
    def __init__(self):
        self.frame = LabelFrame(controls, text='point selectionné', bg = color1, fg = color2)
        self.variables = []
        self.entries = []
        self.index = ptIndex
        for i in range(2):
            va = StringVar()
            en = Entry(self.frame, textvariable=va, width = 10)
            if i == 0:
                Label(self.frame, text='x', bg = color1, fg = color2).grid(row = 0, column = 0)
            else:
                Label(self.frame, text='y', bg = color1, fg = color2).grid(row = 0, column = 1)
            en.grid(row = 1, column = i, padx = 5, pady = 5)
            self.variables.append(va)
            self.entries.append(en)
        self.frame.pack()
        self.checkvalue()

    def checkvalue(self):
        if ptIndex >= 0:
            self.index = ptIndex
            temp = pList[ptIndex]
            self.variables[0].set(temp.x)
            self.variables[1].set(temp.y)
        elif self.index == -1:
            self.variables[0].set('aucun point')
            self.variables[1].set('aucun point')
        root.after(10, self.checkvalue)

class bsnds:
    def __init__(self):
        self.degree = IntVar()
        self.degreescale = Scale(c_crv, bg = color1, fg = color2,variable = self.degree, orient='horizontal', from_=1, to=4, tickinterval=1, length=100, label='Degré', command = self.updatecan)
        self.degree.set(1)
        self.degreescale.grid(row = 4, column = 1, padx = 5, pady = 5)
        self.c = Canvas(c_crv, width = 200, height = 20, bg = '#F4F4F4')
        self.c.bind("<ButtonRelease-1>", self.rlsLC)
        self.c.bind("<B1-Motion>", self.lDrag)

        num = self.degree.get()+1+len(pList)
        if num == 0:
            temp = 0
        else:
            temp = 200/num
        self.pts = []
        self.index = -1
        for i in range(num):
            p = point(i*temp+temp/2, 10, 5, 'yellow', 'black', self.c)
            self.pts.append(p)
        self.c.grid(row = 4, column = 0, padx = 5, pady = 5)

    def updatecan(self, a):
        for i in self.pts:
            i.delete()
        num = self.degree.get()+1+len(pList) - 2*self.degree.get()-2
        if num == 0:
            temp = 0
        else:
            temp = 200/num
        self.pts = []
        for i in range(num):
            p = point(i*temp+temp/2, 10, 5, 'yellow', 'black', self.c)
            self.pts.append(p)
        getCurve()


    def lDrag(self, event):
        x1, y1 = event.x, event.y
        if self.index != -1:
            t = self.pts[self.index]
            if self.index > 0 and x1 < self.pts[self.index-1].x:
                t.update(self.pts[self.index-1].x, t.y)
            elif self.index < len(self.pts)-1 and x1 > self.pts[self.index+1].x:
                t.update(self.pts[self.index+1].x, t.y)
            else:
                t.update(x1, t.y)
            if t.x < 0:
                t.update(0, t.y)
            elif t.x > 200:
                t.update(200, t.y)

        else:
            found = False
            for i in range(len(self.pts)):
                if distance(x1, y1, self.pts[i].x, self.pts[i].y) <= 7:
                    self.index = i
                    found = True
                    break
            if not(found):
                self.index = -1
        getCurve()

    def rlsLC(self, event):
        self.index = -1

    def getValues(self):
        temp = []
        num = self.degree.get()+1
        for i in range(num):
            temp.append(0)
        for i in self.pts:
            temp.append(i.x/200)
        for i in range(self.degree.get()+1):
            temp.append(num)
        return temp

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
tempevent = None
pList = []
curveLns = []
curveMode = ''
radius = 10
ptIndex = -1
bspl = None
closedCurve = BooleanVar()

controls = Frame(root, bg = color1, width = 600, height = h-150)

c_pts = LabelFrame(controls, bg = color1, fg = color2, text = 'Points', width = 200)

Button(c_pts, text = 'ajouter', command = lambda:changeCursorMode('add'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'supprimer', command = lambda:changeCursorMode('del'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'deplacer', command = lambda:changeCursorMode('mvpt'), relief = FLAT).pack(side = LEFT, padx = 5, pady = 5)
Button(c_pts, text = 'reinitialiser', command = delAll, relief = FLAT).pack(side = RIGHT, padx = 5, pady = 5)
c_pts.pack(padx = 10, pady = 5)
c_can = LabelFrame(controls, bg = color1, fg = color2, text = 'Canvas', width = 200)

Button(c_can, text = 'se deplacer', command = lambda:changeCursorMode('mvcan'), relief = FLAT).grid(row = 0, sticky = W, padx = 5, pady = 5)
c_can.pack(padx = 10, pady = 5)
c_crv = LabelFrame(controls, bg = color1, fg = color2, text = 'Courbe', width = 200)

Button(c_crv, text = 'bezier', command = lambda:changeCurveMode('bezier'), relief = FLAT).grid(row = 0, column = 0, padx = 5, pady = 5)
Button(c_crv, text = 'spline²', command = lambda:changeCurveMode('spline'), relief = FLAT).grid(row = 1, column = 0, padx = 5, pady = 5)
Button(c_crv, text = 'spline³', command = lambda:changeCurveMode('splinec'), relief = FLAT).grid(row = 2, column = 0, padx = 5, pady = 5)
Button(c_crv, text = 'bspline', command = lambda:changeCurveMode('bspline'), relief = FLAT).grid(row = 2, column = 1, padx = 5, pady = 5)
Checkbutton(c_crv, text = 'courbe fermee', bg = color1, fg = color2, selectcolor = color1, variable = closedCurve, onvalue = True, offvalue = False, command = getCurve).grid(row = 0, column = 1, padx = 5, pady = 5)
c_crv.pack(padx = 10, pady = 5)

pointSelector = pointSelector()

Button(controls, text='quitter', bg = color1, fg = color2, command = root.quit, relief = FLAT).pack(side = BOTTOM, pady = 10)
Button(controls, text = 'minijeu', bg = color1, fg = color2, command = launchminigame, relief = FLAT).pack(side = BOTTOM, padx = 5, pady = 5)

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
