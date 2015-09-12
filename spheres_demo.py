__author__ = 'martin berridge'

import dag, math

class Material (dag.DomainObj):

    @dag.DagMethod
    def density(self):
        return 0.0

    @dag.DagMethod
    def name(self):
        return  0.0

class Sphere (dag.DomainObj):

    @dag.DagMethod
    def material(self):
        return None

    @dag.DagMethod
    def radius(self):
        return 0

    @dag.DagMethod
    def mass(self):
        return 4.0/3.0 * math.pi * self.radius() * self.material().density()

class Container(dag.DomainObj):

    @dag.DagMethod
    def contents(self):
        return []

    @dag.DagMethod
    def mass(self):
        retval = 0
        for c in self.contents():
            retval += c.mass()
        return retval

rubber = Material()
steel = Material()

rubber.density.set_value(1.0)
steel.density.set_value(2.5)

steel_sphere1 = Sphere()
steel_sphere1.material.set_value(steel)
steel_sphere1.radius.set_value(5.0)

steel_sphere2 = Sphere()
steel_sphere2.material.set_value(steel)
steel_sphere2.radius.set_value(15.0)

rubber_sphere = Sphere()
rubber_sphere.material.set_value(rubber)
rubber_sphere.radius.set_value(3.0)

c = Container()
spheres = [steel_sphere1, steel_sphere2,rubber_sphere]
c.contents.set_value(spheres)

# everything recalculated
print c.mass()
# everything cached - no recalc
print c.mass()

rubber.density.set_value(1.5)

# density of rubber reset - mass of rubber sphere and container c ONLY recalculated  - rest cached
print c.mass()
# everything cached - no recalc

print c.mass()

# list member radius reset - mass of one sphere and container c ONLY recalculated - rest cached
spheres[1].radius.set_value(11.2)

print c.mass()
# everything cached - no recalc
print c.mass()

steel.density.set_value(3.798)

#steel density reset two steel spheres and container c recalcuated - but not rubber sphere
print c.mass()
# everything cached - no recalc
print c.mass()
