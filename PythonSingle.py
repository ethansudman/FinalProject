from heapq import heappush, heappop, heapify
from psim import PSim
import math

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
	
	print "Length of links: " + str(len(links))
	print "Length of vertices: " + str(len(vertices))
	
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
			comm.send(vertex, i)
			i = i + 1
	
	else:
		vtx = comm.recv(0)
		for neighbor_id,length in vertex.neighbors:
			neighbor = P[neighbor_id]
			dist = length+vtx.closest_dist
			if neighbor in Q and dist<neighbor.closest_dist:
				neighbor.closest = vertex
				neighbor.closest_dist = dist
		
		
	return [(v.id,v.closest.id,v.closest_dist) for v in P if not v.id==start]
	
#def Dijkstra_p(graph,start):
		#vertices, links = graph
		

vertices = range(10)
links = [(i,j,abs(math.sin(i+j+1))) for i in vertices for j in vertices]
graph = [vertices,links]
links = Dijkstra_p(graph,0)
for link in links: print link