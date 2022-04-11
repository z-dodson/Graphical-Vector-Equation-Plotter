import tkinter
import tkinter.messagebox
from mpl_toolkits import mplot3d
import numpy
import matplotlib.pyplot as pyplot
from matplotlib.widgets import TextBox

#import windows
from datastructures import Vector3D, VectorFloat, Plane3D, Line3D

colours = ['red','green','blue','yellow','brown','orange','pink']

def getLineLinespace(positionVector, directionVector, l=1):
    x1 = (positionVector[0]+l*directionVector[0])
    x2 = (positionVector[0]-l*directionVector[0])
    y1 = (positionVector[1]+l*directionVector[1])
    y2 = (positionVector[1]-l*directionVector[1])
    z1 = (positionVector[2]+l*directionVector[2])
    z2 = (positionVector[2]-l*directionVector[2])
    return numpy.linspace(x1,x2, 2), numpy.linspace(y1,y2, 2), numpy.linspace(z1,z2, 2)

def getPlaneSpace(directionVector, value):
    detail = 10
    line = Plane3D(*directionVector.get(), value.value)
    if directionVector[2]!=0:
        Xvalues = numpy.linspace(-5,5,detail)
        Yvalues = numpy.linspace(-5,5,detail)
        X,Y = numpy.meshgrid(Xvalues,Yvalues)
        #def func_Z(x,y): return (value.value - (x*directionVector[0])-(y*directionVector[1]))/directionVector[2]
        Z = line.getZvalues(X,Y)
    elif directionVector[1]!=0:
        Xvalues = numpy.linspace(-5,5,detail)
        Zvalues = numpy.linspace(-5,5,detail)
        X,Z = numpy.meshgrid(Xvalues,Zvalues)
        Y = line.getYvalues(X,Z)
    elif directionVector[0]!=0:
        Yvalues = numpy.linspace(-5,5,detail)
        Zvalues = numpy.linspace(-5,5,detail)
        Y,Z = numpy.meshgrid(Yvalues,Zvalues)
        X = line.getYvalues(Y,Z)
    else: 
        alertInvalid()
    return X,Y,Z
def getLMPlaneSpace(directionVector, value):
    detail = 10
    line = Plane3D(*directionVector.get(), value.value)
    Xvalues = numpy.linspace(-5,5,detail)
    Yvalues = numpy.linspace(-5,5,detail)
    X,Y = numpy.meshgrid(Xvalues,Yvalues)
    #def func_Z(x,y): return (value.value - (x*directionVector[0])-(y*directionVector[1]))/directionVector[2]

