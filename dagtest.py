#!/usr/bin/python
"""
Created on Sun Apr 12 08:53:34 2015

standup test of dag tweak layer and context functionality 
@author: martin berridge
"""

import dag
import unittest

class Delegate(dag.DomainObj):

    def __init__(self):
        super(Delegate,self).__init__()
        self.number_of_calls_to_dosomething = 0

    @dag.DagMethod
    def do_something(self):
        self.number_of_calls_to_dosomething += 1
        return 1

class Delegator(dag.DomainObj):

    def __init__(self):
        super(Delegator,self).__init__()
        self.number_of_calls_to_delegate_dosomething = 0

    @dag.DagMethod
    def delegate(self):
        return None

    @dag.DagMethod
    def delegate_do_something(self):
        self.number_of_calls_to_delegate_dosomething += 1
        things = self.delegate().do_something()
        return "delegate did " + str(things ) + (" thing" if things == 1 else  " things")



class DependentOnTwoClasses(dag.DomainObj):

    def __init__(self):
        super(DependentOnTwoClasses,self).__init__()
        self.number_of_calls_to_total = 0

    @dag.DagMethod
    def Delegate_1(self):
        return None

    @dag.DagMethod
    def Delegate_2(self):
        return None

    @dag.DagMethod
    def Total(self):
        self.number_of_calls_to_total += 1
        return self.Delegate_1().do_something() + self.Delegate_2().do_something()

class OneEdgeDag(dag.DomainObj):

    def __init__(self):
        super(OneEdgeDag,self).__init__()
        self.number_of_calls_to_Top = 0
        self.number_of_calls_to_Bottom = 0

    @dag.DagMethod
    def TopFunction(self):
        self.number_of_calls_to_Top += 1
        return self.BottomFunction() + 5

    @dag.DagMethod
    def BottomFunction(self):
        self.number_of_calls_to_Bottom += 1
        return 1

class TwoEdgeDag(dag.DomainObj):

    def __init__(self):
        super(TwoEdgeDag,self).__init__()
        self.number_of_calls_to_Top = 0
        self.number_of_calls_to_Middle = 0
        self.number_of_calls_to_Bottom = 0

    @dag.DagMethod
    def TopMethod(self):
        self.number_of_calls_to_Top += 1
        return  self.MiddleMethod() + 1

    @dag.DagMethod
    def MiddleMethod(self):
        self.number_of_calls_to_Middle += 1
        return self.BottomMethod() + 1

    @dag.DagMethod
    def BottomMethod(self):
        self.number_of_calls_to_Bottom  += 1
        return 1

class MultipleDependencies(dag.DomainObj):

    def __init__(self):
        super(MultipleDependencies,self).__init__()
        self.number_of_calls_to_Top = 0
        self.number_of_calls_to_Left = 0
        self.number_of_calls_to_Right = 0
        self.number_of_calls_to_Bottom = 0

    @dag.DagMethod
    def Top(self):
        self.number_of_calls_to_Top += 1
        return self.Left() + self.Right()

    @dag.DagMethod
    def Left(self):
        self.number_of_calls_to_Left += 1
        return self.Bottom() + 6

    @dag.DagMethod
    def Right(self):
        self.number_of_calls_to_Right += 1
        return self.Bottom() + 3


    @dag.DagMethod
    def Bottom(self):
        self.number_of_calls_to_Bottom += 1
        return 1


class test_OneEdgeDag(unittest.TestCase):

    def setUp(self):
        self.one_edge = OneEdgeDag()

    def test_evaluated_once_then_cached(self):
        x = self.one_edge.TopFunction()
        self.assertEqual(x,6)
        x = self.one_edge.TopFunction()
        self.assertEqual(self.one_edge.number_of_calls_to_Top,1)
        self.assertEqual(self.one_edge.number_of_calls_to_Bottom,1)

    def test_override_node_then_invalidate(self):
        top_return_value = self.one_edge.TopFunction()
        self.one_edge.BottomFunction.set_value(2)

        top_return_value_after_overriding_downstream_node = self.one_edge.TopFunction()
        self.assertEqual(top_return_value_after_overriding_downstream_node,7)
        self.assertEqual(self.one_edge.number_of_calls_to_Top,2)
        self.assertEqual(self.one_edge.number_of_calls_to_Bottom,1)
        self.one_edge.BottomFunction.invalidate()

        top_return_value = self.one_edge.TopFunction()
        self.assertEqual(top_return_value,6)
        self.assertEqual(self.one_edge.number_of_calls_to_Top,3)
        self.assertEqual(self.one_edge.number_of_calls_to_Bottom,2)

