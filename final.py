from psim import PSim

# Implementation of the Dijkstra algorithm for a single algorithm
from DijkstraSingle import *

def Parallel(V, E, w, s):
	l = V.keys()

	"""
	Create a new process for each start vector.
	
	Note that there is an "extra" because the root process
	does NOT handle any work - it just scatters and gathers
	data.
	"""	
	comm = PSim(len(l) + 1)

	# Scatter
	if comm.rank==0:
		# Loop through all of the processes 
		for i in range(1, len(l)+1):
			comm.send(i, l[i-1])
	else:
		curr = comm.recv(0)
		res = Dijkstra(V, curr)
		comm.send(0, res)

	# Gather
	if comm.rank==0:
		# Loop through all of the processes
		for i in range(1, len(l)+1):
			res = comm.recv(i)
			print ""
			print "Start: " + str(l[i-1])
			print "Path: " + str(res)


G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}

Parallel(G, None, None, None)

"""
def dijkstra(V, E, w, s):
	Vt = s
	# Loop through all of the vertices but the starting/ending one
	for vte in filter(lambda x: not x == Vt, V):
		if (s, vte) in w:
			l[vte] = w[(s, vte)]
		else:
			l[vte] = float("inf")

	#while not Vt =
"""


