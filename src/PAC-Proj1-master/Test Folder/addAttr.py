import sys

try:
    import networkx as nx
    import matplotlib as mp
except ImportError:
    print('Fail to import networkx! Programing terminates')
    print('Please install by: pip install networkx')
    sys.exit()

import copy

G=nx.DiGraph()
#G.add_node(1, time='5PM', name='Elon')
G.add_node(1)
G.node[1]['name']='Elon'
G.node[1]['time']='1AM'
print(G.nodes())
print(G.node[1]['time'])


seen_attributes = set()
seen_attributes.add('nihao')
#seen_attributes.add('attribute_of_node')

# code here adding nodes

node = 0 #node_to_add
attribute = 'attribute_of_node'

if attribute not in seen_attributes:
    print("not in seen_attributes set")
    G.add_node(node, coord=attribute)
    seen_attributes.add(attribute)
print(seen_attributes)

#for i in range(len(seen_attributes)):
#    print i#len(seen_attributes)


print("nodes numbers: ", nx.number_of_nodes(G))
#mp.draw()