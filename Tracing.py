#! /usr/bin/python##
#
import networkx as nx
import csv
from datetime import datetime
import random as rand

outcomponent = set()

def find_successors_in_time(G, start_node, from_date="",k=0):
    fd = datetime.strptime(from_date.title(),"%d%b%Y").date()
    # outcomponent.add(start_node)
    succ = G.successors(start_node)
#    k = k+1
    for n in succ:  # n is a node
#        print "start node is ", start_node
#        print "next node is ", n
        e = (start_node, n)
        dot = G.get_edge_data(*e)["trade_date"]
        ddot = datetime.strptime(dot.title(),"%d%b%Y").date()
#        print "date from     ", fd
#        print "date of trade ", ddot
        #print ddot
        if(ddot > fd and n not in outcomponent):
#            print "node added ", n
            # if node is selected we add information to the node
#            if('toc' in G.node[n]):
#                G.node[n]['toc'] += ddot-fd
#            else:
#                G.node[n]['toc'] = ddot-fd
            G.node[n]['toc'] = ddot
            G.node[n]['doi'] = ddot
            G.node[n]['ttc'] = G.node[start_node]['ttc'] + (ddot-fd)
            G.node[n]['k']=G.node[start_node]['k']+1
            outcomponent.add(n)
            find_successors_in_time(G, n, dot,k)
        if (n in outcomponent):
            if(ddot < G.node[n]['toc'] and ddot > G.node[start_node]['doi']):
                print "this is an earlier contact to ", n
                print "predecessor node is           ", start_node
                print "   k level                    ", G.node[start_node]['k']
                print "   infected at date           ", G.node[start_node]['doi']
                print "date of new contact is        ", ddot
                print "date of old contact was       ", G.node[n]['toc']
                print n, G.node[n]['toc'], G.node[n]['k'], G.node[n]['ttc'].days
                print "new node data"
                G.node[n]['toc'] = ddot
                G.node[n]['doi'] = ddot
                G.node[n]['k'] = G.node[start_node]['k']+1
                G.node[n]['ttc'] = G.node[start_node]['ttc'] + (ddot-fd)
                print n, G.node[n]['toc'], G.node[n]['k'], G.node[n]['ttc'].days 
                print "find successors of node ",n
                find_successors_in_time(G, n, dot, k)
                print "--------------------------------"

                       
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
    G = nx.read_edgelist("/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/Cattle_Trade_01092009_31112009.csv",delimiter=";",create_using=nx.DiGraph(), nodetype=str, data=(('trade_date',str),))
    print "G has nodes "+str(G.number_of_nodes())
    #SCC = nx.strongly_connected_components(G)
    #lSCC = SCC[0]
    print "Read start nodes for out component"
    startnodes = getStartNodes(fn="/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/Sources_05554_rs2.csv")
    start_date = "01Sep2009"
    #noNodesINlSCC=0
    for node in startnodes:
        #print "node(s) in StartNodes: ",node
    #    if(node in lSCC):
    #        noNodesINlSCC += 1        
    #    if(node not in lSCC):
    #        print node
        sd = datetime.strptime(start_date.title(),"%d%b%Y").date()
        G.node[node]['toc']=sd      # time of contact [date]
        G.node[node]['ttc']=sd-sd   # time to contact [days]
        G.node[node]['k']=0         # infection sequence [0: farms at start]
        G.node[node]['doi']=sd      # date of infection
        outcomponent.add(node)
    #print str(noNodesINlSCC) + " of "+str(len(startnodes)) + " in lSCC"
    for node in startnodes:
        find_successors_in_time(G,node,start_date,k=0)


#    print G.nodes(data=True)
    for n in outcomponent:
        print n, G.node[n]['ttc'].days, G.node[n]['k']

    print "out Component size: ", len(outcomponent)
    print "no start  nodes   : ", len(startnodes)
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

