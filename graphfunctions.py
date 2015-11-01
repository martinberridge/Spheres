__author__ = 'martin berridge'

"""
tweak        - temporary change to DagMethod.
remove tweak - manually restores values changed by tweaks
context      - temporary repository for DagMethod tweaks
             - saves old values at start of with ... block restores old vales at end of with block
"""

import itertools

tweak_stack = []
layers = {}
current_context = 0
saved_tweaks = {}
current_layer = 0
# see  https://docs.python.org/2/reference/datamodel.html#context-managers
# for explanation of with statement and context managers
class context (object):

# need to keep track of contexts for nested with statement
    def __enter__(self):
        global current_context
        current_context += 1

# rolls back tweaks for current context i.e at end of with statement block
# unwind teaks by popping changes from stack and reapplying stored values
# TODO better exception handling using exc_ parameters - hard to debug unhandled exceptions in with blocks

    def __exit__(self, exc_type, exc_val, exc_tb):
        global tweak_stack
        global current_context

        while tweak_stack[-1][0] == current_context :
            the_tweak = tweak_stack.pop()
            dagnode = the_tweak[1]
            value = the_tweak[2]
            dagnode.set_value(value)
            if not tweak_stack:
               break

        current_context -= 1


class Layer(object):

    layer_count = itertools.count(1)

    def __init__(self):
       self.layer_id = self.layer_count.next()

    def __enter__(self):
       global layers
       global current_layer

       current_layer = self.layer_id

       if self.layer_id in layers.keys() :
          for dag_method,value in layers[self.layer_id].items() :
              dag_method.set_value(value)

    def __exit__(self, exc_type, exc_val, exc_tb):
       global saved_tweaks, current_layer

       if exc_type is not None:
        print exc_type, exc_val, exc_tb

       for dagmethod in saved_tweaks.keys():
           dagmethod.set_value( saved_tweaks[dagmethod] )
           current_layer = 0

def tweak( dagmethod , value):
    global current_context
    global tweak_stack
    global saved_tweaks
    global current_layer

    if current_context > 0 :
        saved_value = dagmethod()
        a_tweak = ( current_context,dagmethod,saved_value)
        tweak_stack.append( a_tweak)

    if current_layer :
        if dagmethod not in saved_tweaks.keys():
            saved_value = dagmethod()
            saved_tweaks[dagmethod] = saved_value
        if current_layer not in layers.keys():
            layers[current_layer] = {dagmethod:value}
        elif dagmethod not in layers[current_layer].keys():
            layers[current_layer] = {dagmethod:value}
        else :
            layers[current_layer][dagmethod] = value

    dagmethod.set_value(value)



def remove_tweak(dagmethod):
    dagmethod.invalidate()

def layer():
    return Layer()

def create_layer() :
    raise NotImplementedError

