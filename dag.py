
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

DagMethod - decorator class that wraps members of a class derived from DomObject to give them functionality described above.
DagNode -   holds compute state for each DomObject/Dag instance
DomObject - base class for any class that has DagMethod methods. Maintains the DAG which implements the dependency graph of DagMethod

"""


from networkx import DiGraph
import networkx as nx
import inspect
import functools
import visualize
import itertools


method_name_node_map = {}

dependency_graph = DiGraph()

# ------------------------------------------------helpers-----------------------------------
def is_at_top_of_call_stack(calling_function):

        return calling_function in ('main','<module>','setUp','tearDown') or  \
               calling_function.startswith('test_')

# -----------------------------------------------------------------------------------------------



class DagMethod(object):

# Decorator class which intercepts binding and invocation of DomObject methods to implement lazy evaluation/memoization.
# Intercepts invocation to inspect state of DagNode object mapped to object/method instance to determine whether to return
# cached result or rebuild cache by evaluating "curried" copy of DomObject method.
# Routes invalidation of result cache and and overiding of return value to DagNode object which is stored on an in-memory directed acyclic
# graph/dependency graph.

# see http://www.rafekettler.com/magicmethods.html which is the best guide to __???__ methods (i.e. magic methods) in python
# and https://docs.python.org/2/reference/datamodel.html#object.__call__

    cached_method = None
    compute_node = None
    x,y = 0,0

    def __init__(self, a_dag_method) :
           self.current_node_id = None
           self.cached_method = a_dag_method

# ---- helper ----
    def get_requested_node_id(self,dom_obj):
        return dom_obj.my_id() + "_" + self.cached_method.func_name

# ----- intercept referencing of method by class
    def __get__(self, dom_obj, dummy_objtype_parameter):

        global method_name_node_map

        # make key for looking up DagNode
        requested_node_id = self.get_requested_node_id(dom_obj)

        # DagMethod class has only one instance but there can be multiple DomObj instanaces.
        # is the call from a different DomObj instance from before?
        if self.current_node_id != requested_node_id:
            self.current_node_id = requested_node_id
            if requested_node_id not in method_name_node_map:
                #create a DagNode for holding compute state and for loading into dependecy graph
                visualize.plot_node(self.x, self.y,self.current_node_id)
                method_name_node_map[self.current_node_id] = DagNode(self.current_node_id)

        # refresh "curried" function object which routes invocation
        self.compute_node = functools.partial(self.__call__, dom_obj)
        # load dag node so state can be queried and changed
        self.dag_node =  method_name_node_map[self.current_node_id]

        #who's calling this method?
        call_stack = inspect.stack()
        calling_function = call_stack[1][3]

        #if caller is another DagMethod
        if not is_at_top_of_call_stack(calling_function):

                #build key for looking up dependent DagMethod/DagNode
                caller_class =  call_stack[1][0].f_locals['self']
                dependent_dag_node_id = caller_class.my_id() + "_" +  calling_function

                assert(dependent_dag_node_id  in method_name_node_map )
                dependent_dag_node = method_name_node_map[dependent_dag_node_id]

                # add edge to dependency graph
                if not dependency_graph.has_edge(dependent_dag_node, self.dag_node) :
                    visualize.plot_dag_edge(visualize.edge_count,self.current_node_id, dependent_dag_node_id)
                    dependency_graph.add_edge(self.dag_node, dependent_dag_node)
                    visualize.edge_count += 1

        # monkey patch methods for routing state changing methods to DagNode
        self.compute_node.is_valid = self.is_valid
        self.compute_node.invalidate = self.invalidate
        self.compute_node.set_value = self.set_value

        #client can now evaluate Node invoke date method
        return self.compute_node

    def __call__(self,*args):

        if not self.dag_node.valid:
           self.dag_node.value = self.cached_method(*args  )
           self.dag_node.valid = True
        visualize.update_dag_node_plot(self.dag_node.value, self.current_node_id, self.x, self.y, self.dag_node.value )
        return self.dag_node.value

    def invalidate(self):

        self.dag_node.valid = False
        self.dag_node.value = None

        #invalidate/force recalculation
        self.notify_dependent_nodes(self.dag_node)

        visualize.update_dag_node_plot(self.dag_node.value, self.current_node_id, self.x, self.y, self.dag_node.value )

    def is_valid(self):
        return  self.dag_node.valid

#  overrides value returned by DagMethod. call invalidate to get original value by forcing recalculation
    def set_value(self, val):
        self.dag_node.value = val
        self.dag_node.valid = True

        visualize.update_dag_node_plot(self.dag_node.valid, self.current_node_id, self.x, self.y, self.dag_node.value )
        self.notify_dependent_nodes(self.dag_node)

# find dependent DagMethods which need to be recalculated when they called.
    def notify_dependent_nodes (self, node):
        if  dependency_graph.nodes():
            dependents = nx.descendants(dependency_graph, node)
            for n in dependents : n.invalidate()




class DomainObj(object):

    instance_count = itertools.count(0)

    def __init__(self):
        self.id = self.instance_count.next()

    def my_id(self):
        return self.__class__.__name__ + "_" + str(self.id)

class DagNode(object):

    def __init__(self, node_id):
        self.node_id = node_id
        self.valid = False
        self.value = None

    def invalidate(self):
        self.valid = False