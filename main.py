#-- import des modules --#
from tkinter import *
from tkinter.ttk import *

#-- creation des fonctions --#
def mv(event):
    pass

def rmv(event):
    pass

def add(event):
    pass

def unknown(event):
    pass

# -- creation des classes --#

#-- programme principal --#
root = Tk()
root.attributes('-zoomed', True)

root_w, root_h = root.winfo_screenwidth(), root.winfo_screenheight()

control_panel = Frame(root, width = root_w//2 -40, height = root_h-40) #creation du panneau de controle

infoCurve = Frame(control_panel) #partie réservée aux paramètres de la courbe
degree = Spinbox(infoCurve, from_ = 1, to = 10, width = 7).pack()
curve_type = Combobox(control_panel, values = ['spline', 'b-spline', 'bezier'], state = 'readonly', width = 7).pack()
infoCurve.pack()

tools = Frame(control_panel)
t_curve = Frame(tools)
Button(t_curve, text = 'deplacer', command = mv).pack()
Button(t_curve, text = 'supprimer', command = rmv).pack()
Button(t_curve, text = 'ajouter', command = add).pack()
t_curve.pack()
t_scene = Frame(tools)
Button(t_scene, text = 'btn1', command = unknown).pack()
Button(t_scene, text = 'btn2', command = unknown).pack()
Button(t_scene, text = 'btn3', command = unknown).pack()
t_scene.pack()
tools.pack()

control_panel.pack(side = LEFT, padx = 20, pady = 20) #fin du panneau de controle

scene = Canvas(root, width = root_w//2, height = root_h-40, bg = 'white')
scene.focus_set()
'''scene.bind("<Button-1>", leftClick)
scene.bind('<B1-Motion>', leftDrag)
scene.bind('<ButtonRelease-1>', releaseLeftClick)'''

scene.pack(side = RIGHT, padx = 20, pady = 20)
root.mainloop()
