# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 09:44:25 2016

@author: OldzieMa

it needs Visa, manuyal on the web
https://pyvisa.readthedocs.io/en/stable/getting.html

pyvisa library located at:

https://github.com/hgrecco/pyvisa

This is great

NI Visa library located at:
http://search.ni.com/nisearch/app/main/p/bot/no/ap/tech/lang/en/pg/1/sn/catnav:du,n8:3.1637,ssnav:sup/

"""

#100 steps both directions 340 - 440 on the Sig gen
#sgi gen 1.25V amp 

# reaf freq from the generator. 

import sys
import matplotlib.pyplot as plt
import numpy as np
import random
import time

#sys.path.append("c:/Anaconda/Lib/pySmithPlot-master")
#import smithplot

#sys.path.append('c:\Anaconda\Lib\easygui-0.97.4')
#import easygui as eg

sys.path.append('c:/Anaconda/Lib/python-vxi11-master')
#import vxi11
import visa

#import timeit

from time import sleep

rm = visa.ResourceManager()      #start Visa Resource Manager
resources = rm.list_resources()     # list resources

"""
# Function below searches for VISA GPIB resources:
# ex. SearchGPIB_Inst(resources, "Hewlett-Packard", "8648A", "GPIB")
# Agilent Technologies  33521A      GPIB
# Hewlett-Packard       8648A       GPIB
# ROHDE&SCHWARZ         NRP-Z51     RSNRP
# Agilent Technologies  33522A      GPIB
"""
def SearchGPIB_Inst(Resource, Name = "", Model = "", Conection = ""):
    for Num, Res in enumerate(Resource):
        #print Num
        #print Res
        ResList = Res.split("::")
        #print ResList
        if Conection in str(ResList[0]):
            res = rm.open_resource(Resource[Num])
            test = res.ask("*IDN?")
            res.close()
            if Name in str(test.split(",")[0]) and Model in str(test.split(",")[1]):
                #print (test)
                print "found: ",
                print Name + " ",
                print Model + " ",
                print "resource # " + str(Num)
                return Num

"""
# Function below searches for VISA COM port resources:
# ex. SearchCOM_Inst(resources, ASRL3::INSTR")
# ASRL3::INSTR
# ASRL7::INSTR
# ASRL10::INSTR
"""
def SearchCOM_Inst(Resource, Conection = ""):
    for Num, Res in enumerate(Resource):
        #print Num
        #print Res
        if Conection in str(Res):
            print "found: ",
            print Conection + " ",
            print "resource #: " + str(Num)
            return Num


GEN = rm.open_resource(resources[SearchGPIB_Inst(resources, "Agilent Technologies", "33522A", "GPIB")])    #SigGen assigned to GPIB 10
com3 = rm.open_resource(resources[SearchCOM_Inst(resources, "ASRL3::INSTR")])   #This is the 400kHz generator port RS232

com3.baud_rate = 115200

SigGenDAta = [] # global array to Sig Gen data
RFgenDATA = []  # global array to Sig Gen data
hunting = []    # global array again
HuntingFreqAll = []
HuntingVectorsAll = []
samplingRate_1 = 0.0

def close_inst():
    GEN.close() #close GPIB
#    com10.close() #close port
    com3.close() #close port    
    rm.close()   #close resources

def readbuffer():
    while com3.bytes_in_buffer>1:
        return com3.read()


def sweep(delay=.05):
    com3.clear()
    for step in range(340000,440000,100):
        print "Sig Gen Freq = ",
        print step,
        GEN.write("FREQuency "+str(step))
        sleep(delay)
        com3.ask("FRQ")
        sleep(delay)
        EdgeReadback = int(readbuffer())
        print " ===> EDGE Freq = ",
        print str(EdgeReadback)
        SigGenDAta.append(step)
        RFgenDATA.append(EdgeReadback)
        
def sweep1(delay=.004):
    com3.clear()
    startTime = time.clock()
    for step in range(390000,340000,-100):
        #print "Sig Gen Freq = ",
        #print step,
        GEN.write("FREQuency "+str(step))
        #sleep(delay)
        com3.ask("FRQ")
        sleep(delay)
        EdgeReadback = int(readbuffer())
        #EdgeReadback = int(com3.read())
        #print " ===> EDGE Freq = ",
        #print str(EdgeReadback)
        SigGenDAta.append(step)
        RFgenDATA.append(EdgeReadback)
    com3.clear()
    for step in range(340000,390000,100):
        #print "Sig Gen Freq = ",
        #print step,
        GEN.write("FREQuency "+str(step))
        #sleep(delay)
        com3.ask("FRQ")
        sleep(delay)
        EdgeReadback = int(readbuffer())
        #EdgeReadback = int(com3.read())
        #print " ===> EDGE Freq = ",
        #print str(EdgeReadback)
        SigGenDAta.append(step)
        RFgenDATA.append(EdgeReadback)
    stopTime = time.clock()
    print("Sweep time: "),
    print(stopTime - startTime)
    print("FRQ command sampling rate: "),
    global samplingRate_1
    samplingRate_1= ((stopTime - startTime)/len(RFgenDATA)*1000)
    print(samplingRate_1),
    print(" ms/sample")

def plotsweep1():
    plt.plot(RFgenDATA)
    plt.grid()
    plt.title("Sweep 390kHz to 340kHz & 340kHz to 390kHz sampling rate: "+str(samplingRate_1)[0:4] + " ms/sample")
    plt.xlabel("samples")
    plt.ylabel("Freq [kHz]")

def jump(x = 50): #collect x numbers of randomn tracking waveorms
    com3.clear()
    readbuffer()
    readbuffer()
    randFreq = random.randrange(340000,440000,1000)
    GEN.write("FREQuency "+str(randFreq))
    print "random freq: ",
    print randFreq
    HuntingFreqAll.append(randFreq)
    for c in range(x):
        com3.ask("FRQ")
        sleep(.005)
        EdgeReadback = int(readbuffer())
        hunting.append(EdgeReadback)
    #plt.plot(hunting)
    #plt.grid()
        


def randomplt():
    global HuntingVectorsAll
    global hunting
    for i in range(50):
        jump()
        plt.plot(hunting)
        HuntingVectorsAll.append(hunting)
        hunting = []
    plt.grid()
    plt.title("Random Freq Tracking Vaveforms")
    plt.xlabel("Freq Samples RS-232 Baud set to 115200 for faster dampling rate")
    plt.ylabel("Freq [kHz]")
    if raw_input("Do you want to save y/n? ") == ("y"):
        plt.savefig(str(time.ctime())[0:10] + " - Random Freq Tracking Vaveforms")



def niceplot(title = "Sig Gen Freq. vs dCEX 400kHz Generetor Freq.", xlab = "Sig Gen Freq", ylab = "dCEX Freq"):
    plt.plot(SigGenDAta, RFgenDATA)
    plt.grid()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    
#sweep()
#niceplot()
#plt.savefig("plot")