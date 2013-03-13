#! /usr/bin/python##
#
import networkx as nx
import csv
from datetime import datetime

outcomponent = set()

def find_successors_in_time(G, start_node, from_date="",k=0):
    fd = datetime.strptime(from_date.title(),"%d%b%Y").date()
    # outcomponent.add(start_node)
    succ = G.successors(start_node)
    k = k+1
    for n in succ:  # n is a node
        e = (start_node, n)
        dot = G.get_edge_data(*e)["trade_date"]
        ddot = datetime.strptime(dot.title(),"%d%b%Y").date()
        #print ddot
        if(ddot >= fd and n not in outcomponent):
            # if node is selected we add information to the node
#            if('toc' in G.node[n]):
#                G.node[n]['toc'] += ddot-fd
#            else:
#                G.node[n]['toc'] = ddot-fd
            G.node[n]['toc'] = ddot
            G.node[n]['ttc'] = G.node[start_node][ttc] + (ddot-fd)
            G.node[n]['k']=k
            outcomponent.add(n)
            find_successors_in_time(G, n, dot,k)
        if(n in outcomponent):
            print "node present in outcomponent", n
            if(ddot < G.node[n]['toc']):
                print "there exists an earlier contact"
                print n, G.node[n]['toc'], ddot, k
                print "change contatct date and k"
                G.node[n]['toc'] = ddot
                G.node[n]['k'] = k
                G.node[n]['ttc'] = G.node[start_node]['ttc'] + (ddot-fd)
                print "find successors"
                find_successors_in_time(G, n, dot, k)

                       
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
    G = nx.read_edgelist("/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/virtualTrade.csv",delimiter=";",create_using=nx.DiGraph(), nodetype=str, data=(('trade_date',str),))
    print "G has nodes "+str(G.number_of_nodes())
    print "Read start nodes for out component"
    startnodes = getStartNodes(fn="/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/virtualTrade_sources.csv")
    start_date = "01Sep2009"
    for node in startnodes:
        sd = datetime.strptime(start_date.title(),"%d%b%Y").date()
        G.node[node]['toc']=sd
        G.node[node]['ttc']=sd-sd
        G.node[node]['k']=0
        outcomponent.add(node)

    for node in startnodes:
        find_successors_in_time(G,node,start_date,k=0)

    print len(outcomponent)

#    print G.nodes(data=True)
    for n in outcomponent:
        print n, G.node[n]['toc'], G.node[n]['k']
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

