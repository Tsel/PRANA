#! /usr/bin/python
#
import networkx as nx
import SNA as na

def get_edge_List(diG):
    for e in diG.edges_iter():
        print str(e[1])+","+str(e[0])
        
def node_Centralities(diG):
    "Calculate and output node Centralities (Graph diG is assumed to be directed)"
    "in deg, out deg , size of out and in component are calculted for nodes"
    "diG is resersed to calculate the out component size"
    rdiG = diG.reverse()
    for node in diG.nodes():
        degout = diG.out_degree(node)
        degin  = diG.in_degree(node)
        #st     = nx.bfs_tree(diG,node)
        #soc    = len(nos)
        #soc    = len(nx.single_source_shortest_path(diG, node))-1
        #sic    = len(nx.single_source_shortest_path(rdiG, node))-1
        print node,degout,degin
        

if __name__=="__main__":
    diG = nx.DiGraph
    fn = "/Users/tselhorst/Forschungsprojekte/SliLeBAT/Handelnetz Rinder/Daten/sanHIT_2002-2009dg.csv"
    #fn = "/Users/tselhorst/Forschungsprojekte/SliLeBAT/Handelnetz Rinder/Daten/Ring.csv"

    diG = na.diGraph_from_File(fn)
    n_cc=nx.closeness_centrality(diG)
    print n_cc
    
    #print "Graph has nodes: "+str(diG.number_of_nodes())
    #print "Graph has edges: "+str(diG.number_of_edges())
    #node_Centralities(diG)
    #rdiG = diG.reverse()
    print "determine strongly connected components"
    #ascc = nx.strongly_connected_components(diG)
    #for x in ascc:
    #    if(len(x)>1):
    #        print len(x)
    # fuer den reversen Graphen
    #ascc = nx.strongly_connected_components(rdiG)
    #for x in ascc:
    #    if(len(x)>1):
    #        print len(x)