def alertInvalid(): tkinter.messagebox.showinfo('Invalid input','The input you gave was not recognised')
class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.entryWidth = 50

        self.title("3D vector graph plotting")
        # self.geometry(loc) DONT THINK THIS IS NEEDED
        # self.photo = tkinter.PhotoImage(file="Chat.png")
        # self.iconphoto(False, self.photo)
        self.DND = tkinter.BooleanVar()
        self.entryCount = 2
        if 0:
            self.menubar = tkinter.Menu(self)
            self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
            self.filemenu.add_command(label="Dark mode", command=self.dark)
            self.filemenu.add_command(label="Light mode", command=self.light)
            self.filemenu.add_separator()
            self.filemenu.add_command(label="Copy", command=self.copy)
            self.filemenu.add_checkbutton(label="Silent", variable=self.DND, selectcolor='#961414')
            self.filemenu.add_command(label="Run Windows Bridge", command=start_windows_bridge)
            self.filemenu.add_separator()
            self.filemenu.add_command(label="Restart", command=restart)
            self.filemenu.add_command(label="Exit", command=stop)

            self.menubar.add_cascade(label="Settings", menu=self.filemenu)

            self.config(menu=self.menubar)
        
        # self.l2 = tkinter.Label(self, text=L2TEXT)
        # self.t1 = tkinter.scrolledtext.ScrolledText(self, wrap=tkinter.WORD, state='disabled')
        # packing
        self.frame = tkinter.Frame(self)
        
        self.pack(False)

    def pack(self, refill):
        self.frame.destroy()
        self.frame = tkinter.Frame(self)
        #self.frame['padding'] = (10,10,10,10)
        self.label1 = tkinter.Label(self.frame, text="Enter vectors")
        self.entries = []
        for i in range(self.entryCount):self.entries.append(tkinter.Entry(self.frame, width=self.entryWidth, fg=colours[i]))
        self.clearButton = tkinter.Button(self.frame, text="Clear All", command=self.clear)
        self.addButton = tkinter.Button(self.frame, text="Add entry", command=self.addEntry)
        self.rmButton = tkinter.Button(self.frame, text="Remove entry", command=self.rmEntry)
        self.showButton = tkinter.Button(self.frame, text="SHOW GRAPH", command=self.showGraph)# this will all need to be in one file (sigh)
        self.perpendicularButton = tkinter.Button(self.frame, text="Add perpendicular line", command=self.addPerp)
        self.infoButton = tkinter.Button(self.frame, text="Help", command=self.docs)

        if refill:
            for i in range(len(refill)):
                self.entries[i].insert(0,refill[i])
        self.label1.pack(expand=True)  # scrolled text
        for b in self.entries: b.pack(expand=True)  # do not disturb
        self.clearButton.pack(expand=True)
        self.addButton.pack(expand=True)
        self.rmButton.pack(expand=True)
        self.perpendicularButton.pack(expand=True)
        self.showButton.pack(expand=True)
        
        self.infoButton.pack(expand=True)
        self.frame.pack()

    def addPerp(self): 
        autofill = ""
        for entry in self.entries:
            p = entry.index(tkinter.INSERT)
            if p: autofill = entry.get()
        PerpendicularWindow(self, autofill)
    def addPerp2(self, value): 
        #self.addEntry(value)
        line = getLine(value)
        vector, value = getPerpPlane(*line)
        self.addEntry(f"r.{vector}={value}")

    def docs(self): 
        s=""
        with open(".help.txt","r") as f: n = f.readlines()
        for t in n: s += f"{t}\n"
        tkinter.messagebox.showinfo('Help',s)

    def clear(self): self.pack(False)
    def addEntry(self, value=None): 
        if self.entryCount<=7:
            self.entryCount += 1
            d=self.getData()
            if value: d.append(value)
            self.pack(d)
    def rmEntry(self):
        if self.entryCount>1: 
            self.entryCount -=1
            d=self.getData()
            d.pop()
            self.pack(d)
    def getData(self): 
        info = []
        for n in self.entries: info.append(n.get().strip())
        return info
    def showGraph(self):
        t=self.getData()
        while""in t: t.remove("")
        doStuff(t)
        runMap()

class PerpendicularWindow(tkinter.Tk):
    def __init__(self, parent, autofill):
        super().__init__()
        self.parent = parent
        self.stringValue = ""
        self.plotPlane= True
        self.title("Add a perpedicular line")
        self.frame = tkinter.Frame(self)
        self.label1 = tkinter.Label(self.frame, text="Note: You can only plot a perdendicular plane or line to a line (using the position vector) ")
        self.button1 = tkinter.Button(self.frame, text="Plot plane", command=self.change)
        self.label2 = tkinter.Label(self.frame, text="Enter Line")
        self.entry1 = tkinter.Entry(self.frame, width=30)
        self.button2 = tkinter.Button(self.frame, text="Add", command=self.submit)
        self.entry1.insert(0,autofill)
        self.label1.pack()
        self.button1.pack()
        self.label2.pack()
        self.entry1.pack()
        self.button2.pack()
        self.frame.pack()

    def submit(self):
        self.parent.addPerp2(self.entry1.get())
        self.destroy()

    def change(self): 
        if self.plotPlane: self.button1.config(text="Plot line")
        else: self.button1.config(text="Plot plane")
        self.plotPlane = not self.plotPlane
