from heapq import heappush, heappop, heapify
from psim import PSim
import math

"""
def Dijkstra_p(graph, start):
	vertices, links = graph
	
	P = [PrimVertex(i,links) for i in vertices]
	Q = [P[i] for i in vertices if not i==start]
	vertex = P[start]
	vertex.closest_dist = 0
	
	comm = PSim(len(vertices) - 1)
	
	if comm.rank==0:
		heapify(Q)
		
		i = 1
		while Q:
			vertex = heappop(Q)

			comm.send(i, vertex)
			i = i + 1

	else:
		vtx = comm.recv(0)

		print vtx.id
		for neighbor_id,length in vertex.neighbors:

			neighbor = P[neighbor_id]
			dist = length+vtx.closest_dist
			if neighbor in Q and dist<neighbor.closest_dist:

				neighbor.closest = vertex
				neighbor.closest_dist = dist	

	return [(v.id,v.closest.id,v.closest_dist) for v in P if not v.id==start]
"""

class PrimVertex(object):
	INFINITY = 1e100
	def __init__(self,id,links):
			self.id = id
			self.closest = None
			self.closest_dist = PrimVertex.INFINITY
			self.neighbors = [link[1:] for link in links if link[0]==id]

	def __cmp__(self,other):
		return cmp(self.closest_dist, other.closest_dist)
		
def Dijkstra(graph, start):
	vertices, links = graph
	P = [PrimVertex(i,links) for i in vertices]
	Q = [P[i] for i in vertices if not i==start]
	vertex = P[start]
	vertex.closest_dist = 0
	while Q:
		for neighbor_id,length in vertex.neighbors:
			neighbor = P[neighbor_id]
			dist = length+vertex.closest_dist
			if neighbor in Q and dist<neighbor.closest_dist:
				neighbor.closest = vertex
				neighbor.closest_dist = dist
		heapify(Q)
		vertex = heappop(Q)
	return [(v.id,v.closest.id,v.closest_dist) for v in P if not v.id==start]
	
def Dijkstra_p(graph, start):
	vertices, links = graph

	# This number is a little arbitrary.
	proc = len(vertices) if len(vertices) < 5 else 5
	#comm = PSim(proc)

	P = [PrimVertex(i,links) for i in vertices]
	Q = [P[i] for i in vertices if not i==start]
	vertex = P[start]
	vertex.closest_dist = 0
	#if comm.rank==0:
	while Q:
		# Number to divide
		procL=len(vertex.neighbors)/proc
		for i in range(proc):
			start = i*procL
			# todo handle odd case
			# No need to subtract 1 because range function does that for us
			end = start+procL

			for j in range(start, end):
				neighbor_id, length = vertex.neighbors[j]

				print "(neighbor_id: " + str(neighbor_id) + ", length: " + str(length) + ")"
				neighbor = P[neighbor_id]
				dist = length + vertex.closest_dist
				if neighbor in Q and dist<neighbor.closest_dist:
					neighbor.closest = vertex
					neighbor.closest_dist = dist
		heapify(Q)
		vertex = heappop(Q)

		return [(v.id,v.closest.id,v.closest_dist) for v in P if not v.id==start]

vertices = range(10)
links = [(i,j,abs(math.sin(i+j+1))) for i in vertices for j in vertices]
graph = [vertices,links]
#normal = Dijkstra(graph, 0)
parallel = Dijkstra_p(graph,0)

#print "******************************************************************"
#print "Parallel:"
#for link in parallel: print link
#print ""
#print "******************************************************************"
#for link in normal: print link
