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
import itertools


method_name_node_map = {}
dependency_graph = DiGraph()

def is_at_top_of_call_stack(calling_function):

        return calling_function in ('main','<module>','setUp','tearDown') or  \
               calling_function.startswith('test_')


class DagMethod(object):

# valid - we don't need to recalculate
# value - cached return value
# method - function object to be wrapped
# compute_node - functools compute_node function object which wraps method see __call__ and __get__
# dependency_graph - reference to DAG maintained by DomObject
# function_names - reference to dictionary maintained by DomObject used for parsing method calls and building DAG see __call__ and __get__


    valid = False
    value = None
    method = None
    compute_node = None
    x,y = 0 ,0

    def __init__(self, a_dag_method) :
           self.method = a_dag_method
           if visualize.gephi and visualize.plot:
                self.x = visualize.x
                self.y = visualize.y
                visualize.plot_node(self.x, self.y, self.method.func_name)
# --------------------------------------------------------------------------------------
# intercepts method call to implement lazy evaluation.
# see http://www.rafekettler.com/magicmethods.html which is the best guide to __???__ methods (i.e. magic methods) in python
# and https://docs.python.org/2/reference/datamodel.html#object.__call__
# --------------------------------------------------------------------------------------

    def __call__(self,*args):

        if not self.valid:
           self.value = self.method(*args  )
           self.valid = True
        visualize.update_dag_node_plot(self.valid, self.method.func_name, self.x, self.y, self.value )
        return self.value

# force recalculation of DagMethod and delete cached value . Think about implementing as @property?
    def invalidate(self):
        self.valid = False
        self.value = None
        self.notify_dependent_nodes(self.compute_node)
        visualize.update_dag_node_plot(self.valid, self.method.func_name, self.x, self.y, self.value )

    def is_valid(self):
        return  self.valid

#  overrides value returned by DagMethod. call invalidate to get original value by forcing recalculation
    def set_value(self, val):
        self.value = val
        self.valid = True

        visualize.update_dag_node_plot(self.valid, self.method.func_name, self.x, self.y, self.value )
        self.notify_dependent_nodes(self.compute_node)

# find dependent DagMethods which need to be recalculated when they called.
    def notify_dependent_nodes (self, node):
        if  dependency_graph.nodes():
            dependents = nx.descendants(dependency_graph, node)
            for n in dependents : n.invalidate()


# faking a method call so do this in two stages - intercept the function call and return  function object
# which is a compute_node (wraps a function, simplifies signature ) "monkey patched" with methods to override and invalidate cache
# gets references to function name dictionary and dependency_graph from calling class
# gets calling function from stack vi inspect. Calling function is dependent on this function so function and calling function
# form an edge in a Directed Acyclic Graph, this is built up as function as called, on-demand.

    def __get__(self, dom_obj, objtype):


        the_call_stack = inspect.stack()
        calling_function = the_call_stack[1][3]

#       create a standalone function object that holds state: ie can be validated/invalidated, holds cached value
#       bound to
        if self.compute_node is None :

            self.compute_node = functools.partial(self.__call__, dom_obj)
            self.compute_node.invalidate = self.invalidate
            self.compute_node.set_value = self.set_value
            self.compute_node.is_valid = self.is_valid

            #lookup up compute node by object instance as well as method name
            function_name = dom_obj.my_id() + "_" + self.method.func_name

            method_name_node_map[function_name] = self.compute_node

        if not is_at_top_of_call_stack(calling_function):

            #lookup up compute node by object instance as well as method name

                caller_class =  the_call_stack[1][0].f_locals['self']
                calling_function_name = caller_class.my_id() + "_" +  calling_function

                calling_compute_node = method_name_node_map[calling_function_name]
                if not dependency_graph.has_edge(calling_compute_node, self.compute_node) :
                    visualize.plot_dag_edge(visualize.edge_count,self.method.func_name, calling_function)
                    dependency_graph.add_edge(self.compute_node, calling_compute_node)
                    visualize.edge_count += 1

        return self.compute_node

class DomainObj(object):

    instance_count = itertools.count(0)

    def __init__(self):
        self.id = self.instance_count.next()

    def my_id(self):
        return self.__class__.__name__ + "_" + str(self.id)

