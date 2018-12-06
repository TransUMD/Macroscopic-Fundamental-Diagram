import numpy as np
import os
import sys
import optparse
import subprocess
import random
import sumolib
import traci
import time
import re

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# 计算状态
def CalcProduction():
    EdgeID = np.array(list(traci.edge.getIDList()))
    Speed = 0
    for i in range(0,EdgeID.shape[0]):
        Edge = EdgeID[i]
        VehicleID = np.array(list(traci.edge.getLastStepVehicleIDs(Edge)))
        for j in range(0,VehicleID.shape[0]):      
            Speed += traci.vehicle.getSpeed(VehicleID[j])
    
    Production = Speed
    
    return Production
  
def CalcDeltaQ():
    #LoadedNum = traci.simulation.getLoadedNumber()
    DepartNum = traci.simulation.getDepartedNumber()
    ArriveNum = traci.simulation.getArrivedNumber()
    Delta_Q = (DepartNum-ArriveNum)
    
    return Delta_Q

def ChangeDemandRandom0():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""", file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+1,random.randint(1,Low),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,random.randint(Low,Middle),EdgeIn[i],EdgeOut[j]), file=routes)   
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,random.randint(Middle,High),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
    return

def ChangeDemandRandom1():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""", file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+1,np.round(random.randint(20,Low)*0.75),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,np.round(random.randint(20,Low)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,np.round(random.randint(20,Low)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+4,np.round(random.randint(20,Low)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+5,np.round(random.randint(Low,Middle)*0.75),EdgeIn[i],EdgeOut[j]), file=routes)   
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+6,np.round(random.randint(Low,Middle)*0.15),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+7,np.round(random.randint(Low,Middle)*0.05),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+8,np.round(random.randint(Low,Middle)*0.05),EdgeIn[i],EdgeOut[j]), file=routes) 
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+9,np.round(random.randint(Middle,High)*0.75),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+10,np.round(random.randint(Middle,High)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+11,np.round(random.randint(Middle,High)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+12,np.round(random.randint(Middle,High)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
        routes.close()
    return

def ChangeDemandRandom2():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""", file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+1,np.round(random.randint(20,Low)*0.50),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,np.round(random.randint(20,Low)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,np.round(random.randint(20,Low)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+4,np.round(random.randint(20,Low)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+5,np.round(random.randint(20,Low)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+6,np.round(random.randint(Low,Middle)*0.50),EdgeIn[i],EdgeOut[j]), file=routes)   
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+7,np.round(random.randint(Low,Middle)*0.25),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+8,np.round(random.randint(Low,Middle)*0.10),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+9,np.round(random.randint(Low,Middle)*0.10),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+10,np.round(random.randint(Low,Middle)*0.05),EdgeIn[i],EdgeOut[j]), file=routes) 
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+11,np.round(random.randint(Middle,High)*0.50),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+12,np.round(random.randint(Middle,High)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+13,np.round(random.randint(Middle,High)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+14,np.round(random.randint(Middle,High)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+15,np.round(random.randint(Middle,High)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
        routes.close()
    return

def ChangeDemandRandom3():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""" ,  file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+1,np.round(random.randint(20,Low)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,np.round(random.randint(20,Low)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,np.round(random.randint(20,Low)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+4,np.round(random.randint(20,Low)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+5,np.round(random.randint(20,Low)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+6,np.round(random.randint(20,Low)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+7,np.round(random.randint(Low,Middle)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)   
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+8,np.round(random.randint(Low,Middle)*0.25),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+9,np.round(random.randint(Low,Middle)*0.20),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+10,np.round(random.randint(Low,Middle)*0.15),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+11,np.round(random.randint(Low,Middle)*0.10),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+12,np.round(random.randint(Low,Middle)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car0" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+13,np.round(random.randint(Middle,High)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+14,np.round(random.randint(Middle,High)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+15,np.round(random.randint(Middle,High)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+16,np.round(random.randint(Middle,High)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+17,np.round(random.randint(Middle,High)*0.10),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+18,np.round(random.randint(Middle,High)*0.05),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
        routes.close()
    return

def ChangeDemandRandom4():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""" ,  file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,np.round(random.randint(20,Low)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,np.round(random.randint(20,Low)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+4,np.round(random.randint(20,Low)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+5,np.round(random.randint(20,Low)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+6,np.round(random.randint(20,Low)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j: 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+8,np.round(random.randint(Low,Middle)*0.15),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+9,np.round(random.randint(Low,Middle)*0.20),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+10,np.round(random.randint(Low,Middle)*0.20),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+11,np.round(random.randint(Low,Middle)*0.25),EdgeIn[i],EdgeOut[j]), file=routes) 
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*100000+NodeDemand[j]*10+12,np.round(random.randint(Low,Middle)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car1" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+14,np.round(random.randint(Middle,High)*0.15),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car2" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+15,np.round(random.randint(Middle,High)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car3" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+16,np.round(random.randint(Middle,High)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car4" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+17,np.round(random.randint(Middle,High)*0.25),EdgeIn[i],EdgeOut[j]), file=routes)
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*100000000+NodeDemand[j]*10+18,np.round(random.randint(Middle,High)*0.20),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
        routes.close()
    return

def ChangeDemandRandom5():
    with open("MFDGrid.rou.xml", "w") as routes:
        print("""<routes>
              <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="1.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
              <vType id="Car1" carFollowModel="Krauss" accel="3.05" decel="4.5" tau="1.2" sigma="0.4" length="5" minGap="2" maxSpeed="18"/>
              <vType id="Car2" carFollowModel="Krauss" accel="3.5" decel="4.5" tau="1.0" sigma="0.3" length="5" minGap="1.5" maxSpeed="18"/>
              <vType id="Car3" carFollowModel="Krauss" accel="3.6" decel="4.5" tau="0.8" sigma="0.2" length="5" minGap="1.25" maxSpeed="18"/>
              <vType id="Car4" carFollowModel="Krauss" accel="3.7" decel="4.5" tau="0.7" sigma="0" length="5" minGap="0.75" maxSpeed="18"/>
              <vType id="Car5" carFollowModel="Krauss" accel="3.8" decel="4.5" tau="0.6" sigma="0" length="5" minGap="0.5" maxSpeed="18"/>
              <vehicles>""" ,  file=routes)
        Low = random.randint(21,81)
        Middle = random.randint(81,300)
        High = random.randint(301,600)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="0" end="360" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+1,random.randint(1,Low),EdgeIn[i],EdgeOut[j]), file=routes)
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="360" end="720" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>'
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+2,random.randint(Low,Middle),EdgeIn[i],EdgeOut[j]), file=routes)   
        for i in range(np.size(EdgeIn)):
            for j in range(np.size(EdgeOut)):
                if i!=j:
                    print('                <flow id="F%i" begin="720" end="1080" vehsPerHour="%i" type="Car5" departLane="random" departSpeed="random" from="%i" to="%i"/>' 
                          % (NodeDemand[i]*1000+NodeDemand[j]*10+3,random.randint(Middle,High),EdgeIn[i],EdgeOut[j]), file=routes)
        print("</vehicles>"
              "</routes>", file=routes)
        routes.close()
    return

def run():
    step = 1
    CurrentNumber = 0
    InOut = 0
    OutFlow = 0
    Production = 0
    Accumulation = 0
    Acc = []
    Out = []
    Pro = []
    for i in range (1,1080):       
        traci.simulationStep()
        i += 1
        InOut += CalcDeltaQ()
        step += 1
        Production += CalcProduction()
        OutFlow += traci.simulation.getArrivedNumber()      # Outflow, vehicles that reached their destination (vehicles per time unit)
        if step % 90 ==0:
            Accumulation = CurrentNumber + InOut            # Accumulation, # of vehicles traveling in the network.
            CurrentNumber = Accumulation
            Acc.append(Accumulation)
            Out.append(OutFlow)
            Pro.append(Production)
            InOut = 0
            OutFlow = 0
            Production = 0
    
    traci.close()
    sys.stdout.flush()
    
    return Acc, Pro, Out
    
if __name__ == "__main__":
    options = get_options()    
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    accum=[];produc=[];outfl=[];
    
    #for j in range(1,10):
    Accumulation = []
    Production = [];
    Outflow = [];    
    for i in range(1,6):
        ChangeDemandRandom0()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)
        
    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')    
    accum = Accumulation
    produc = Production
    outfl = Outflow                
    Accumulation = []
    Production = [];
    Outflow = [];    
    
    for i in range(1,6):
        ChangeDemandRandom1()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)
        
    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')       
    accum = np.c_[accum,Accumulation]
    produc = np.c_[produc,Production]
    outfl = np.c_[outfl,Outflow]
    Accumulation = []
    Production = [];
    Outflow = []; 
    
    for i in range(1,6):
        ChangeDemandRandom2()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)

    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')        
    accum = np.c_[accum,Accumulation]
    produc = np.c_[produc,Production]
    outfl = np.c_[outfl,Outflow]
    Accumulation = []
    Production = [];
    Outflow = []; 
               
    
    for i in range(1,6):
        ChangeDemandRandom3()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)
        
    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')   
    accum = np.c_[accum,Accumulation]
    produc = np.c_[produc,Production]
    outfl = np.c_[outfl,Outflow]
    Accumulation = []
    Production = [];
    Outflow = []; 
    
    
    for i in range(1,6):
        ChangeDemandRandom4()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)

    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')           
    accum = np.c_[accum,Accumulation]
    produc = np.c_[produc,Production]
    outfl = np.c_[outfl,Outflow]
    Accumulation = []
    Production = [];
    Outflow = []; 
    
    
    for i in range(1,6):
        ChangeDemandRandom5()            
        traci.start([sumoBinary, "-c", "MFDGrid.sumocfg"])
        a,b,c = run()
        Accumulation.append(a)
        Production.append(b)
        Outflow.append(c)

    Accumulation = np.array(Accumulation)
    Accumulation = Accumulation.reshape(i*12,order='c')
    Production = np.array(Production)
    Production = Production.reshape(i*12,order='c')
    Outflow = np.array(Outflow)
    Outflow = Outflow.reshape(i*12,order='c')       
    accum = np.c_[accum,Accumulation]
    produc = np.c_[produc,Production]
    outfl = np.c_[outfl,Outflow]
    Accumulation = []
    Production = [];
    Outflow = []; 
        