class test_TwoEdgeDag(unittest.TestCase):

    def setUp(self):
        self.two_edge = TwoEdgeDag()

    def test_evaluated_once_then_cached(self):
        x = self.two_edge.TopMethod()
        self.assertEqual(x,3)
        x = self.two_edge.TopMethod()
        self.assertEqual(self.two_edge.number_of_calls_to_Top,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

    def test_override_and_invalidate_middle_node(self):
        x = self.two_edge.TopMethod()
        self.two_edge.MiddleMethod.set_value(3)
        x = self.two_edge.TopMethod()
        self.assertEqual(x,4)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

        self.two_edge.MiddleMethod.invalidate()
        x = self.two_edge.TopMethod()
        self.assertEqual(x,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

    def test_override_and_invalidate_bottom_node(self):
        x = self.two_edge.TopMethod()
        self.two_edge.BottomMethod.set_value(5)
        x = self.two_edge.TopMethod()
        self.assertEqual(x,7)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

        self.two_edge.BottomMethod.invalidate()
        x = self.two_edge.TopMethod()
        self.assertEqual(x,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,2)


    def test_dag_built_from_middle_node(self):
        x = self.two_edge.MiddleMethod()
        self.assertEqual(x,2)
        x = self.two_edge.MiddleMethod()
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

        self.two_edge.BottomMethod.set_value(3)
        x = self.two_edge.MiddleMethod()
        self.assertEqual(x,4)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)

        self.two_edge.BottomMethod.invalidate()

        x = self.two_edge.MiddleMethod()
        self.assertEqual(x,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,2)


    def test_dag_rebuilt_when_higher_level_node_called(self):
        x = self.two_edge.MiddleMethod()
        x = self.two_edge.MiddleMethod()
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)
        x = self.two_edge.TopMethod()
        self.assertEqual(x,3)
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,1)
        x = self.two_edge.TopMethod()
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,1)
        self.two_edge.MiddleMethod.invalidate()
        x = self.two_edge.TopMethod()
        self.assertEqual(self.two_edge.number_of_calls_to_Middle,2)
        self.assertEqual(self.two_edge.number_of_calls_to_Bottom,1)
        self.assertEqual(self.two_edge.number_of_calls_to_Top,2)


