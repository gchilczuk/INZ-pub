import igraph as ig
import random
from collections import Counter
import matplotlib.pyplot as plt


def task1():
	# generate Erdős-Rényi network: number of vertices=100, probability of edges=0.05
	g = ig.Graph.Erdos_Renyi(n=100, p=0.05, directed=False)

	# print graph summary; is graph weighted?
	ig.summary(g)  # something like: IGRAPH U--- 100 xx --
	# there is four-character code at the beginnig; weighted graph would have 'W' at third place

	# list all vertices and edges
	print('Vertices:')
	for vertex in g.vs:
		print(f'vertex {vertex.index}; attributes: {vertex.attributes()}')
	
	print('Edges:')
	for edge in g.es:
		print(f'edge {edge.index}; attributes: {edge.attributes()}')

	# set wegights for all edges at random in range [0.1, 1]
	g.es['weight'] = [(random.randint(10**4, 10**6))/10**6 for _ in range(g.ecount())]

	# print graph summary; is graph weighted?
	ig.summary(g)  # something like: IGRAPH U-W- 100 xx --
	# graph is weighted

	# degrees of vertices
	for v, d in zip(g.vs, g.degree()):
		print(f'({v.index}: {d}), ', end='')

	histogram(Counter(g.degree()))

	# number of clusters (connected components)
	print(g.clusters())
	

def task2():
	# generate Barabási-Albert graph with 1000 vertices
	g = ig.Graph.Barabasi(1000)

def histogram(counter):
	items = sorted(counter.items(), key=lambda x: x[0])
	labels, values = zip(*items)

	indexes = list(range((len(labels))))
	width = 1

	plt.bar(indexes, values, width)
	plt.xticks(indexes, labels)
	plt.show()


if __name__ == '__main__':
	# task1()
	task2()







