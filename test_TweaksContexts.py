__author__ = 'Owner'

import unittest
import graphfunctions as gf
from dagtest import Delegate,Delegator,DependentOnTwoClasses,MultipleDependencies,OneEdgeDag,TwoEdgeDag

class TweakOneEdgeDag(unittest.TestCase):

    def test_tweak_and_restore_bottom_node(self):
        oed = OneEdgeDag()
        self.assertEquals(oed.TopFunction(),6)
        with gf.context():
            gf.tweak(oed.BottomFunction,8)
            self.assertEquals(oed.TopFunction(),13)
            self.assertEquals(oed.number_of_calls_to_Bottom,1)
            self.assertEquals(oed.number_of_calls_to_Top,2)
        self.assertEquals(oed.TopFunction(),6)
        self.assertEquals(oed.number_of_calls_to_Bottom,1)
        self.assertEquals(oed.number_of_calls_to_Top,3)

    def test_tweak_bottom_node_and_restore_nested_once(self):
        oed = OneEdgeDag()
        self.assertEquals(oed.TopFunction(),6)
        with gf.context():

            gf.tweak(oed.BottomFunction,8)
            self.assertEquals(oed.TopFunction(),13)

            with gf.context():
                gf.tweak(oed.BottomFunction,-1)
                self.assertEquals(oed.TopFunction(),4)
                self.assertEquals(oed.number_of_calls_to_Bottom,1)
                self.assertEquals(oed.number_of_calls_to_Top,3)

        self.assertEquals(oed.TopFunction(),6)
        self.assertEquals(oed.number_of_calls_to_Bottom,1)
        self.assertEquals(oed.number_of_calls_to_Top,4)

    def test_tweak_bottom_node_and_restore_nested_twice(self):
        oed = OneEdgeDag()
        self.assertEquals(oed.TopFunction(),6)
        with gf.context():
            gf.tweak(oed.BottomFunction,8)
            self.assertEquals(oed.TopFunction(),13)
            with gf.context():
                gf.tweak(oed.BottomFunction,-1)
                self.assertEquals(oed.TopFunction(),4)

                with gf.context():
                    gf.tweak(oed.BottomFunction,16)
                    self.assertEquals(oed.TopFunction(),21)
                    self.assertEquals(oed.number_of_calls_to_Bottom,1)
                    self.assertEquals(oed.number_of_calls_to_Top,4)

        self.assertEquals(oed.TopFunction(),6)
        self.assertEquals(oed.number_of_calls_to_Bottom,1)
        self.assertEquals(oed.number_of_calls_to_Top,5)

