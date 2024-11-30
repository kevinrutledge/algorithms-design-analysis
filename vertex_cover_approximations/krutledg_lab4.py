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
"""
bruteforce(G):
Input: Graph G = (V,E)
Output: Minimum vertex cover C

1. min_cover = V  // Start with all vertices as the minimum cover
2. for each subset S in powerset(V):
     // Check if S is a valid vertex cover
3.   is_cover = true
4.   for each edge (u,v) in E:
5.     if neither u nor v is in S:
6.       is_cover = false
7.       break
8.   if is_cover and |S| < |min_cover|:
9.     min_cover = S
10. return min_cover
"""
def bruteforce(G):
	# Start with all vertices
    min_cover = G.V.copy()
    # Generate all possible subsets
    for subset in powerset(G.V):
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = set(subset)
    return min_cover


# Optional (recommended) method to check if a subset is a vertex cover.
# In a vertex cover, for every vertex v, either v is in the cover, or all its neighbors are
def is_vertex_cover(G, subset):
    # Convert subset to set for O(1) lookup
    cover = set(subset)
    # Check each edge
    for v in G.V:
        for u in G.E[v]:
            # Only check each edge once
            if v < u:
                if v not in cover and u not in cover:
                    return False
    return True

# Method stub for the greedy algorithm
# Returns a log(n)-approximation of the the minimal vertex cover
# Correct behavior: while there are any **edges***, find the vertex with max degree, add it to the cover and remove it from the graph (along with all its edges)
# Method stub incorrect behavior: adds all vertices to the cover and removes it from the graph 
"""
greedy(G):
Input: Graph G = (V,E)
Output: Vertex cover C

1. C = ∅  // Initialize empty cover
2. E' = E  // Copy of edges
3. while E' ≠ ∅:
4.   v = vertex with maximum degree in G
5.   C = C ∪ {v}
6.   Remove v and all incident edges from G
7. return C
"""
def greedy(G):
    C = set()  # Initialize empty cover
    # Work on a copy of the graph
    G_copy = graph(G.V.copy(), {v: G.E[v].copy() for v in G.V})
    
    while G_copy.count_edges() > 0:
        # Find vertex with maximum degree
        max_degree = -1
        max_vertex = None
        for v in G_copy.V:
            degree = G_copy.degree(v)
            if degree > max_degree:
                max_degree = degree
                max_vertex = v
        
        # Add to cover and remove from graph
        C.add(max_vertex)
        G_copy.remove_vertex(max_vertex)
    
    return C

# Method stub for the matching algorithm
# Returns a 2-approximation of the the minimal vertex cover
# Correct behavior: while there are any **edges**, selects an arbitrary edge (u,v), adds both u and v to the cover and removes both u and v from the graph
# Method stub incorrect behavior: adds all vertices to the cover and removes it from the graph 
"""
matching(G):
Input: Graph G = (V,E)
Output: Vertex cover C

1. C = ∅  // Initialize empty cover
2. while E ≠ ∅:
3.   Pick any edge (u,v) from E
4.   if degree(u) < degree(v):
5.       Add v to C  // Add higher degree vertex
6.       Remove v and all its incident edges from G
7.   else:
8.       Add u to C  // Add higher degree vertex 
9.       Remove u and all its incident edges from G
10. return C
"""
def matching(G):
	# Initialize empty cover
    C = set()
    G_copy = graph(G.V.copy(), {v: G.E[v].copy() for v in G.V})
    
    # Find leaf edges (edges to vertices with degree 1)
    while G_copy.count_edges() > 0:
        # Get any remaining edge
        u, v = G_copy.get_edge()
        
        # Choose which vertex to include based on degree
        if G_copy.degree(u) < G_copy.degree(v):
			# Add the higher degree vertex
            C.add(v)
			  # Remove it and its edges
            G_copy.remove_vertex(v)
        else:
			# Add higher degree vertex
            C.add(u)
			# Remove it and its edges
            G_copy.remove_vertex(u)
    
    return C

def main():
	filename = sys.argv[1]
	mode = sys.argv[2].lower()
	G = read_file(filename)
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