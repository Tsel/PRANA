#! /usr/bin/python
#
import csv
from datetime import datetime
import networkx as nx
#
# This file contains routines to process HI-Data
#
def getNodes4InOutComponents(fnEdgeList="", SID ="", TID =""):
    nodes = set()
    index = 0;
    reader = csv.reader(open(fnEdgeList, "rb"), delimiter=";")
    vIDl=(0,3,5,8,11,15)
    SIDl = len(SID)
    TIDl = len(TID)
    if(SIDl not in vIDl or TIDl not in vIDl):
        print "Malformat (length) >"+SID+"< or >"+TID+"<"
        raise SystemExit(0)

    headerline = reader.next()
    for row in reader:
        rSID = row[0]
        rTID = row[1]
        if(rSID[:SIDl]!=SID or rTID[:TIDl]!=TID):
            continue
        else:
            if(SIDl>0):
#                print rSID
                nodes.add(rSID)
                index += 1
            if(TIDl > 0):
#                print rTID
                nodes.add(rTID)

#    print "Number of nodes " +str(index)
#    print "Number of unique nodes in set "+str(len(nodes))
    for node in nodes:
        print node

def HIT2DiGraph(G, fnEdgeList="", startdate="01.01.1999", enddate="31.12.2011", SID="", TID=""):
    #
    #assert fnEdgeList=="", "Namen des Files angeben"    
    #
    # Startdatum und Enddatum in datetime.date Objekte umwandeln
    #
    sdate = datetime.strptime(startdate,"%d.%m.%Y").date()
    edate = datetime.strptime(enddate,"%d.%m.%Y").date()
    reader = csv.reader(open(fnEdgeList, "rb"), delimiter=";")
    print sdate, edate
    #
#
#   ueber SourceID und TargetID erfolgt der Zugriff auf geografische Einheiten ueber die BNR
#   diese ist wie folgt aufgebaut
#   SSS ll R ll ggg nnnn
#   SSS stellt den Staat dar: 276 fuer Deutschland
#   ll  ist das Bundesland 01 - 16
#   R   ist der Regierungsbezirk
#   ll  ist der Landkreis
#   ggg ist die Gemeindenummer
#   nnnn laufende Nummmer
#
#   SID und TID koennen nur bestimmte Loesngen haben (valid ID lengths [vIDl]), gemaess der obigen Zuordnung
    vIDl = (0, 3, 5, 8, 11, 15)
#   Laengen bestimmen und ueberpruefen
#
    SIDl = len(SID)
    TIDl = len(TID)
    if(SIDl not in vIDl or TIDl not in vIDl):
        print "Malformat (length) >"+SID+"< or >"+TID+"<"
        raise SystemExit(0)

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
        # filter the data according to SID and TID, the time window and the Federal state
        #
        if(bnr_vb[:SIDl]!=SID or bnr_nb[:TIDl]!=TID): continue
        #
        # if(state !="" and bnr_vb[3:8]!=state): continue
        #
#        print str(row) + " is valid"
        if(date < sdate or date >= edate): continue
        #
        #print bnr_vb,bnr_nb,d
        if(G.has_edge(bnr_vb,bnr_nb)==False):
            G.add_edge(bnr_vb, bnr_nb, datum=d)
        #
    print "Zeitraum "+startdate+" bis "+enddate
    print "G has nodes "+str(G.number_of_nodes())
    print "G has edges "+str(G.number_of_edges())


if __name__=="__main__":
    G = nx.DiGraph()
    #HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg.csv","01.09.2009","01.12.2009","276","276")
    getNodes4InOutComponents(fnEdgeList="/Users/tselhorst/Forschungsprojekte/PRANA/Cattle_Trade_01092009_31112009.csv",TID="",SID="27603456")
    #print "Starting HIT2DiGraph "
    #HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg.csv","01.09.2009","01.12.2009") # 8 Jahre in der Untersuchung
    #HIT2DiGraph(G,"/Users/tselhorst/Forschungsprojekte/SliLeBAT/Handelnetz Rinder/Daten/sanHIT_2002-2009dg.csv","01.01.2009","01.11.2009") # 8 Jahre in der Untersuchung
    #trade_date = nx.get_edge_attributes(G,'datum')
    #for e in G.edges():
    #    print str(e[0])+";"+str(e[1])+";"+str(trade_date[(e[0],e[1])])
    
    