class TweakTwoEdgeDag(unittest.TestCase):

    def test_tweak_bottom_node_and_restore(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.BottomMethod,8)
            self.assertEquals(ted.TopMethod(),10)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Top,3)

    def test_tweak_bottom_node_nested_once(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.BottomMethod,8)
            self.assertEquals(ted.TopMethod(),10)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
            with gf.context():
                gf.tweak(ted.BottomMethod,9)
                self.assertEquals(ted.TopMethod(),11)
                self.assertEquals(ted.number_of_calls_to_Bottom,1)
                self.assertEquals(ted.number_of_calls_to_Top,3)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Top,4)

    def test_tweak_bottom_node_nested_twice(self):

        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.BottomMethod,8)
            self.assertEquals(ted.TopMethod(),10)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
            with gf.context():
                gf.tweak(ted.BottomMethod,9)
                self.assertEquals(ted.TopMethod(),11)
                self.assertEquals(ted.number_of_calls_to_Bottom,1)
                self.assertEquals(ted.number_of_calls_to_Top,3)
                with gf.context():
                    gf.tweak(ted.BottomMethod,-1)
                    self.assertEquals(ted.TopMethod(),1)
                    self.assertEquals(ted.number_of_calls_to_Bottom,1)
                    self.assertEquals(ted.number_of_calls_to_Top,4)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Top,5)


    def test_tweak_middle_node_and_restore(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.MiddleMethod,8)
            self.assertEquals(ted.TopMethod(),9)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Middle,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,1)
        self.assertEquals(ted.number_of_calls_to_Top,3)

    def test_tweak_middle_node_nested_once(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.MiddleMethod,8)
            self.assertEquals(ted.TopMethod(),9)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Middle,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
            with gf.context():
                gf.tweak(ted.MiddleMethod,9)
                self.assertEquals(ted.TopMethod(),10)
                self.assertEquals(ted.number_of_calls_to_Bottom,1)
                self.assertEquals(ted.number_of_calls_to_Middle,1)
                self.assertEquals(ted.number_of_calls_to_Top,3)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,1)
        self.assertEquals(ted.number_of_calls_to_Top,4)

    def test_tweak_middle_node_nested_twice(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.MiddleMethod,8)
            self.assertEquals(ted.TopMethod(),9)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Middle,1)
            self.assertEquals(ted.number_of_calls_to_Top,2)
            with gf.context():
                gf.tweak(ted.MiddleMethod,9)
                self.assertEquals(ted.TopMethod(),10)
                self.assertEquals(ted.number_of_calls_to_Bottom,1)
                self.assertEquals(ted.number_of_calls_to_Middle,1)
                self.assertEquals(ted.number_of_calls_to_Top,3)
                with gf.context():
                    gf.tweak(ted.MiddleMethod,-1)
                    self.assertEquals(ted.TopMethod(),0)
                    self.assertEquals(ted.number_of_calls_to_Bottom,1)
                    self.assertEquals(ted.number_of_calls_to_Middle,1)
                    self.assertEquals(ted.number_of_calls_to_Top,4)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,1)
        self.assertEquals(ted.number_of_calls_to_Top,5)

    def test_tweak_bottom_node_then_middle_node_in_same_context(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.BottomMethod,8)
            self.assertEquals(ted.TopMethod(),10)
            gf.tweak(ted.MiddleMethod,9)
            self.assertEquals(ted.TopMethod(),10)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Middle,2)
            self.assertEquals(ted.number_of_calls_to_Top,3)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,3)
        self.assertEquals(ted.number_of_calls_to_Top,4)

    def test_tweak_middle_node_then_bottom_node_in_same_context(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
            gf.tweak(ted.MiddleMethod,9)
            self.assertEquals(ted.TopMethod(),10)
            gf.tweak(ted.BottomMethod,8)
            self.assertEquals(ted.TopMethod(),10)
            self.assertEquals(ted.number_of_calls_to_Bottom,1)
            self.assertEquals(ted.number_of_calls_to_Middle,2)
            self.assertEquals(ted.number_of_calls_to_Top,3)

        self.assertEquals(ted.TopMethod(), 3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,2)
        self.assertEquals(ted.number_of_calls_to_Top,4)

    def test_tweak_bottom_node_then_middle_node_in_successive_contexts(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
           gf.tweak(ted.BottomMethod,3)
           self.assertEquals(ted.TopMethod(),5)
           with gf.context():
              gf.tweak(ted.MiddleMethod,6)
              self.assertEquals(ted.TopMethod(),7)
        self.assertEquals(ted.TopMethod(),3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,3)
        self.assertEquals(ted.number_of_calls_to_Top,4)

    def test_tweak_middle_node_then_bottom_node_in_successive_context(self):
        ted = TwoEdgeDag()
        self.assertEquals(ted.TopMethod(),3)
        with gf.context():
           gf.tweak(ted.MiddleMethod,6)
           self.assertEquals(ted.TopMethod(),7)
           with gf.context():
              gf.tweak(ted.BottomMethod,3)
              self.assertEquals(ted.TopMethod(),5)
        self.assertEquals(ted.TopMethod(),3)
        self.assertEquals(ted.number_of_calls_to_Bottom,1)
        self.assertEquals(ted.number_of_calls_to_Middle,2)
        self.assertEquals(ted.number_of_calls_to_Top,4)





class Tweak_Multiple_Dependencies(unittest.TestCase):

    def test_tweak_bottom_node(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom ,3)
           self.assertEquals(md.Top(),15)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,3)
        self.assertEqual(md.number_of_calls_to_Right,3)
        self.assertEquals(md.number_of_calls_to_Top,3)

    def test_tweak_bottom_node_nested_once(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom, 3)
           self.assertEquals(md.Top() ,15)
           with gf.context():
              gf.tweak(md.Bottom ,4)
              self.assertEquals(md.Top(),17)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,4)
        self.assertEqual(md.number_of_calls_to_Right,4)
        self.assertEquals(md.number_of_calls_to_Top,4)

    def test_tweak_bottom_node_nested_twice(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom, 3)
           self.assertEquals(md.Top() ,15)
           with gf.context():
              gf.tweak(md.Bottom ,4)
              self.assertEquals(md.Top(),17)
              with gf.context():
                 gf.tweak(md.Bottom ,-1)
                 self.assertEquals(md.Top(),7)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,5)
        self.assertEqual(md.number_of_calls_to_Right,5)
        self.assertEqual(md.number_of_calls_to_Top, 5)

    def test_tweak_left_node(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Left ,3)
           self.assertEquals(md.Top(),7)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,3)

    def test_tweak_left_node_nested_once(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Left ,3)
           self.assertEquals(md.Top(),7)
           with gf.context():
              gf.tweak(md.Left ,-1)
              self.assertEquals(md.Top(),3)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,4)

    def test_tweak_left_node_nested_twice(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Left ,3)
           self.assertEquals(md.Top(),7)
           with gf.context():
              gf.tweak(md.Left ,-1)
              self.assertEquals(md.Top(),3)
              with gf.context():
                 gf.tweak(md.Left ,5)
                 self.assertEquals(md.Top(),9)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,5)

    def test_tweak_right_node(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Right ,8)
           self.assertEquals(md.Top(),15)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,3)


    def test_tweak_right_nested_once(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Right ,-7)
           self.assertEquals(md.Top(),0)
           with gf.context():
              gf.tweak(md.Right ,8)
              self.assertEquals(md.Top(),15)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,4)

    def test_tweak_right_node_nested_twice(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Right ,0)
           self.assertEquals(md.Top(),7)
           with gf.context():
              gf.tweak(md.Right ,-1)
              self.assertEquals(md.Top(),6)
              with gf.context():
                 gf.tweak(md.Right , 5)
                 self.assertEquals(md.Top(), 12)
        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,1)
        self.assertEqual(md.number_of_calls_to_Right,1)
        self.assertEqual(md.number_of_calls_to_Top,5)

    def test_tweak_bottom_right_left_node_same_context(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom ,0)
           self.assertEquals( md.Top(),9)
           gf.tweak(md.Right ,-1)
           self.assertEquals(md.Top(),5)
           gf.tweak(md.Left ,7)
           self.assertEquals( md.Top(),6)

        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,3)
        self.assertEqual(md.number_of_calls_to_Right,3)
        self.assertEqual(md.number_of_calls_to_Top,5)

    def test_tweak_bottom_left_in_same_context_right_node_different_context(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom ,0)
           self.assertEquals( md.Top(),9)
           gf.tweak(md.Left ,2)
           self.assertEquals( md.Top(),5 )
           with gf.context():
              gf.tweak(md.Right, -1 )
              self.assertEquals( md.Top() ,1)
           self.assertEquals( md.Top(),5 )

        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,3)
        self.assertEqual(md.number_of_calls_to_Right,3)
        self.assertEqual(md.number_of_calls_to_Top,6)

    def test_tweak_bottom_left_right_node_in_successive_contexts(self):
        md = MultipleDependencies()
        self.assertEquals(md.Top(),11)
        with gf.context():
           gf.tweak(md.Bottom ,0)
           self.assertEquals( md.Top(),9)
           with gf.context():
              gf.tweak(md.Left ,2)
              self.assertEquals( md.Top(),5 )
              with gf.context():
                 gf.tweak(md.Right, -1 )
                 self.assertEquals( md.Top() ,1)
              self.assertEquals( md.Top(),5 )
           self.assertEquals( md.Top(),9 )

        self.assertEqual(md.Top(),11)
        self.assertEqual(md.number_of_calls_to_Bottom,1)
        self.assertEqual(md.number_of_calls_to_Left,3)
        self.assertEqual(md.number_of_calls_to_Right,3)
        self.assertEqual(md.number_of_calls_to_Top,7)


