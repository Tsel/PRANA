#! /usr/bin/python##
#
import networkx as nx
import csv
from datetime import datetime
import random as rand
import sys
from collections import defaultdict

outcomponent = set()

def bfs_edges_chrono(G, source):
    """ Produced edges in breadth-first search starting at source considering chronology. """
    # Based on the algorithm described at 
    # http://networkx.github.com/documentation/latest/_modules/networkx/algorithms/traversal/breadth_first_search.html#bfs_successors
    visited = set([source])
    stack = [(source, iter(G[source]))]
    while stack:
        parent, children = stack[0]
        try:
            child = next(children)
            # Edge between parent and child
            e = (parent, child)
            # DoC := Date of Contact
            sDoC = G.get_edge_data(*e)["trade_date"]    # this is a string
            DoC  = datetime.strptime(sDoC.title(),"%d%b%Y").date()
            if child not in visited and DoC >= G.node[parent]["doi"]:
                print "parent -> child, date ", parent, child, DoC
                G.node[child]["doi"] = DoC
                yield parent, child
                visited.add(child)
                stack.append((child,iter(G[child])))
            elif child in visited and DoC < G.node[child]["doi"] and DoC > G.node[parent]["doi"]:
                print "This is an earlier contact ", parent, child, DoC
                print stack
                #print visited
                yield parent,child
                G.node[child]["doi"] = DoC
                #stack.append(child)
        except StopIteration:
            #print "stack "
            #print stack
            stack.pop(0)
            #print "after pop"
            #print stack

def bfs_successors_chrono(G, source):
    d = defaultdict(list)
    for s,t in bfs_edges_chrono(G, source):
        d[s].append(t)
    return dict(d)


def find_successors_in_time(G, start_node, from_date="",k=0):
    fd = datetime.strptime(from_date.title(),"%d%b%Y").date()
    # outcomponent.add(start_node)
    succ = G.successors(start_node)
#    k = k+1
    for n in succ:  # n is a node
#        print "start node is ", start_node
#        print "next node is ", n
        just_added = False
        e = (start_node, n)
        dot = G.get_edge_data(*e)["trade_date"]
        ddot = datetime.strptime(dot.title(),"%d%b%Y").date()
#        print "date from     ", fd
#        print "date of trade ", ddot
        #print ddot
        if(ddot >= fd and n not in outcomponent):
            just_added = True
            print "following ", start_node, n
            G.node[n]['toc'] = ddot
            G.node[n]['doi'] = ddot
            G.node[n]['ttc'] = G.node[start_node]['ttc'] + (ddot-fd)
            G.node[n]['k']=G.node[start_node]['k']+1
            #if(G.node[start_node]['k'] == 0):
            G.node[n]['ID'] = G.node[start_node]['ID']
            outcomponent.add(n)
            find_successors_in_time(G, n, dot,k)
        if (n in outcomponent and just_added==False):
            if( ddot <= G.node[n]['toc']  and ddot >= G.node[start_node]['doi']): #and (G.node[n]['ID'] != G.node[start_node]['ID'])):
                print "this is an earlier contact to ", n
                print "predecessor node is           ", start_node
                print "   k level                    ", G.node[start_node]['k']
                print "   infected at date           ", G.node[start_node]['doi']
                print "   ID(infector)               ", G.node[start_node]['ID']
                print "date of new contact is        ", ddot
                print "date of old contact was       ", G.node[n]['toc']
                print n, G.node[n]['toc'], G.node[n]['k'], G.node[n]['ttc'].days
                print "new node data"
                G.node[n]['toc'] = ddot
                G.node[n]['doi'] = ddot
                G.node[n]['k'] = G.node[start_node]['k']+1
                G.node[n]['ttc'] = G.node[start_node]['ttc'] + (ddot-fd)
                G.node[n]['ID'] = G.node[start_node]['ID']
                print n, G.node[n]['toc'], G.node[n]['k'], G.node[n]['ttc'].days 
                print "find successors of node ",n
                find_successors_in_time(G, n, dot, k)
                print "--------------------------------"
                # 

                       

def getStartNodes(fn=""):
    print "File is " + fn
    reader=csv.reader(open(fn, "rb"), delimiter=";")

    nodes = set()
    for row in reader:
        nodes.add(row[0])

    return nodes
#

def OC2file(G, oc, fn=""):
    writer = csv.writer(open(fn, "wb"))

    writer.writerow(["BNR","ttc","k"])
    for n in oc:
        line = [str(n), str(G.node[n]['ttc'].days), str(G.node[n]['k'])]
        writer.writerow(line)
         
if __name__ == "__main__":
    print "Create network G"
    G = nx.read_edgelist("/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/virtualTrade.csv",delimiter=";",create_using=nx.DiGraph(), nodetype=str, data=(('trade_date',str),))
    print "G has nodes "+str(G.number_of_nodes())
    #SCC = nx.strongly_connected_components(G)
    #lSCC = SCC[0]
    print "Read start nodes for out component"
    startnodes = getStartNodes(fn="/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/virtualTrade_sources.csv")
    start_date = "01Sep2009"
    #for n in startnodes:
    #    print n, G[n]
    #    el = nx.bfs_successors(G,n)
    #    print el
    #noNodesINlSCC=0
    for node in startnodes:
    #    print "node(s) in StartNodes: ",node
    #    if(node in lSCC):
    #        noNodesINlSCC += 1        
    #    if(node not in lSCC)
    #        print node
        sd = datetime.strptime(start_date.title(),"%d%b%Y").date()
        G.node[node]['toc']=sd      # time of contact [date]
        G.node[node]['ttc']=sd-sd   # time to contact [days]
        G.node[node]['k']=0         # infection sequence [0: farms at start]
        G.node[node]['doi']=sd      # date of infection
        G.node[node]['ID']=node     # ID of initial node
    #    outcomponent.add(node)
    #print str(noNodesINlSCC) + " of "+str(len(startnodes)) + " in lSCC"

    #sys.setrecursionlimit(9000)
    for node in startnodes:
        el = bfs_successors_chrono(G, node)
        for s in el:
            for t in el[s]:
                e = (s,t)
                print s, t, G.get_edge_data(*e)["trade_date"]
        #    for t in el[s]
        #        print s, t
    #    find_successors_in_time(G,node,start_date,k=0)


#   Out component to file
    # OC2file(G, outcomponent, fn="/Users/tselhorst/Forschungsprojekte/Rinder/Handelsdaten/OC_S05554.csv")

    #print "Recursion limit"
    #print sys.getrecursionlimit()
    #print "---------------"
    #for n in outcomponent:
    #    print n, G.node[n]['ttc'].days, G.node[n]['k'], G.node[n]['ID']



    #print "out Component size: ", len(outcomponent)
    #print "no start  nodes   : ", len(startnodes)
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

