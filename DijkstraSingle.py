from priorityDict import priorityDictionary
from psim import PSim

def Dijkstra(G,start,end=None):
	Distances = {}
	Predecessors = {}
	Q = priorityDictionary()
	Q[start] = 0
	
	for v in Q:
		Distances[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			length = Distances[v] + G[v][w]
			if w in Distances:
				if length < Distances[w]:
					raise ValueError, "Found a better path to a final vertex"
			elif w not in Q or length < Q[w]:
				Q[w] = length
				Predecessors[w] = v
	
	return (Distances,Predecessors)

"""
I haven't quite been able to get this working, but the idea is to parallelize the
individual iterations of the Dijkstra algorithm too to increase the parallelization.
"""
def Dijkstra_p(G,start,end=None):
	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0

	comm = PSim(len(Q)+1)

	if comm.rank==0:
		i = 1
		for v in Q:
			D[v] = Q[v]

			if v == end: break

			comm.send(i, v)
			i = i + 1
	else:
		v = comm.recv(0)
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)

