#! /usr/bin/python
#
import csv
from datetime import datetime
import networkx as nx
#
# This file contains routines to process HI-Data
#
def HIT2DiGraph(G, fnEdgeList="", startdate="01.01.1999", enddate="31.12.2011", SID="", TID=""):
    #
    #assert fnEdgeList=="", "Namen des Files angeben"    
    #
    # Startdatum und Enddatum in datetime.date Objekte umwandeln
    #
    sdate = datetime.strptime(startdate,"%d.%m.%Y").date()
    edate = datetime.strptime(enddate,"%d.%m.%Y").date()
    reader = csv.reader(open(fnEdgeList, "rb"), delimiter=";")
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
        print "Malformat (length) "+SID+" or "+TID
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
        print str(row) + " is valid"
        if(date < sdate and date >= edate): continue
        #
        G.add_edge(bnr_vb, bnr_nb)
        #
    print "Zeitraum "+startdate+" bis "+enddate
    print "G has nodes "+str(G.number_of_nodes())
    print "G has edges "+str(G.number_of_edges())


if __name__=="__main__":
    G = nx.DiGraph()
    HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg_sample.csv","01.04.2001","01.12.2001","","27502")
    print "Starting HIT2DiGraph "
    #HIT2DiGraph(G,"/Users/tselhorst/SNA Cattle/r_beweg.csv","01.09.2009","01.12.2009") # 8 Jahre in der Untersuchung
    #HIT2DiGraph(G,"/Users/tselhorst/Forschungsprojekte/SliLeBAT/Handelnetz Rinder/Daten/sanHIT_2002-2009dg.csv","01.01.2009","01.11.2009") # 8 Jahre in der Untersuchung
    for e in G.edges():
        print str(e[1])+";"+str(e[0])
    
    


