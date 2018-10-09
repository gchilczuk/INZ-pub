from collections import Counter
import matplotlib.pyplot as plt
import random

import igraph as ig
import pandas as pd

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

    # visualize graph, use Page Range to determine vertex size\
    vertex_size = [rank * 10**3 for rank in g.pagerank()]
    ig.plot(g, layout=g.layout('fr'), vertex_size=vertex_size)
    

def task2():
    # generate Barabási-Albert graph with 1000 vertices
    g = ig.Graph.Barabasi(1000)

    # visualize graph with Fruchterman-Reingold layout
    ig.plot(g, layout=g.layout('fr'))

    # find vertex with the highest betweenness centrality 
    ebs = g.betweenness()
    max_eb = max(ebs)
    for i, eb in enumerate(ebs):
        if eb == max_eb:
            print(g.vs[i].index)

    # find diameter of the graph
    print(f'diameter: {g.diameter()}')

    # describe differences between Barabási-Albert and Erdős-Rényi graph models
    #
    #
    #


def task3():
    # read data, take columns 0 and 1
    file = pd.read_csv('./manufacturing/manufacturing.csv', sep=';', usecols=[0,1])[1:]
    
    # decrease indexes beacuse vertices in the Graph are indexed form 0
    file -= 1  
    
    #create Graph
    edges = list(zip(file.Sender, file.Recipient))
    g = ig.Graph(edges=edges, directed=True)

    # remove self-loops and multiple edges
    g.simplify()

    # make sure that there is 167 vertices and 5783 edges
    assert len(g.vs) == 167
    assert len(g.es) == 5783

    # information spreading
    g.vs['activated'] = False
    # vertex_size = [rank * 10**3 for rank in g.pagerank()]
    ig.plot(g, layout=g.layout('kk'))

def spdreading_experiment(graph, initial):
        random.choice(g.vs)['activated'] = True
        for _ in range(2):
            active = g.vs.select(activated=True)
            print('a1', len(active))
            print([a.index for a in active])
            neighbors = g.vs.select(*g.neighborhood(vertices=[v.index for v in active], mode='out'))
            print('n1', len(neighbors))
            neighbors['activated'] = True
            print('n2', [a.index for a in neighbors])
            print('r',len(g.vs.select(activated=True)), end='\n\n')







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
    # task2()
    task3()






