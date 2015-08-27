__author__ = 'martin berridge & john barclay'

"""
Framework for excel-style lazy evaluation of class methods - DagMethod
For compute efficiency, we can follow lazy evaluation similar to "memoization" when values are cached and are only recalculated when invalidated.
In addition to lazy evaluation DagMethods can be overridden i.e. their values set to constants in the same way that formulas can be overridden in Excel.
To reset a DagMethod you invalidate it to force recalculation.
When you change an input to a formula in Excel , that function and dependent functions are recalculated.
If you override a DagMethod in this framework, DagMethods that call it (and are dependent on it by definition) will be invalidated.
The framework maintains a dependency graph (A Directed Acyclic Graph - DAG -  hence the names) like Excel to work out which dependent DagMethods need to be invalidated.

Exports following classes:

DagMethod - decorator class that wrap members of a class derived from DomObject to give them functionality described above.

DomObject - base class for any class that has DagMethod methods. Maintains the DAG which implements the dependency graph of DagMethod

TODO -  usage examples
     -  get update

"""


from networkx import DiGraph
import networkx as nx
import inspect
import functools
import visualize

from client import GephiClient





class DagMethod(object):

# TODO - cleanup?
# valid - we don't need to recalculate
# value - cached return value
# method - function object to be wrapped
# partial - functools partial function object which wraps method see __call__ and __get__
# dag - reference to DAG maintained by DomObject
# function_names - reference to dictionary maintained by DomObject used for parsing method calls and building DAG see __call__ and __get__


    valid = False
    value = None
    method = None
    partial = None
    dag = None
    function_names = None


    def __init__(self, a_dag_method) :

        try:
            if visualize.gephi is None and visualize.plot :
                visualize.gephi = GephiClient('http://localhost:8080/workspace0', autoflush=True)
                visualize.gephi.clean()
        except :
                print "Gephi Not Running"
        finally:
            self.method = a_dag_method
            if visualize.gephi and visualize.plot:
                self.plot_node(self.method.func_name)


# ---------------------------- gephi wrappers -----------------------------------------

    def plot_node(self,name):

        if visualize.gephi and visualize.plot:

            self.x = visualize.x
            self.y = visualize.y
            visualize.node_attributes['label'] = name

            visualize.node_attributes['x'] = visualize.x
            visualize.node_attributes['y'] = visualize.y
            visualize.gephi.add_node(name, **visualize.node_attributes)
            visualize.x += 0 if (visualize.node_count%2) > 0 else  -200 if (visualize.node_count%3) > 2 else 200
            visualize.y += 0 if ((visualize.node_count+1)%2) > 1 else  -200 if ((visualize.node_count+1)%6) > 3 else 200
    #        node_attributes['x'] += 200
    #        node_attributes['x'] +=  0 if (node_count%4) > 1 else  -200 if (node_count%6) > 3 else 200
#            node_attributes['y'] +=  0 if ((node_count+4)%4) > 1 else  -200 if ((node_count+4)%6) > 3 else 200
 #          "0" if (i%4) > 1 else "-" if (i%6) >  3 else "+"
 #          node_attributes['y'] = ( node_count % 2 ) + 100
            visualize.node_count += 1



    def plot_dag_edge(self,id,caller,callee):


        if visualize.gephi and visualize.plot:
            visualize.gephi.add_edge(id,caller, callee)

    def update_dag_node_plot(self):


        if visualize.gephi and visualize.plot:
            visualize.node_attributes['r'] = 0.0 if self.valid else 1.0
            visualize.node_attributes['g'] = 0.5 if self.valid else 0.0
            visualize.node_attributes['b'] = 0.5 if self.valid else 0.0

            visualize.node_attributes['label'] = self.method.func_name + "():\r" + str(self.value)
            visualize.node_attributes['fixed'] = True
            visualize.node_attributes['x'] = self.x
            visualize.node_attributes['y'] = self.y


            visualize.gephi.change_node(self.method.func_name, **visualize.node_attributes )

# --------------------------------------------------------------------------------------
# intercepts method call to implement lazy evaluation.
# see http://www.rafekettler.com/magicmethods.html which is the best guide to __???__ methods (i.e. magic methods) in python
# and https://docs.python.org/2/reference/datamodel.html#object.__call__

    def __call__(self,*args):

        if not self.valid:
#           print ">>recalculating %s<<"%self.method.func_name
           self.value = self.method(*args  )
           self.valid = True

        # self.plot_value()
        # self.plot_dag_node_state()
        self.update_dag_node_plot()
        return self.value

# force recalculation of DagMethod and delete cached value . Think about implementing as @property?
    def invalidate(self):
#        print ">>invalidating %s<<"%self.method.func_name
        self.valid = False
        self.value = None
        self.notify_dependent_nodes(self.partial)
        self.update_dag_node_plot()

    def is_valid(self):
        return  self.valid

#  overrides value returned by DagMethod. call invalidate to get original value by forcing recalculation
    def set_value(self, val):
        self.value = val
        self.valid = True

        self.update_dag_node_plot()
        self.notify_dependent_nodes(self.partial)

# find dependent DagMethods which need to be recalculated when they called.
    def notify_dependent_nodes (self, node):
        if  self.dag.nodes():
            dependents = nx.descendants(self.dag, node)
            for n in dependents : n.invalidate()

# faking a method call so do this in two stages - intercept the function call and return  function object
# which is a partial (wraps a function, simplifies signature ) "monkey patched" with methods to override and invalidate cache
# gets references to function name dictionary and dag from calling class
# gets calling function from stack vi inspect. Calling function is dependent on this function so function and calling function
# form an edge in a Directed Acyclic Graph, this is built up as function as called, on-demand.

    def __get__(self, dom_obj, objtype):

       #if self.dag is None :
        self.dag  = dom_obj.dag

      #  if self.function_names is None :
        self.function_names =  dom_obj.function_names


        a_stack = inspect.stack()
        calling_function = a_stack[1][3]

#       create a standalone function object that holds state: ie can be validated/invalidated, holds cached value
#       bound to
        if self.partial is None :

            self.partial = functools.partial(self.__call__, dom_obj)
            self.partial.invalidate = self.invalidate
            self.partial.set_value = self.set_value
            self.partial.is_valid = self.is_valid

            self.function_names[self.method.func_name]  = self.partial

        if calling_function.startswith('test_'): # kludge for unit testing
                calling_function = 'main'

        if calling_function in ('setUp','tearDown'): # kludge for unit testing
                calling_function = 'main'

        if calling_function not in ( 'main','<module>' ) :
                caller_partial = self.function_names[calling_function]
                if not dom_obj.dag.has_edge(caller_partial, self.partial) :
                    self.plot_dag_edge(visualize.edge_count,self.method.func_name, calling_function)
                    self.dag.add_edge(self.partial, caller_partial)
                    visualize.edge_count += 1


        return self.partial



class DomainObj(object):
    def __init__(self):
        self.dag = DiGraph()
        self.function_names = {}

