# Spheres
A framework to create instances of python classes which implement parts of a dependency graph.

During the design of classes, methods can be designated as on-graph, and at run-time become nodes of a dependency graph.  

Invocation of methods becomes dependency-driven (DAG-driven) on a lazy evaluation basis. 
As methods are evaluated and associated DAG nodes are created, 
New objects are fetched transparently and seamlessly and required methods for the these precedent objects are also instantiated on the DAG, and so on, until all nodes have been created and the DAG is complete and valid.
