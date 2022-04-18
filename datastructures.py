
import numpy
class Vector3D():
    """I am aware that python has classes that do this, but for me it amkes more sense to make it myself"""
    def __init__(self, a, b, c) -> None: self.a, self.b, self.c = float(a), float(b), float(c)
    def __str__(self) -> str: return f"[{int(self.a)},{int(self.b)},{int(self.c)}]"
    def __repr__(self) -> str: return f"[{int(self.a)},{int(self.b)},{int(self.c)}]"
    def __add__(self,other): return Vector3D(self.a+other.a, self.b+other.b, self.c+other.c)
    def __sub__(self,other): return Vector3D(self.a-other.a, self.b-other.b, self.c-other.c)
    def __mul__(self,other): return Vector3D(self.a*other.value, self.b*other.value, self.c*other.value)
    def dot(self,other): return self.a*other.a+self.b+other.b+self.c*other.c
    def coords(self): return self.a, self.b, self.c
    def __abs__(self): return (self.a**2+self.b**2+self.c**2)**0.5
    def get(self): return self.a, self.b, self.c
    def __getitem__(self,i):
        if i==0: return self.a
        elif i==1: return self.b
        elif i==2: return self.c
    def gettype(self): return "Vector3D"
    def getVectorLinespace(self): return numpy.linspace(0,self.a, 2), numpy.linspace(0, self.b, 2), numpy.linspace(0, self.c, 2)
    def max(self):
        if self.a>self.b:
            if self.a>self.c: max = self.a
            else: max = self.c
        else:
            if self.b> self.c: max = self.b
            else: max = self.c
        return abs(max)
    def maxPos(self):
        if self.a>self.b:
            if self.a>self.c: max = 0
            else: max = 2
        else:
            if self.b> self.c: max = 1
            else: max = 2
        return max
class VectorFloat():
    """This allows floats to be mutilplies by vectors"""
    def __init__(self, value):
        self.value = float(value)
    def __add__(self,other): return VectorFloat(self.value+other.value)
    def __sub__(self,other): return VectorFloat(self.value-other.value)
    def gettype(self): return "VectorFloat"
    def __mul__(self, other): 
        if other.gettype()=="Vector3D": return Vector3D(self.value*other.a, self.value*other.b, self.value*other.c)
        else: return VectorFloat(self.value*other.value)
    def __str__(self) -> str: return f"{self.value}"
    def __repr__(self) -> str: return f"{self.value}"

class Line3D():
    def __init__(self,a1,a2,a3,b1,b2,b3):
        self.a1, self.a2, self.a3, self.b1, self.b2, self.b3 = a1,a2,a3,b1,b2,b3
    def __str__(self) -> str: 
        if self.a1>0: A=f"{self.a1}+{self.b2}"
        elif self.a1<0: A=f"{self.a1}{self.b2}"
        elif self.a1==0: A=f"{self.a1}"
        if self.b1!=1: A = f"({A})/{self.b1}"

        if self.a2>0: B=f"{self.a2}+{self.b2}"
        elif self.a2<0: B=f"{self.a2}{self.b2}"
        elif self.a2==0: B=f"{self.a2}"
        if self.b2!=1: B = f"({B})/{self.b2}"

        if self.a3>0: C =f"{self.a3}+{self.b3}"
        elif self.a3<0: C =f"{self.a3}{self.b3}"
        elif self.a3==0: C=f"{self.a3}"
        if self.b3!=1: C = f"({C})/{self.b3}"
        return f"{A}={B}={C}"
class Plane3D():
    """ax+by+cz=d"""
    def __init__(self,a,b,c,d): self.a, self.b, self.c, self.d = a, b, c, d
    def getXvalues(self, y, z): return (self.d-(y*self.b)-(z*self.c))/self.a
    def getYvalues(self, x, z): return (self.d-(x*self.a)-(z*self.c))/self.b
    def getZvalues(self, x, y): return (self.d-(x*self.a)-(y*self.b))/self.c
class Point3D():
    """I am aware that python has classes that do this, but for me it amkes more sense to make it myself"""
    def __init__(self, a, b, c) -> None: self.a, self.b, self.c = float(a), float(b), float(c)
    def __str__(self) -> str: return f"({self.a},{self.b},{self.c})"
    def __repr__(self) -> str: return f"({self.a},{self.b},{self.c})"
    def __getitem__(self,i):
        if i==0: return self.a
        elif i==1: return self.b
        elif i==2: return self.c
    def coords(self): return self.a, self.b, self.c
    def max(self):
        if self.a>self.b:
            if self.a>self.c: max = self.a
            else: max = self.c
        else:
            if self.b> self.c: max = self.b
            else: max = self.c
        return abs(max)
    def maxPos(self):
        if self.a>self.b:
            if self.a>self.c: max = 0
            else: max = 2
        else:
            if self.b> self.c: max = 1
            else: max = 2
        return max
