# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:36:48 2015

@author: martin
"""








import math , random

from mdf import MDFContext, evalnode, varnode

class Location(object):
    Fore, Mid1, Mid2, Aft = range(1,5)
 
class Material(object):
    def __init__(self, name, density):
        self.name = name
        self.density = density
   
    
class Sphere(object):
    
    density = varnode()  
    radius = varnode() 
    
    @evalnode
    def volume(cls):
       return 4/3 * math.pi * cls.radius()      
      
    @evalnode
    def mass(cls):
        return cls.density() * cls.volume()

    
   
def main():
    
   
    ctx1 = MDFContext()
    
    clist=[]
    clist.append(('big', Location.Aft))
    clist.append(('bigger', Location.Mid1))
    clist.append(('small', Location.Mid2))
    clist.append(('medium', Location.Aft))
 
    
    pop = [7000, 15000, 5000, 4000] 
    
    contents = [] 

    m = [Material(n, d) for  n, d in [('cheese', 200), ('steel', 8000), ('mahogany', 3500), ('plastic', 150), ('rubber', 175)]]

    for c,p in zip(clist,pop):
        contents = [(mat.density, rad) for mat, rad in zip([random.choice(m) for i in range(p)], [random.uniform(0.000001, 3.7) for i in range(p)])]
        
    total = 0.0
    
    for c in contents:
        ctx1[Sphere.radius] = 1


        ctx1[Sphere.density] = 1
        total += ctx1[Sphere.mass] 
   
    print total
    
if __name__ == "__main__":
    main()
    
    
    
    