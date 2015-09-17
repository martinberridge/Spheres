__author__ = 'martin'

import urllib2

from client import GephiClient


plot = False

gephi = None
node_attributes = {"size":50, 'r':1.0, 'g':0.0, 'b':0.0, 'x':1,'y':0, 'fixed':True  }
node_count = 0
edge_count = 0
x = 0
y = 0


def enable():
    global gephi,plot
    if gephi is None:
        try:
            gephi = GephiClient('http://localhost:8080/workspace0', autoflush=True)
            gephi.clean()

        except urllib2.URLError:
            print "Gephi Not Running"

    plot = True

def update_dag_node_plot(valid, function_name, x, y, value, updated ):

        if gephi and plot:

            RED,GREEN, BLUE = 0,1,2

            red = (1.0, 0.0, 0.0)
            bluegreen = (0.0, 0.5, 0.5)
            amethyst = (0.6, 0.4, 0.8)

            colour = red

            if valid :
                colour = bluegreen

            if updated :
                colour = amethyst

            node_attributes['r'] = colour[RED]
            node_attributes['g'] = colour[GREEN]
            node_attributes['b'] = colour[BLUE]

            node_attributes['label'] = function_name + "():\r" + str(value)
            node_attributes['fixed'] = True
            node_attributes['x'] = x
            node_attributes['y'] = y

            gephi.change_node(function_name, **node_attributes )

def plot_dag_edge(id,caller,callee):

    if gephi and plot:
        gephi.add_edge(id,caller, callee)
        
        
def calculate_plot_coordinates():
    global x,y
    x += 0 if (node_count % 2) > 0 else  -200 if (node_count % 3) > 2 else 200
    y += 0 if ((node_count + 1) % 2) > 1 else  -200 if ((node_count + 1) % 6) > 3 else 200


def plot_node(x, y ,name):

    if gephi and plot:

        node_attributes['r'] = 1.0
        node_attributes['g'] = 0.0
        node_attributes['b'] = 0.0

        node_attributes['label'] = name
        node_attributes['x'] = x
        node_attributes['y'] = y
        gephi.add_node(name, **node_attributes)

        calculate_plot_coordinates()
