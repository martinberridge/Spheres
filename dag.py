__author__ = 'Martin Berridge, John Barclay & Eirik Hektoen'

"""
Framework for excel-style lazy evaluation of class methods - DagMethod

For compute efficiency, we can follow lazy evaluation similar to "memoization" when values are cached and are only
recalculated when invalidated. In addition to lazy evaluation DagMethods can be overridden i.e. their values set to
constants in the same way that formulas can be overridden in Excel. To reset a DagMethod you invalidate it to force
recalculation. When you change an input to a formula in Excel, that function and dependent functions are recalculated.
If you override a DagMethod in this framework, DagMethods that call it (and are dependent on it by definition) will be
invalidated. The framework maintains a dependency graph (a Directed Acyclic Graph - DAG -  hence the names) like Excel
to work out which dependent DagMethods need to be invalidated.

Exports following classes:

DagMethod - decorator class that wraps members of a class derived from DomObject to give them functionality described
            above.
DagNode -   holds compute state for each DomObject/Dag instance
DomObject - base class for any class that has DagMethod methods. Maintains the DAG which implements the dependency graph
            of DagMethod

"""

# TODO think about clean up after DomObjects/DagMethods destroyed

import networkx
import visualize
import itertools
import collections

node_call_stack = collections.deque()

dependency_graph = networkx.DiGraph()


class DomainObj(object):
    instance_count = itertools.count(0)

    def __init__(self):
        self.id = self.instance_count.next()
        # derived classes may optionally set different, unique names in their __init__ methods
        self._name = self.__class__.__name__ + "_" + str(self.id)


class DagMethod(object):
    # Decorator class which intercepts binding and invocation of DomObject methods to implement lazy
    # evaluation/memoization. Intercepts invocation to inspect state of DagNode object mapped to object/method instance
    # to determine whether to return cached result or rebuild cache by evaluating "curried" copy of DomObject method.
    # Routes invalidation of result cache and and overiding of return value to DagNode object which is stored on an
    # in-memory directed acyclic graph/dependency graph.

    # See http://www.rafekettler.com/magicmethods.html which is the best guide to __???__ methods (i.e. magic methods)
    # and https://docs.python.org/2/reference/datamodel.html#object.__call__

    def __init__(self, method):
        self.method = method
        self.node_map = {}

    def __get__(self, obj, obj_type):
        node = self.node_map.get(obj._name)
        if not node:
            node = DagNode(obj, self.method)
            self.node_map[obj._name] = node
        return node


class DagNode(object):
    def __init__(self, obj, method):
        self.obj = obj
        self.method = method
        self.name = obj._name + "_" + method.func_name
        self.value = None
        self.valid = False
        self.updated = False
        self.x = 0
        self.y = 0
        visualize.add_node(self.x, self.y, self.name)
        update_plot(self)

    def __call__(self, *args, **kwargs):
        if node_call_stack:
            last_node = node_call_stack[-1]
            if not dependency_graph.has_edge(self, last_node):
                dependency_graph.add_edge(self, last_node)
                visualize.add_edge(self.name, last_node.name)
                self.x, self.y = update_layout(self)
        if not self.valid:
            node_call_stack.append(self)
            self.value = self.method(self.obj, *args, **kwargs)
            node_call_stack.pop()
            self.valid = True
            self.updated = False
            update_plot(self)
        return self.value

    def set_value(self, val):
        self.value = val
        self.valid = True
        self.updated = True
        update_plot(self)
        self.notify_dependent_nodes()

    def invalidate(self):
        self.value = None
        self.valid = False
        self.updated = False
        update_plot(self)
        self.notify_dependent_nodes()

    def notify_dependent_nodes(self):
        nodes = dependency_graph.nodes()
        if nodes and self in nodes:
            for node in networkx.descendants(dependency_graph, self):
                node.invalidate()


layout = {}


def update_layout(node):
    if visualize.plot:
        global layout
        layout = networkx.graphviz_layout(dependency_graph)
        return layout[node]
    return 0, 0


def update_plot(node):
    visualize.update_dag_node_plot(node.valid, node.name, node.x, node.y, node.value, node.updated)


def print_graph_edges():
    edges = [(e[1].name, e[0].name) for e in dependency_graph.edges()]
    edges.sort()
    w = max(map(lambda edge: len(edge[0]), edges)) + 4
    last = None
    for edge in edges:
        if edge[0] != last:
            print
            print '{0:{1}}{2}'.format(edge[0], w, edge[1])
            last = edge[0]
        else:
            print '{0:{1}}{2}'.format('', w, edge[1])
