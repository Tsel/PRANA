#! /usr/bin/python##
#
import networkx as nx
import csv
from datetime import datetime

outcomponent = set()

def find_successors_in_time(G, start_node, from_date=""):
    fd = datetime.strptime(from_date.title(),"%d%b%Y").date()
    outcomponent.add(start_node)
    succ = G.successors(start_node)
    for n in succ:
        e = (start_node, n)
        dot = G.get_edge_data(*e)["trade_date"]
        ddot = datetime.strptime(dot.title(),"%d%b%Y").date()
        #print ddot
        if(ddot >= fd and n not in outcomponent):
            outcomponent.add(n)
            find_successors_in_time(G, n, dot)
    
    #print len(outcomponent)

def getStartNodes(fn=""):
    print "File is " + fn
    reader=csv.reader(open(fn, "rb"), delimiter=";")

    nodes = set()
    for row in reader:
        nodes.add(row[0])

    return nodes
#
if __name__ == "__main__":
    print "Create network G"
    G = nx.read_edgelist("/Users/tselhorst/Forschungsprojekte/PRANA/Cattle_Trade_01092009_31112009.csv",delimiter=";",create_using=nx.DiGraph(), nodetype=str, data=(('trade_date',str),))
    print "G has nodes "+str(G.number_of_nodes())
    print "Read start nodes for out component"
    startnodes = getStartNodes(fn="/Users/tselhorst/Forschungsprojekte/PRANA/Sources_05554.csv")
    for node in startnodes:
        find_successors_in_time(G,node,"01Sep2009")

    print len(outcomponent)

    for n in outcomponent:
        print n
    #outcomponent = set()
    #print "Calculate all reachable nodes from start nodes"
    #index = 0
    #for node in startnodes:
    #    index += 1
    #    print "Node " +str(index)+node+ " out of " +str(len(startnodes))
    #    component = nx.single_source_shortest_path_length(G, node, cutoff=3)
    #    print len(component)
    #    for node_reached in component:
    #        outcomponent.add(node_reached)
    #    if(index > 5): break
#
    #for node in outcomponent:
    #    print node
#
    #print "Number of nodes reached " + str(len(outcomponent))