class TestTweakTwoDomObjectsOfDifferentClasses(unittest.TestCase):

    def test_tweak_delegate(self):
        inner = Delegate()
        outer = Delegator()
        outer.delegate.set_value(inner)
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')
        with gf.context():
            gf.tweak(inner.do_something,"tweaked")
            self.assertEqual(outer.delegate_do_something(),'delegate did tweaked things')
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')

    def test_tweak_delegate_nested_once(self):
        inner = Delegate()
        outer = Delegator()
        outer.delegate.set_value(inner)
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')
        with gf.context():
            gf.tweak(inner.do_something,"tweaked")
            self.assertEqual(outer.delegate_do_something(),'delegate did tweaked things')
            with gf.context():
                gf.tweak(inner.do_something,"nested tweak")
                self.assertEqual(outer.delegate_do_something(),'delegate did nested tweak things')
            self.assertEqual(outer.delegate_do_something(),'delegate did tweaked things')
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')

    def test_tweak_delegate_nested_twice(self):
        inner = Delegate()
        outer = Delegator()
        outer.delegate.set_value(inner)
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')
        with gf.context():
            gf.tweak(inner.do_something,"tweaked")
            self.assertEqual(outer.delegate_do_something(),'delegate did tweaked things')
            with gf.context():
                gf.tweak(inner.do_something,"nested tweak")
                self.assertEqual(outer.delegate_do_something(),'delegate did nested tweak things')
                with gf.context():
                    gf.tweak(inner.do_something,"nested nested tweak")
                    self.assertEqual(outer.delegate_do_something(),'delegate did nested nested tweak things')
            self.assertEqual(outer.delegate_do_something(),'delegate did tweaked things')
        self.assertEqual(outer.delegate_do_something(),'delegate did 1 thing')


