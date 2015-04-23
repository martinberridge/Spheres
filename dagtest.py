#!/usr/bin/python
"""
Created on Sun Apr 12 08:53:34 2015

standup test of dag tweak layer and context functionality 
@author: martin berridge
"""

import dummydag as dag
import unittest
import sys
from StringIO import StringIO

class Simple (dag.domObj):
    @dag.dagMethod(dag.Stored)
    def A(self):
        return 1 
    
    @dag.dagMethod(dag.Stored)
    def B(self):
        return 2 

    @dag.dagMethod 
    def C(self):
        print 'Calculate C'
        return self.A() + 1
    
    @dag.dagMethod
    def D(self):
        print 'Calculate D'
        return ( self.C() * 2 + self.B())

class CanSetDemo(dag.domObj):
    @dag.dagMethod(dag.Stored)
    def A(self):
        return 1
        
    @dag.dagMethod(dag.Stored)    
    def B(self):
        return 2
        
    @dag.dagMethod(dag.CanSet)
    def C(self):
       print 'calculate C'
       return self.A() + 1
       
    @dag.dagMethod
    def D(self):
        print 'calculate D'
        return ( self.C() * 2 + self.B())
    
class test_dag(unittest.TestCase ): 
    def setUp(self):
        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout
   
    def test_simple_calc(self):
        obj = Simple()
        print "A: ", obj.A()
        self.assertEquals( self.output.getvalue(), 'A:  1\n')
        self.output.truncate(0)

        print "D: ", obj.D()
        self.assertEquals(self.output.getvalue(), "D:  Calculate D\nCalculate C\n6\n")
        print 'calculate D'        
        #obj.A.setvalue(5)
        #self.assertEquals(self.output.getvalue(), "Calculate C Calculate D D: 14")
        #obj.B.setvalue(4)
        #self.assertEquals(self.output.getvalue(), "Calculate C Calculate D D: 16")

    @unittest.skip("not implemented")
    def  test_initialising_through_keyword_arguments_to_constructors(self):
        obj = Simple(A=3)
        print "A:", obj.A()
        self.assertEquals(self.output.getvalue(), "A: 3")
        self.output.truncate(0)
        print "D:", obj.D()
        self.assertEquals(self.output.getvalue(), "Calculate C\nCalculate D\nD: 10")
        self.output.truncate(0)

    @unittest.skip("not implemented")    
    def test_can_set(self):
        obj = CanSetDemo() 
        print "C,D", obj.C(), obj.D() 
        self.assertEquals(self.output.getvalue(), 'calculate C\ncalculate D\nC: 2\nD: 6')
        self.output.truncate(0)
        obj.C.setvalue(20)
        obj.C.clear()          
        
        
        
    @unittest.skip("not implemented")    
    def test_calc_across_classes(self):
        self.fail("calc across classes not implemented yet")
    
    @unittest.skip("not implemented")    
    def test_referring_to_dag_object(self):
        self.fail("referring to dag_object not implemented yet")

    @unittest.skip("not implemented")    
    def test_chaining_dag_object_references(self):
        self.fail("chaining dag object references not implemented yet")
    
    @unittest.skip("not implemented")    
    def test_list_comprehension(self):
        self.fail("list comprehension not implemented yet")
        
    @unittest.skip("not implemented")    
    def test_sorting_lists(self):
        self.fail("sorting lists not implemented yet")
        
    @unittest.skip("not implemented")    
    def test_sorting_attribute_lists(self):
        self.fail("sorting attribute lists not implemented yet")
    
    @unittest.skip("not implemented")    
    def test_filtering_lists(self):
        self.fail("sorting attribute lists not implemented yet")
    
    @unittest.skip("not implemented")    
    def test_eval(self):
        self.fail("eval not implemented yet")
        
    @unittest.skip("not implemented")    
    def test_off_graph_local_vars(self):
        self.fail("off graph local vars not implemented yet ")
        
    @unittest.skip("not implemented")    
    def test_off_graph_super(self):
        self.fail("off graph super super not implemented yet ")
        
    @unittest.skip("not implemented")    
    def test_off_graph_non_dag_methods(self):
        self.fail("off graph super non dag methods not implemented yet ")
        
    @unittest.skip("not implemented")    
    def test_passing_dag_objects_as_arguments(self):
        self.fail("passing dag objects not implemented yet ")
         
    @unittest.skip("not implemented")    
    def test_tweak(self):
        self.fail("tweak not implemented yet ")
    
    @unittest.skip("not implemented")    
    def test_context(self):
        self.fail("context not implemented yet ")
        
    @unittest.skip("not implemented")    
    def test_nested_context(self):
        self.fail("nested context not implemented yet")        
        
    @unittest.skip("not implemented")    
    def test_tweak_layer(self):
        self.fail("tweak layer not implemented yet" )
        
    @unittest.skip("not implemented")    
    def test_onchange(self):
        self.fail("on change not implemented yet")
    
    @unittest.skip("not implemented")    
    def test_pushchannge(self):
        self.fail("push change not implemented yet")

    @unittest.skip("not implemented")    
    def test_onvalidate(self):
        self.fail("on validate not implemented yet")
        
    @unittest.skip("not implemented")    
    def test_strictchange(self):
        self.fail("strict change not implemented yet")
        
    @unittest.skip("not implemented")    
    def test_noderef(self):
        self.fail("node ref not implemented yet")

    @unittest.skip("not implemented")    
    def test_alias(self):
        self.fail("self not implemented yet")
    
        
def main():
    unittest.main()

if __name__ == "__main__":
    main()

