# A template for lab 4 - vertex cover approximation in graphs - for CSC 349 at Cal Poly
# Reads a file with a list of edges and outputs the minimum vertex cover to the screen
# Credit: Rodrigo Canaan 
# Adapted with permission from Iris Ho and Theresa Migler

import sys
import math
import collections

# Method and imports to generate all subsets of a collection.
# Useful for the brute force implementation
# DO NOT CHANGE this method
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# Helper graph class. I recommend you do not modify any of the implemented attributes and methods, but feel free to add your own
# Note that since we're not interested in pathfinding, there's no need to record metadata for nodes like pre-numbers, visit flags, components etc. 
class graph:
	def __init__(self,V,E):
		self.V = V
		self.E = E

	def print_graph(self):
		print("Printing graph...")
		for v in self.V:
			if not self.E[v]:
				print("Vertex {} has no neighbors:".format(v))
			else:
				print("Vertex {} neighbors: {}".format(v,self.E[v]))
		print("n = {}".format(self.count_vertices()))
		print("m = {}".format(self.count_edges()))
		print("Graph printed!")
		print()

	# Recommended to use this method to remove edges rather than deleting from E directly
	# If modifying this method, note that when removing (v,u), we also need to remove (u,v)
	def remove_edge(self,v,u):
		self.E[v].remove(u)
		self.E[u].remove(v)

	# Recommended to use this method to remove vertices rather than deleting from V directly
	# If modifying this method, note that we also need to remove all edges
	def remove_vertex(self,v):
		remove = []
		for u in self.E[v]:
			remove.append((v,u))
		for e in remove:
			self.remove_edge(e[0],e[1])
		self.V.remove(v)

	# Returns n, the total number of vertices
	def count_vertices(self):
		n = len(self.V)
		return n

    # Returns the degree of a vertex v
	def degree(self,v):
		d = len(self.E[v])
		return d

	# Returns m, the total number of edges. Edges (v,u) and (u,v) count as a single edge.
	def count_edges(self):
		m=0
		for v in self.V:
			m+= self.degree(v)
		m = int(m/2)
		return m

	# Gets an arbitrary edge
	def get_edge(self):
		for v in self.V:
			if self.degree(v) > 0:
				u = next(iter(self.E[v]))
				return v,u
		raise ValueError("G must have at least one edge!")

# Reads a file and creates the corresponding graph
# Note that as opposed to the strongly connected component assignment, the graph is undirected (so there's a single adjenceny list)
# Another difference is we're not interested in pathfinding, so there's no need for pre-numbers, visit flags, components etc.
# I recommend you DO NOT CHANGE this method, but if you do, note that it is possible for a vertex to have no neighbors. 
def read_file(filename):
	with open(filename) as f:
		lines = f.readlines()
		n = int(lines[0])
		if n<=0:
			raise ValueError("Graph must have at least 1 vertex")
		V = {i for i in range(n)}
		E = {i:set() for i in V} 
		for l in lines[1:]:
			tokens = l.split(",")
			v,u = (int(tokens[0]),int(tokens[1]))	
			E[v].add(u)
			E[u].add(v) 
		return graph(V,E)

# Helper method to print the names of nodes in a given subset
def print_subset(subset):
	print("Subset {}".format([v for v in subset]))

# Helper method that takes a collection of nodes and prints them in a standardized, sorted list format.
def print_cover(cover):
	print(sorted([v for v in cover]))

# Method stub for the brute force algorithm.
# Returns a collection of nodes (not node names!) in the true minimal vertex cover
# Generates all subsets of the nodes in a graph, then checks if they are valid vertex covers, then finally return the valid one with fewest elemnts
# I recommend creating a helper method to check if a subset is a vertex cover (see below)
def bruteforce(G):
	P = powerset(G.V) 
	for subset in P: 
		print_subset(subset) # Make sure you comment out or delete this line for the final submission!
		pass
	return G.V # This is the maximal vertex cover provided as an incorrect example. You want the true minimum cover instead!


# Optional (recommended) method to check if a subset is a vertex cover.
# In a vertex cover, for every vertex v, either v is in the cover, or all its neighbors are
def is_vertex_cover(subset):
	pass

# Method stub for the greedy algorithm
# Returns a log(n)-approximation of the the minimal vertex cover
# Correct behavior: while there are any **edges***, find the vertex with max degree, add it to the cover and remove it from the graph (along with all its edges)
# Method stub incorrect behavior: adds all vertices to the cover and removes it from the graph 
def greedy(G):	
	C = set() # Add nodes of maximum degree here
	while G.V:
		v = next(iter(G.V)) # use this to avoid changing G.V while inside a for loop over G.V
		G.remove_vertex(v)
		C.add(v)
	return C 

# Method stub for the matching algorithm
# Returns a 2-approximation of the the minimal vertex cover
# Correct behavior: while there are any **edges**, selects an arbitrary edge (u,v), adds both u and v to the cover and removes both u and v from the graph
# Method stub incorrect behavior: adds all vertices to the cover and removes it from the graph 
def matching(G):
	C = set() # Add nodes of maximum degree here
	while G.V:
		v = next(iter(G.V)) # use this to avoid changing G.V while inside a for loop over G.V
		G.remove_vertex(v)
		C.add(v)
	return C

def main():
	filename = sys.argv[1]
	mode = sys.argv[2].lower()
	G = read_file(filename)
	G.print_graph() # Make sure you comment out or delete this line for the final submission!ß		
	if mode == "bruteforce" or mode == "1":
		print_cover(bruteforce(G))
	elif mode == "greedy" or mode == "2":
		print_cover(greedy(G))
	elif mode == "matching" or mode == "3":
		print_cover(matching(G))
	else :
		raise ValueError("Mode should be bruteforce, greedy or matching (or 1, 2, 3 respectively)")

if __name__ == '__main__':
	main()
