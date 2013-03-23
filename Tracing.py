#! /usr/bin/python##
#
'''
File: Tracing.py
Author: Thomas Selhorst <Thomas.Selhorst@fli.bund.de>
Description: 
    This script contains functions for chronological Breadth first search

'''
import networkx as nx
import csv
from datetime import datetime
from collections import defaultdict

outcomponent = set()

def my_bfs_edges_m(G, source):
    """ Adapted procedure to produce edges in breadth-first search statring at source. """
    """ This function is essentially identical to that one at 
        http://networkx.github.com/documentation/latest/_modules/networkx/algorithms/traversal/breadth_first_search.html#bfs_edges 
        There are two exceptiioins: """
   
    """ 1.) In the original function provides a set called visited where all the
    nodes are stored which were, as stated, already visited. This is not needed
    here because the information wheter and when a node was visited is stored
    at the node level.
    2.) The selection of nodes for bfs differs. A node is selected if:
        a) the node has no doi (date of infection), i.e. the node has never
        been selected before
        b) the node is selected again, when there is - in comparison to the old
        date of infection - an earlier date. DoC is the date of contact and if
        DoC < doi of the node, then the node is selected
        c) the node is selected if the infector of this  node has changed
        d) The node will only be selected if the parent node has an doi, and if
        this date of infection is before the actual contact. This guarantees
        that the node can only be infected by an infected parent node """

    stack = [(source, iter(G[source]))]
    while stack:
        parent, children = stack[0]
        try:
            child = next(children)
            e = (parent, child)
            sDoC = G.get_edge_data(*e)["trade_date"]
            DoC  = datetime.strptime(sDoC.title(), "%d%b%Y").date()
            """ this if clause is diffent from the original bfs search
            function. Everything else is identical """
            if ('doi' not in G.node[child] or DoC < G.node[child]['doi'] or (DoC == G.node[child]['doi'] and G.node[child]['Infector'] != G.node[parent]['Infector'])) and (DoC > G.node[parent]['doi']):
                G.node[child]['k'] = G.node[parent]['k']+1
                G.node[child]['doi'] = DoC
                G.node[child]['ttc'] = G.node[parent]['ttc'] + (DoC - G.node[parent]['doi'])
                G.node[child]['Infector'] = G.node[parent]['Infector']
                yield parent, child
                stack.append((child, iter(G[child])))
        except StopIteration:
            stack.pop(0)

def my_bfs_successors(G, source):
    d = defaultdict(list)
    for s,t in my_bfs_edges_m(G, source):
        d[s].append(t)
    return d

def getStartNodes(fn=""):
    """ This function reads a file with the start nodes to be considered"""
    print "File is " + fn
    reader=csv.reader(open(fn, "rb"), delimiter=";")

    nodes = set()
    for row in reader:
        nodes.add(row[0])

    return nodes

def OC2file(G, oc, fn=""):
    """ This function writes the start nodes and the nodes reached by the start
    nodes to a file """
    writer = csv.writer(open(fn, "wb"))

    writer.writerow(["BNR","ttc","k"])
    for n in oc:
        line = [str(n), str(G.node[n]['ttc'].days), str(G.node[n]['k'])]
        writer.writerow(line)
         
if __name__ == "__main__":
    print "Create network G"
    G = nx.read_edgelist("/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/Cattle_Trade_01092009_31112009.csv",delimiter=";",create_using=nx.DiGraph(), nodetype=str, data=(('trade_date',str),))
    print "G has nodes "+str(G.number_of_nodes())
    print "Read start nodes for out component"
    startnodes = getStartNodes(fn="/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/Sources_05554_rs2.csv")
    start_date = "01Sep2009"
    for node in startnodes:
        sd = datetime.strptime(start_date.title(),"%d%b%Y").date()
        G.node[node]['toc']=sd      # time of contact [date]
        G.node[node]['ttc']=sd-sd   # time to contact [days]
        G.node[node]['k']=0         # infection sequence [0: farms at start]
        G.node[node]['doi']=sd      # date of infection
        G.node[node]['Infector']=node     # ID of initial node

    ChronoGraph = nx.DiGraph()
    distinctNodes = set()
    for node in startnodes:
        counter=0
        ccounter = 0
        el = my_bfs_successors(G, node)
        for s in el:
            distinctNodes.add(s)
            for t in el[s]:
                distinctNodes.add(t)
                edge = (s,t)
                sedgeDoC = (G.get_edge_data(*edge)['trade_date'])
                edgeDoC = datetime.strptime(G.get_edge_data(*edge)['trade_date'].title(),"%d%b%Y").date()
                if ChronoGraph.has_node(t):
                    plt = ChronoGraph.predecessors(t)
                    for p in plt:
                        e = (p,t)
                        tedgeDoC = datetime.strptime(ChronoGraph.get_edge_data(*e)['trade_date'].title(),"%d%b%Y").date()
                        if edgeDoC < tedgeDoC:
                            ChronoGraph.remove_edge(*e)
                    if not ChronoGraph.predecessors(t):
                        ChronoGraph.add_edge(s, t, trade_date=sedgeDoC)

                else:
                    ChronoGraph.add_edge(s,t, trade_date=sedgeDoC)

