from psim import PSim

def dijkstra(V, E, w, s):
	Vt = s
	# Loop through all of the vertices but the starting/ending one
	for vte in filter(lambda x: not x == Vt, V):
		if (s, vte) in w:
			l[vte] = w[(s, vte)]
		else:
			l[vte] = float("inf")

	#while not Vt =


