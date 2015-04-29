'''
dag is a module which allows DOM objects to be instantiated and computed on an Excel-style directed acyclic graph, or  DAG, 
enabling 
-lazy evaluation, 
- caching, 
- overriding of "literal" (nodes which have no precedents) AND evaluated nodes nodes with override values

domObj - metaclass which creates behaviours for DOM object instances to enable them to have DAG experiences. 
Any object to be instantiated on DAG must inherit from domObj
-

Notes:
1 dag nodes will map to method objects of DOM object instances; in other words an instance of a DOM object will potentially have
many dag nodes, for
-@dagMethod decorated member function (although dag nodes will be created on demand)
-intermediate dag nodes will also be used to expand multi-level dependencies implicit within a method
2 need to create auto-load functionality, where serialised object is fetched and then instantiated in DOM instance. 
Thinking of using 'shelve' which presents a dictionary of objects to save/restore, where you can restore by name

'''

#need to work out bit/xor flag etc.
Stored = True
CanSet = True 

import inspect
import ast  
import shelve

class domObj(object):
    def __init__(self):s
        pass
    def override(self, meth, newval):
        if dagNode.dagnodes.has_key(meth):
            dagNode.dagndes[meth].override = True
            dagNode.dagndes[meth].cached_value = newval
            dagNode.dagndes[meth].valid = True
        else:
            pass
    def remove_override(self,meth):
        pass
        
        
class dagNode(object):
    dagnodes = dict()
    def __init__(self, meth):
        self.valid = False
        self.override = False
        self.literal = False
        self.cached_value = 0.0
        #self.domobj= dom
        self.method = meth
        dagNode.dagnodes[meth]=self 
        self.precedents =[]
        self.dependents = []
    # downlinks returns next level precedents (nodes this node depends on)
    def downlinks(self):
        pass
    # uplinks returns next level dependents (nodes that depend on this node)
    def uplinks(self):
        pass
    # validate non-valid precedents downwards one level
    def validate(self):
        if self.valid : return
        for n in self.downlinks() and not (n.valid):
            n.validate()
        self.dagcode()
        self.valid = True
        
    # invalidate upwards (dependents, and dependents on these, etc.)
    def invalidate(self):
        self.valid = False
        for n in self.uplinks():
            n.invalidate()
    # code which implements the "transformed" DOM method, but on DAG, referring to precedent node values
    def dagcode(self):
        pass
        
# Decorator for DAG methods (methods which are evaluated on/by DAG)
# intercepts method invocations on DOM object instances and returns cached node value if valid 
# else evaluates non-valid precedents and then evaluates self  
def dagMethod(method):
    def dagmethwrapper(self):
        if self.dagnode and self.dagnode.valid:
            return self.dagnode.cached_value
        elif self.dagnode:
            # evaluate ('validate') any invalid precedents
            # evaluate self
            pass
        elif self.dagnode == None:
            self.dagnode = dagNode(method)
            # build the node for this method for "self"
        
#TODO rewrite for attribute params (i.e test for callabaility )    