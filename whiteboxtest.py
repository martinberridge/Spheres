# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:50:16 2015

@author: Martin Berridge

white box tests for internals of dag/domObj
"""

import  unittest
#in case we want to check whether an invalidated method has been called 
import  mock
import  dag

class Simple(dag.domObj):
   
    @dag.dagMethod
    def A():
        return "Literal A"
        
    @dag.dagMethod
    def B() :
        return "Literal B" 
    
    @dag.dagMethod
    def E():
        return self.A() + " and " + self.B()
    
class TestSimpleDependencyBuilding(unittest.TestCase):
    
    def test_call_literal(self) :
        s = Simple()
        res = s.A()
        self.assertEqual(res, "Literal A")
    
    @unittest.skip("not implemented")    
    def test_uplinks(self):
        pass        
        
    @unittest.skip("not implemented")    
    def test_downlinks(self):   
        pass
    
    @unittest.skip("not implemented")    
    def tests_validate(self):
        pass
    
    @unittest.skip("not implemented")    
    def test_invalidate(self):
        pass        
        
    @unittest.skip("not implemented")    
    def test_valid_function_notcalled(self):       
        pass
    
    @unittest.skip("not implemented")    
    def test_invalid_function_called(self):
        pass
            
def main():
    unittest.main()

if __name__ == "__main__":
    main()
