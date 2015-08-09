__author__ = 'martin berridge'


"""
tweak        - temporary change to DagMethod.
remove tweak - manually restores values changed by tweaks
context      - temporary repository for DagMethod tweaks
             - saves old values at start of with ... block restores old vales at end of with block
"""

tweak_stack = []

current_context = 0


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


# if inside a with block save old value of DagMethod by pushing it onto stack with context id so __exit__ knows which changes to unwind
def tweak( dagmethod , value):
    global current_context
    global tweak_stack

    if current_context > 0 :
        saved_value = dagmethod()
        a_tweak = ( current_context,dagmethod,saved_value)
        tweak_stack.append( a_tweak)

    dagmethod.set_value(value)


def remove_tweak(dagmethod):
    dagmethod.invalidate()

def layer():
    raise NotImplementedError

def create_layer() :
    raise NotImplementedError

