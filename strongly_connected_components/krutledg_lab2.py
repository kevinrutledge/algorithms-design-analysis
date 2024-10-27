# A template for lab 2 - strong connectivity in graphs - for CSC 349 at Cal Poly
# Reads a file with a list of edges, then creates one component for each node and outputs it to the screen
# Credit: Rodrigo Canaan 

import sys
import math

class node:

	def __init__(self,name,out_edges,in_edges,previsit, postvisit,component):
		self.name = name
		self.out_edges = out_edges
		self.in_edges = in_edges
		self.previsit = previsit
		self.postvisit = postvisit
		self.component = component

def strong_connectivity(G):
	components = [ [n.name] for n in G]
	sort_component_list(components)
	return components

def sort_component_list(components):
	for c in components:
		c.sort()
	components.sort(key = lambda x: x[0])

def read_file(filename):
	with open(filename) as f:
		lines = f.readlines()
		v = int(lines[0])
		if  v == 0:
			raise ValueError("Graph must have one or more vertices")
		G = list(node(name = i, out_edges=[],in_edges=[],previsit= -1, postvisit=-1, component=None) for i in range(v))
		for l in lines[1:]:
			tokens = l.split(",")
			fromVertex,toVertex = (int(tokens[0]),int(tokens[1]))
			G[fromVertex].out_edges.append(toVertex)
			G[toVertex].in_edges.append(fromVertex)
		return G


# explore_first(G, v, clock):
# Input: A graph G, vertex v, and current clock value
# Output: Returns updated clock value after DFS with previsit and postvisit numbers assigned
# 
#     v.previsit <- clock
#     clock <- clock + 1
#     for neighbor u in v.out_edges:
#         if not u.previsit == -1:
#             clock <- explore_first(G, u, clock)
#     v.postvisit <- clock
#     clock <- clock + 1
#     return clock

def explore_first(G, v, clock):
    v.previsit = clock
    clock += 1
    for u in v.out_edges:
        if G[u].previsit == -1:
            clock = explore_first(G, G[u], clock)
    v.postvisit = clock
    clock += 1
    return clock


# explore_second(G, v, component_num):
# Input: A graph G, vertex v, and current component number
# Output: All reachable vertices from v are assigned to component_num
# 
#     v.component <- component_num
#     for neighbor u in v.in_edges:
#         if u.component is None:
#             explore_second(G, u, component_num)

def explore_second(G, v, component_num):
    v.component = component_num
    for u in v.in_edges:
        if G[u].component is None:
            explore_second(G, G[u], component_num)


# strong_connectivity(G):
# Input: A directed graph G = (V, E) represented as a list of nodes
# 			with out_edges and in_edges
# Output: A list of lists where each inner list represents a strongly
# 			connected component containing vertex names in ascending order,
# 			and components are sorted by their first element
# 
#     clock <- 0
#     for v in G:
#         v.previsit <- -1
#         v.postvisit <- -1
#         v.component <- None
# 
#     for v in G:
#         if v.previsit == -1:
#             clock <- explore_first(G, v, clock)
# 
#     vertices <- sort G by postvisit numbers in descending order
#     component_num <- 0
# 
#     for v in vertices:
#         if v.component is None:
#             explore_second(G, v, component_num)
#             component_num <- component_num + 1
# 
#     components <- create empty lists for each component
#     for v in G:
#         add v.name to components[v.component]
# 
#     sort each component list
#     sort components by first element
#     return components

def strong_connectivity(G):
    clock = 0
    for v in G:
        v.previsit = -1
        v.postvisit = -1
        v.component = None
    
    for v in G:
        if v.previsit == -1:
            clock = explore_first(G, v, clock)
    
    vertices = sorted(G, key=lambda x: x.postvisit, reverse=True)
    component_num = 0
    
    for v in vertices:
        if v.component is None:
            explore_second(G, v, component_num)
            component_num += 1
    
    components = [[] for idx in range(component_num)]
    for v in G:
        components[v.component].append(v.name)
    
    for comp in components:
        comp.sort()
    components.sort(key=lambda x: x[0])
    
    return components


def main():
	filename = sys.argv[1]
	G = read_file(filename)
	components = strong_connectivity(G)
	print(components)
		
		
if __name__ == '__main__':
	main()
