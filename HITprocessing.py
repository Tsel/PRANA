#! /usr/bin/python
#
import csv
from datetime import datetime
import networkx as nx
#
# This file contains routines to process HI-Data
#
def HIT2DiGraph(G, fnEdgeList="", startdate="01.01.1999", enddate="31.12.2011", state=""):
    #
    #assert fnEdgeList=="", "Namen des Files angeben"    
    #
    # Startdatum und Enddatum in datetime.date Objekte umwandeln
    #
    sdate = datetime.strptime(startdate,"%d.%m.%Y").date()
    edate = datetime.strptime(enddate,"%d.%m.%Y").date()
    reader = csv.reader(open(fnEdgeList, "rb"), delimiter=";")
    #
    headerline = reader.next()
    for row in reader:
        domesticTrade=False
        inTimeWindow=False
        inKreis = False
        bnr_nb = row[0]
        bnr_vb = row[1]
        d      = row[2].title()
        volume = row[3]
        date=datetime.strptime(d,"%d%b%Y").date()
        #
        # filter the data according ot the State, the time window and the Federal state
        #
        if(bnr_vb[:3]!="276" or bnr_nb[:3]!="276"): continue
        #
        if(state !="" and bnr_vb[3:8]!=state): continue
        #
        if(date < sdate and date >= edate): continue
        #
        G.add_edge(bnr_vb, bnr_nb)
        #
    print "Zeitraum "+startdate+" bis "+enddate
    print "G has nodes "+str(G.number_of_nodes())
    print "G has edges "+str(G.number_of_edges())


if __name__=="__main__":
    G = nx.DiGraph()
    HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg_sample.csv","01.04.2001","01.12.2001")
    print "Starting HIT2DiGraph "
    #HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg.csv","01.09.2009","01.12.2009") # 8 Jahre in der Untersuchung
    #HIT2DiGraph(G,"/Users/tselhorst/Forschungsprojekte/SliLeBAT/Handelnetz Rinder/Daten/sanHIT_2002-2009dg.csv","01.01.2009","01.11.2009") # 8 Jahre in der Untersuchung
    for e in G.edges():
        print str(e[1])+";"+str(e[0])
    
    