class test_MultipleDependencies(unittest.TestCase):

     def setUp(self):
         self.md = MultipleDependencies()

     def test_evaluated_once_then_cached(self):
         x = self.md.Top()
         self.assertEqual(x,11)
         self.assertEqual(self.md.number_of_calls_to_Top,1)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         x = self.md.Top()
         self.assertEqual(self.md.number_of_calls_to_Top,1)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)


     def test_override_and_invalidate_bottom_node(self):
         x = self.md.Top()
         self.assertEqual(x,11)
         self.assertEqual(self.md.number_of_calls_to_Top,1)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         self.md.Bottom.set_value(10)
         self.assertEqual(29,self.md.Top() )
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,2)
         self.assertEqual(self.md.number_of_calls_to_Right,2)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         x = self.md.Top()
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,2)
         self.assertEqual(self.md.number_of_calls_to_Right,2)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)


     def test_override_and_invalidate_left_node(self):
         x = self.md.Top()
         self.assertEqual(x,11)
         self.assertEqual(self.md.number_of_calls_to_Top,1)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         self.md.Left.set_value(10)
         self.assertEqual(14, self.md.Top() )
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         x = self.md.Top()
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)


     def test_override_and_invalidate_right_node(self):
         x = self.md.Top()
         self.assertEqual(x,11)
         self.assertEqual(self.md.number_of_calls_to_Top,1)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         self.md.Right.set_value(10)
         self.assertEqual(17, self.md.Top() )
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)
         x = self.md.Top()
         self.assertEqual(self.md.number_of_calls_to_Top,2)
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)



     def test_dag_build_from_left_node(self):
         x = self.md.Left()
         self.assertEqual(x,7)
         x = self.md.Left()
         self.assertEqual(self.md.number_of_calls_to_Left,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)

         self.md.Bottom.set_value(3)
         x = self.md.Left()
         self.assertEqual(x,9)
         self.assertEqual(self.md.number_of_calls_to_Left,2)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)

         self.md.Left.invalidate()

         x = self.md.Left()
         self.assertEqual(x,9)
         self.assertEqual(self.md.number_of_calls_to_Left,3)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)


     def test_dag_build_from_right_node(self):
         x = self.md.Right()
         self.assertEqual(x,4)
         x = self.md.Right()
         self.assertEqual(self.md.number_of_calls_to_Right,1)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)

         self.md.Bottom.set_value(3)
         x = self.md.Right()
         self.assertEqual(x,6)
         self.assertEqual(self.md.number_of_calls_to_Right,2)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)

         self.md.Right.invalidate()

         x = self.md.Right()
         self.assertEqual(x,6)
         self.assertEqual(self.md.number_of_calls_to_Right,3)
         self.assertEqual(self.md.number_of_calls_to_Bottom,1)


     def test_dag_rebuild_from_higher_node(self):
        x = self.md.Right()
        x = self.md.Right()
        self.assertEqual(x,4)
        self.assertEqual(self.md.number_of_calls_to_Left,0)
        self.assertEqual(self.md.number_of_calls_to_Right,1)
        self.assertEqual(self.md.number_of_calls_to_Bottom,1)
        x = self.md.Top()
        self.assertEqual(x,11)
        self.assertEqual(self.md.number_of_calls_to_Right,1)
        self.assertEqual(self.md.number_of_calls_to_Left,1)
        self.assertEqual(self.md.number_of_calls_to_Bottom,1)
        self.assertEqual(self.md.number_of_calls_to_Top,1)
        x = self.md.Top()
        self.assertEqual(self.md.number_of_calls_to_Right,1)
        self.assertEqual(self.md.number_of_calls_to_Left,1)
        self.assertEqual(self.md.number_of_calls_to_Bottom,1)
        self.assertEqual(self.md.number_of_calls_to_Top,1)
        self.md.Right.invalidate()
        x = self.md.Top()
        self.assertEqual(self.md.number_of_calls_to_Right,2)
        self.assertEqual(self.md.number_of_calls_to_Left,1)
        self.assertEqual(self.md.number_of_calls_to_Bottom,1)
        self.assertEqual(self.md.number_of_calls_to_Top,2)


class test_DependenciesBetweenDomObjectsOfDifferentClasses(unittest.TestCase):

     def setUp(self):
         self.inner = Delegate()
         self.outer = Delegator()

     def test_evaluated_then_cached(self):
         self.outer.delegate.set_value(self.inner)
         self.assertEqual(self.outer.delegate_do_something(),'delegate did 1 thing')
         self.assertEqual(self.outer.number_of_calls_to_delegate_dosomething, 1)
         self.assertEqual(self.inner.number_of_calls_to_dosomething,1)
         x = self.outer.delegate_do_something()
         self.assertEqual(self.outer.number_of_calls_to_delegate_dosomething, 1)
         self.assertEqual(self.inner.number_of_calls_to_dosomething,1)

     def test_overridden_then_invalidated(self):
         self.outer.delegate.set_value(self.inner)
         self.assertEqual(self.outer.delegate_do_something(),'delegate did 1 thing')
         self.assertEqual(self.outer.number_of_calls_to_delegate_dosomething, 1)
         self.assertEqual(self.inner.number_of_calls_to_dosomething,1)
         self.inner.do_something.set_value(5)
         self.assertEqual(self.outer.delegate_do_something(),'delegate did 5 things')
         self.assertEqual(self.outer.number_of_calls_to_delegate_dosomething, 2)
         self.assertEqual(self.inner.number_of_calls_to_dosomething,1)
         self.assertEqual(self.outer.delegate_do_something(),'delegate did 5 things')
         self.assertEqual(self.outer.number_of_calls_to_delegate_dosomething, 2)
         self.assertEqual(self.inner.number_of_calls_to_dosomething,1)

