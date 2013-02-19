#! /usr/bin/python
#
import csv
#from collections import Counter
#from collections import defaultdict
from datetime import datetime
import numpy as np
#
#
def WT(data, lino):
    print "this is WT"
    l = 0
    FarmWT = {}
    for row in data:
        T,S,d = row.split(";")
        l=l+1
        print str(l)+"/"+str(lino)+" "+S+" "+d.strip()
        date = datetime.strptime(d.strip(),"%d%b%Y").date()
        if S not in FarmWT.keys():
            FarmWT[S]=list()
        FarmWT[S].append(date)
        
    return FarmWT
#    
def WaitingTimes(fn, lino):
    l = 0
    FarmWT = {}
    #
    f = open(fn)
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        S = row[1]
        d = row[2]
        l=l+1
        print str(l)+"/"+str(lino)+" "+ S
        date = datetime.strptime(d,"%d%b%Y").date()
        if S not in FarmWT:
            #print S +" not in list"
            FarmWT[S] = list()
                #print FarmWT
        FarmWT[S].append(date)
     
    f.close()   
    return FarmWT
#
def lif(fn):
    f = open(fn)
    lino = sum(1 for line in f)
    f.close()
    print "Number of lines in file "+fn+" "+str(lino)
    return lino
    
def WT2(fn, lino):
    l = 0
    FarmWT = {}
    file = open(fn,'r')
    data=[[e.strip() for e in line.split(";")] for line in file]
    file.close()

    #print edgeList
    d = defaultdict(list)
    while(l < 500):
        for t,s,d in data:
            l+=1
            print str(l)+"/"+str(lino)
            date = datetime.strptime(d,"%d%b%Y").date()
            if s not in FarmWT.keys():
                FarmWT[s]=list()
            FarmWT[s].append(date)
    #

def getNlines(fn, N=5):
    with open(fn) as myfile:
        head = [myfile.next() for x in xrange(N)]
    return head

def calculateWT(wt):
    ## Calculation distribution of waiting times
    print "Calculate waiting times"
    distWT = Counter()
    for f in wt:
        if(len(wt[f])>4):
            print "processing "+str(f)+" "+str(len(wt[f]))
            wt[f].sort()
            for i in range(len(wt[f])):
                if(i>0):
                    diff = wt[f][i]-wt[f][i-1]
                    distWT[diff.days] += 1
                    #print f, diff.days
    return distWT

def cWTpF(wt):
    ## Calcultate waiting times per farm
    print "Calculate waiting times per farms"
    fn = open("wt_sanitized_2002-2009.txt","wb")
    writer = csv.writer(fn)
    writer.writerow(["BNR","Index","W"])
    index = 0
    for f in wt:
        if(len(wt[f])>4):
            index += 1
            print "processing "+str(f)+" "+str(len(wt[f]))
            wt[f].sort()
            #c = Counter()
            for i in range(1, len(wt[f])):
                diff = wt[f][i]-wt[f][i-1]
                #print f, index, diff.days
                tofile =(f,index,diff.days)
                towrite = f+"\t"+str(index)+"\t"+str(diff.days)
                writer.writerow(tofile)
                #c[diff.days] += 1
            
            #for key in sorted(c.keys()):
            #    print f,key,c[key]
      
    fn.close()
    
def medianWT(wt):
    "calculate the median waiting time per farm and the number of data points used"
    print "Calculate the medinan waiting time per farms"
    #
    # File to store the results and writer object
    #
    fn = open("median_wt_2002-2009.txt","wb")
    writer = csv.writer(fn)
    #
    # file for wrong results
    #
    fn_err = open("errMedian_wt_2002-2009.txt","wb")
    errwriter = csv.writer(fn_err)
    #
    # write header
    #
    writer.writerow(["BNR","Index","Median_wt","noTradeContacts"])
    #
    # start the calculations
    # only farms with at least 5 trade contacts are considered. This gives at least a number of 4 waiting times
    #
    index = 0
    for f in wt:
        noTradeContacts = len(wt[f])
        if(noTradeContacts > 4):
            wts=list()
            index += 1
            #print "processing "+str(f)+str(noTradeContacts)
            wt[f].sort()
            #
            # calculate the wating times
            #
            for i in range(1, noTradeContacts):
                diff = wt[f][i] - wt[f][i-1]
                wts.append(diff.days)
            #
            # calculate the median
            #
            wts.sort()
            med = np.median(wts)
            if(med < 0):
                print str(med)+str(f)+str(wts)
                tofile = (f,med,wt[f],wts)
                errwriter.writerow(tofile)
            #
            # write the results to file
            #
            tofile = (f,index,med,noTradeContacts)
            writer.writerow(tofile)
    fn.close()
    fn_err.close()
            
            
    
#        

if __name__=="__main__":
    fn = "sanitizedHIT_2002_2009.csv"
    ln = lif(fn)
    fwt = WaitingTimes(fn, ln)
    medianWT(fwt)
    #cWTpF(fwt)
