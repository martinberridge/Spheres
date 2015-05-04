'''
Created on 2 May 2015

@author: jbarclay
'''
'param to decorator is func decorated - decoratee'
def deco(func):
    def byx(self,x):
        return x * func(self,x)
    return byx
        
class Foo(object):
    @deco
    def sq(self,x):
        return x**2
    @deco
    def x2(self,x):
        return x * 2
    
f=Foo(a=1)

print f.sq(2)
print f.x2(3)