class test_ListOfDomObjects(unittest.TestCase):

    def setUp(self):
         self.delegate_1 = Delegate()
         self.delegate_2 = Delegate()
         self.delegate_3 = Delegate()

         do2c1 = DependentOnTwoClasses()
         do2c1.Delegate_1.set_value(self.delegate_1)
         do2c1.Delegate_2.set_value(self.delegate_2)

         do2c2 = DependentOnTwoClasses()
         do2c2.Delegate_1.set_value(self.delegate_1)
         do2c2.Delegate_2.set_value(self.delegate_2)

         do2c3 = DependentOnTwoClasses()
         do2c3.Delegate_1.set_value(self.delegate_1)
         do2c3.Delegate_2.set_value(self.delegate_3)

         self.objlist = [ do2c1, do2c2, do2c3 ]

    def test_evaluated_once_then_cached(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)


         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)
         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

    def test_override_and_invalidate_whole_list_of_upstream_nodes(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

         self.delegate_1.do_something.set_value(2)

         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,9)
         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,2)

         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,9)
         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,2)

    def test_override_and_invalidate_part_of_list_of_upstream_nodes(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

         self.delegate_2.do_something.set_value(2)
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,8)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,8)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,2)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

    def test_override_and_invalidate_single_upstream_node_in_list(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,1)

         self.delegate_3.do_something.set_value(2)
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,7)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,2)

         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,7)

         self.assertEqual( self.delegate_1.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_2.number_of_calls_to_dosomething,1)
         self.assertEqual( self.delegate_3.number_of_calls_to_dosomething,1 )

         self.assertEqual( self.objlist[0].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[1].number_of_calls_to_total,1)
         self.assertEqual( self.objlist[2].number_of_calls_to_total,2)



# class test_dag(unittest.TestCase ):
#
#     @unittest.skip("not implemented")
#     def  test_initialising_through_keyword_arguments_to_constructors(self):
#         obj = Simple(A=3)
#         print "A:", obj.A()
#         self.assertEquals(self.output.getvalue(), "A: 3")
#         self.output.truncate(0)
#         print "D:", obj.D()
#         self.assertEquals(self.output.getvalue(), "Calculate C\nCalculate D\nD: 10")
#         self.output.truncate(0)
#
#     @unittest.skip("not implemented")
#     def test_can_set(self):
#         obj = CanSetDemo()
#         print "C,D", obj.C(), obj.D()
#         self.assertEquals(self.output.getvalue(), 'calculate C\ncalculate D\nC: 2\nD: 6')
#         self.output.truncate(0)
#         obj.C.setvalue(20)
#         obj.C.clear()

#
#     @unittest.skip("not implemented")
#     def test_referring_to_dag_object(self):
#         self.fail("referring to dag_object not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_chaining_dag_object_references(self):
#         self.fail("chaining dag object references not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_list_comprehension(self):
#         self.fail("list comprehension not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_sorting_lists(self):
#         self.fail("sorting lists not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_sorting_attribute_lists(self):
#         self.fail("sorting attribute lists not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_filtering_lists(self):
#         self.fail("sorting attribute lists not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_eval(self):
#         self.fail("eval not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_off_graph_local_vars(self):
#         self.fail("off graph local vars not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_off_graph_super(self):
#         self.fail("off graph super super not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_off_graph_non_dag_methods(self):
#         self.fail("off graph super non dag methods not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_passing_dag_objects_as_arguments(self):
#         self.fail("passing dag objects not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_tweak(self):
#         self.fail("tweak not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_context(self):
#         self.fail("context not implemented yet ")
#
#     @unittest.skip("not implemented")
#     def test_nested_context(self):
#         self.fail("nested context not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_tweak_layer(self):
#         self.fail("tweak layer not implemented yet" )
#
#     @unittest.skip("not implemented")
#     def test_onchange(self):
#         self.fail("on change not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_pushchannge(self):
#         self.fail("push change not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_onvalidate(self):
#         self.fail("on validate not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_strictchange(self):
#         self.fail("strict change not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_noderef(self):
#         self.fail("node ref not implemented yet")
#
#     @unittest.skip("not implemented")
#     def test_alias(self):
#         self.fail("self not implemented yet")
#
        
def main():
    unittest.main()

if __name__ == "__main__":
    main()