class MatPlotLibController():
    def __init__(self):
        self.axislength = 15
        self.lines = []
    def plotAxes(self):
        fig = pyplot.figure()# tight?
        self.axes = pyplot.axes(projection ='3d') # 3D graph
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")
        self.axes.set_zlabel("Z")
        self.axes.set_title('Vector Graph Plotter')
        self.axislength = 10
        colour_n = 0

        #     if line[1].max()>self.axislength: self.axislength = line[1].max()

        for line in self.lines: colour_n = self.plot(line, colour_n)
            
        #self.axislength *= 1.2
        xAxis = [numpy.linspace(-self.axislength, self.axislength, 2),numpy.linspace(0, 0, 2),numpy.linspace(0, 0, 2)]#START, STOP, NUM OF POINTS
        yAxis = [numpy.linspace(0, 0, 2),numpy.linspace(self.axislength, -self.axislength, 2),numpy.linspace(0, 0, 2)]#START, STOP, NUM OF POINTS
        zAxis = [numpy.linspace(0, 0, 2),numpy.linspace(0, 0, 2),numpy.linspace(self.axislength, -self.axislength, 2)]#START, STOP, NUM OF POINTS
        self.axes.plot3D(*xAxis, 'black',linewidth=2)
        self.axes.plot3D(*yAxis, 'black',linewidth=2)
        self.axes.plot3D(*zAxis, 'black',linewidth=2)
        pyplot.tight_layout()
        pyplot.show()
    def reset(self): self.lines = []
    def addLine(self, line): self.lines.append(line)

    def plot(self,line, colour_n):
        
        if line[0]=="VECTOR":
            self.axes.text(*line[1].coords(), f"{line[1]}", color=colours[colour_n])
            self.axes.plot3D(*line[1].getVectorLinespace(), colours[colour_n])
        elif line[0]=="LINE":
            self.axes.text(*line[1].coords(), f"r={line[1]}+l{line[2]}", color=colours[colour_n])
            self.axes.plot3D(*getLineLinespace(line[1],line[2]), colours[colour_n])
        elif line[0]=="PLANE":
            self.axes.text(*line[1].coords(), f"r.{line[1]}={line[2]}", color=colours[colour_n])
            self.axes.plot_surface(*getPlaneSpace(line[1],line[2]), color=colours[colour_n],alpha=0.5)
        elif line[0]=="LMPLANE":
            self.axes.text(*line[1].coords(), f"r={line[1]}+l{line[2]}+m{line[3]}", color=colours[colour_n])
            self.axes.plot_surface(*getLMPlaneSpace(line[1],line[2],line[3]), color=colours[colour_n],alpha=0.5)
        return colour_n+1

def doStuff(listofequations):
    controller.reset()
    for equation in listofequations:
        try:
            n = (deduceWhatItIs(equation))
            if n: controller.addLine(n)
            else: alertInvalid()
        except: alertInvalid()
        
def deduceWhatItIs(equation):
    """I feel like this could be a big function"""
    
    if "="in equation:
        if equation[0:2]=="r=": # equation or lambda mu plane
            if "l"in equation:
                if "m" in equation:
                    return ("LMPLANE", *getLMplane(equation))
                else: return ("LINE",*getLine(equation))# LINE
                    
        elif equation[0:3]=="r.[": # simple plane
            return ("PLANE",*getPlane(equation))
    else: # find vector is quite a big thing
        if "[" in equation and "]" in equation: return ("VECTOR", findVector(equation)) 
        # this bit here should be a recursive function
    
def getPlane(equation):
    equation = equation.translate({ord(' '):None}) 
    vector, value = equation[2:].split("=")
    return Vector3D(*vector[1:-1].split(",")), VectorFloat(value)

def getLMPlane(equation):
    equation = equation.translate({ord(' '):None}) 
    equation = equation[2:]
    a,b,c = equation.split("+") # assume they in correct order
    return Vector3D(*a[1:-1].split(",")), Vector3D(*b[2:-1].split(",")), Vector3D(*c[2:-1].split(","))

def getPerpPlane(positionVector, directionVector):
    return directionVector, VectorFloat(positionVector.dot(directionVector))


def getLine(equation):
    """ preperation (cleaning string, etc)"""
    equation = str(equation)
    equation.replace(" ","")
    equation = equation[2:]
    a,b = equation.split("+")
    if "l" in a: a, b = b, a
    b = b.translate({ord('l'):None}) # replace didnt seem to be wroking properly so i used this ..?
    return Vector3D(*(a[1:-1].split(","))), Vector3D(*(b[1:-1].split(",")))

    
def findVector(equation):
    """
    recursiveFunctionForFindingVectorsWithoutEqualls
    Seems to work quite well despite recursion
    """
    #in the order of bidmas
    if"+"in equation:
        parts = equation.split("+")
        tot = Vector3D(0, 0, 0)
        for part in parts: tot = tot + findVector(part)
        return tot
    # UNTIL SUBTRACT WORKS PRPERLY
    # if"-"in equation:
    #     parts = equation.split("-")
    #     first = True
    #     for part in parts: 
    #         if first:
    #             first = False
    #             tot = findVector(part)
    #         else:
    #             tot = tot - findVector(part)
    #     return tot
    elif"*"in equation:
        parts = equation.split("*")
        tot = VectorFloat(1)
        for part in parts: tot = findVector(part) * tot
        return tot
    elif equation[0]=="["and equation[-1]=="]": # breakout cluase
        return Vector3D(*(equation[1:-1].split(",")))
    else:
        return VectorFloat(equation) # int
                
                    
            

def runMap():
    controller.plotAxes()


if __name__=="__main__":
    controller = MatPlotLibController()
    tkwindow = MainWindow()
    tkwindow.mainloop()
