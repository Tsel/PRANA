#! /usr/bin/python
#
import csv
from collections import Counter
import networkx as nx
import matplotlib
from matplotlib import rc
from matplotlib.backends.backend_agg import FigureCanvasAgg as  FigureCanvas
from matplotlib.figure import Figure
#import matplotlib.mlab as mlab


def diGraph_from_File(fn = ""):
    print("Input file: "+fn)
    lines = 0
    G = nx.DiGraph()
    reader = csv.reader(open(fn, "rb"), delimiter=";")
    for row in reader:
        lines+=1
        G.add_edge(row[1],row[0]) # this has to be changed to [1][0]
        
    print(str(lines)+" lines read")
    return G

def degree(G):
    #
    # get the in_degree distribution of nodes
    #
    print "This calculates the degrees of the nodes"

    deg = Counter()
    for node in G.nodes():
        deg[G.degree(node)] += 1
        
    edgeSum = sum(deg.values())
    N = edgeSum
    #
    # dictionary for plotting
    #
    d = dict()
    #
    # sortieren nach keys und Ausgabe
    #
    keylist = deg.keys()
    keylist.sort()
    for key in keylist:
        rcdf = float(edgeSum)/float(N)
        d[key]=rcdf
        #print(key, edgeSum, rcdf)
        edgeSum -= deg[key]
        
    return d

def plot(d):
    rc('text', usetex=True)
    rc('font', family='serif')
    print("Create a plot... ")
    fig = Figure(figsize=(11.6,8.2))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'Degree x',fontsize=18)
    ax.set_ylabel(r'$P(X \ge x)$',fontsize=18)
    ax.set_yscale('log')
    ax.set_xscale('log')
    # x = float(d.keys())
    # y = float(d.values())
    ax.scatter(d.keys(),d.values(),s=20,color='DarkSlateBlue',label='2002')
    ax.legend()
    canvas.print_pdf("/Users/tselhorst/SNA Cattle/test.pdf")
    print("Plot saved to pdf-file")
    
def mplot(dy):
    colors = {2009:"#FD0006",2008:"#FE3F44", 2007:"#FFD200", 2006:"#FFE673", 2005:"#6EE768", 2004:"#42E73A", 2003:"#866FD7", 2002:"#402C84"}
    rc('text', usetex=True)
    rc('font', family='serif')
    print("Create a plot... ")
    fig = Figure(figsize=(11.6,8.2))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'Degree $x$',fontsize=18)
    ax.set_ylabel(r'$P(X \ge x)$',fontsize=18)
    ax.set_yscale('log')
    ax.set_xscale('log')
    yd = {}
    for year in dy:
        yd = dy[year]
        print("Color code is: "+ colors[year])
        ax.scatter(yd.keys(), yd.values(),s=5,color=colors[year], label = str(year))
    
    ax.legend()
    canvas.print_pdf("/Users/tselhorst/SNA Cattle/test_all_years.pdf")
    print("Plot saved to pdf-file")

def process_dictdict(dd):
    yd = {}
    for year in dd:
        yd = dd[year]
        print("Year is: "+str(year))
        for deg in yd:
            print(deg, yd[deg])
#
#
#

if __name__ == '__main__':
    #
    # Build the network from data
    # data file does not contain header
    #
    G2002 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2002.csv")
    G2003 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2003.csv")
    G2004 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2004.csv")
    G2005 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2005.csv")
    G2006 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2006.csv")
    G2007 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2007.csv")
    G2008 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2008.csv")
    G2009 = diGraph_from_File("/Users/tselhorst/SNA Cattle/edgeLists/r_T_S_2009.csv")
    #
    # create a dictionary of dictionaries
    #
    degree_year={}
    d_2002 = degree(G2002)
    d_2003 = degree(G2003)
    d_2004 = degree(G2004)
    d_2005 = degree(G2005)
    d_2006 = degree(G2006)
    d_2007 = degree(G2007)
    d_2008 = degree(G2008)
    d_2009 = degree(G2009)
    degree_year[2002]=d_2002
    degree_year[2003]=d_2003
    degree_year[2004]=d_2004
    degree_year[2005]=d_2005
    degree_year[2006]=d_2006
    degree_year[2007]=d_2007
    degree_year[2008]=d_2008
    degree_year[2009]=d_2009
#   plot(d_2002)
#    mplot(degree_year)
#    process_dictdict(degree_year)
    mplot(degree_year)