class TestTweakListOfDomObjects(unittest.TestCase):

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

    def test_tweak_node_that_invalidates_one_list_item_only(self):

         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         with gf.context():
            gf.tweak(self.delegate_3.do_something,2)

            total = 0
            for o in self.objlist:
                total += o.Total()

         self.assertEqual(total,7)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

    def test_tweak_node_that_invalidates_one_list_item_only_nested_once(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         with gf.context():
            gf.tweak(self.delegate_3.do_something,2)

            total = 0
            for o in self.objlist:
                total += o.Total()
            self.assertEqual(total,7)

            with gf.context():
                gf.tweak(self.delegate_3.do_something,3)
                total = 0
                for o in self.objlist:
                    total += o.Total()
                self.assertEqual(total,8)

            total = 0

            for o in self.objlist:
                total += o.Total()

            self.assertEqual(total,7)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)


    def test_tweak_node_that_invalidates_one_list_item_only_nested_twice(self):
         total = 0
         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         with gf.context():
            gf.tweak(self.delegate_3.do_something,2)

            total = 0
            for o in self.objlist:
                total += o.Total()
            self.assertEqual(total,7)

            with gf.context():
                gf.tweak(self.delegate_3.do_something,3)
                total = 0
                for o in self.objlist:
                    total += o.Total()
                self.assertEqual(total,8)

                with gf.context():
                    gf.tweak(self.delegate_3.do_something,4)
                    total = 0
                    for o in self.objlist:
                        total += o.Total()
                    self.assertEqual(total,9)

                total = 0

                for o in self.objlist:
                    total += o.Total()

                self.assertEqual(total,8)


            total = 0

            for o in self.objlist:
                total += o.Total()

            self.assertEqual(total,7)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

    def test_tweak_node_that_invalidates_two_list_items(self):

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

         with gf.context():
            gf.tweak(self.delegate_2.do_something,2)

            total = 0
            for o in self.objlist:
                total += o.Total()

         self.assertEqual(total,8)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

    def test_tweak_node_that_invalidates_two_list_items_nested_once(self):

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total, 6)

         with gf.context():
            gf.tweak(self.delegate_2.do_something, 2)

            total = 0
            for o in self.objlist:
                total += o.Total()

            self.assertEqual(total,8)

            with gf.context():
               gf.tweak(self.delegate_2.do_something, 5)

               total = 0
               for o in self.objlist:
                   total += o.Total()

               self.assertEqual(total,14)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)

    def test_tweak_node_that_invalidates_two_list_items_nested_twice(self):

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total, 6)

         with gf.context():
            gf.tweak(self.delegate_2.do_something, 2)

            total = 0
            for o in self.objlist:
                total += o.Total()

            self.assertEqual(total,8)

            with gf.context():
               gf.tweak(self.delegate_2.do_something, 5)

               total = 0
               for o in self.objlist:
                   total += o.Total()

               self.assertEqual(total,14)

               with gf.context():
                   gf.tweak(self.delegate_2.do_something, 8)

                   total = 0
                   for o in self.objlist:
                       total += o.Total()

                   self.assertEqual(total,20)

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total,6)


    def test_tweak_nodes_in_successive_contexts(self):

         total = 0

         for o in self.objlist:
            total += o.Total()
         self.assertEqual(total, 6)

         with gf.context():
            gf.tweak(self.delegate_1.do_something, 2)

            total = 0
            for o in self.objlist:
                total += o.Total()

            self.assertEqual(total,9)

            with gf.context():
               gf.tweak(self.delegate_2.do_something, 5)

               total = 0
               for o in self.objlist:
                   total += o.Total()

               self.assertEqual(total,17)

               with gf.context():
                   gf.tweak(self.delegate_3.do_something, 8)

                   total = 0
                   for o in self.objlist:
                       total += o.Total()

                   self.assertEqual(total,24)

               total = 0

               for o in self.objlist:
                   total += o.Total()

               self.assertEqual(total,17)


         total = 0

         # for o in self.objlist:
         #    total += o.Total()
         # self.assertEqual(total,9)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

