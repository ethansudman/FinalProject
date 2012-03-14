# Note that I didn't write this code - I am only using it temporarily

from priodict import priorityDictionary

def Dijkstra(G,start,end=None):
	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)

def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path

#G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}

#print Dijkstra(G, 'y')

