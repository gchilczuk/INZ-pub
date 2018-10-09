from collections import Counter
from itertools import chain
import matplotlib.pyplot as plt
import random

import igraph as ig
import pandas as pd

def task1():
    # generate Erdős-Rényi network: number of vertices=100, probability of edges=0.05
    g = ig.Graph.Erdos_Renyi(n=100, p=0.05, directed=False)

    # print graph summary; is graph weighted?
    ig.summary(g)  # something like: IGRAPH U--- 100 xx --
    # there is four-character code at the beginning; weighted graph would have 'W' at third place

    # list all vertices and edges
    print('Vertices:')
    for vertex in g.vs:
        print(f'vertex {vertex.index}; attributes: {vertex.attributes()}')
    
    print('Edges:')
    for edge in g.es:
        print(f'edge {edge.index}; attributes: {edge.attributes()}')

    # set weights for all edges at random in range [0.1, 1]
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
    # Erdős-Rényi is the simplest network model, nodes are connected at random,
    # network is undirected, there are no hubs in such network.
    # Edros-Renyi network can grow to be very large but nodes will be just few hops apart
    #
    # In Barabási-Albert model, when a new vertex join network
    # probability of creation of connection to other vertices is proportional to their degree.
    # In such a network it is easy to identify hubs - nodes, the degree of which is high compared to others.


def task3():
    # read data, take columns 0 and 1
    file = pd.read_csv('./manufacturing/manufacturing.csv', sep=';', usecols=[0,1])[1:]
    
    # decrease indexes because vertices in the Graph are indexed form 0
    file -= 1 
    
    #create Graph
    edges = list(zip(file.Sender, file.Recipient))
    g = ig.Graph(edges=edges, directed=True)

    # remove self-loops and multiple edges
    g.simplify()

    # make sure that there are 167 vertices and 5783 edges
    assert len(g.vs) == 167
    assert len(g.es) == 5783

    # information spreading
    betweenness = g.betweenness()
    pagerank = g.pagerank()
    # random vertex
    spdreading_experiment(g, random.choice(g.vs).index, 'random')
    spdreading_experiment(g, random.choice(g.vs).index, 'random')
    # max betweenness
    spdreading_experiment(g, betweenness.index(max(betweenness)), 'max betweenness')
    # min betweenness
    spdreading_experiment(g, betweenness.index(min(betweenness)), 'min betweenness')
    # max pagerank
    spdreading_experiment(g, pagerank.index(max(pagerank)), 'max pagerank')
    # min pagerank
    spdreading_experiment(g, list(reversed(pagerank)).index(min(pagerank)), 'min pagerank')


def spdreading_experiment(graph, initial_id, initial_comment=''):
        g = graph.copy()

        with open('experiment_results', 'a') as output:
            g.vs['activated'] = False
            g.vs[initial_id]['activated'] = True
            for v in g.vs: v['id'] = v.index

            output.write(f'### START ###\t\t{initial_comment}\n'
                f'initial vertex id: {initial_id}\n\n'
                'number of active vertives: 1\n')
            
            for i in range(10):
                active = g.vs.select(activated=True)
                active_ids = [v.index for v in active]
                
                neighbors_ids = set(chain(*[g.neighborhood(vertices=_id, mode=ig.OUT) for _id in active_ids]))
                neighbors = g.vs.select(neighbors_ids).select(activated=False)
                neighbors['activated'] = True

                output.write(f'number of active vertives: {len(neighbors_ids)}\n')

            output.write('### END ###\n\n\n')


def histogram(counter):
    items = sorted(counter.items(), key=lambda x: x[0])
    labels, values = zip(*items)

    indexes = list(range((len(labels))))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes, labels)
    plt.show()


if __name__ == '__main__':
    task1()
    task2()
    task3()






