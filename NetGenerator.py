# Generate Square Grid Network
# Demand Nodes at Each Begin

import numpy as np
import random

R = 10  # number of intersections in rows
C = 10  # number of intersection in columns
L = 500 # Intersection Gap
NodeMatrix = np.zeros([R,C]);

# Node
with open("MFDGrid.nod.xml", "w") as routes:
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=routes)
    print("""<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">""", file=routes)
    Intersection = 1
    for i in range(C):
        for j in range(R):
            print('                <node id="%i" x="+%i" y="-%i" type="traffic_light" tl="%i"/>' % ((i+1)*10+(j+1),j*L,i*L,Intersection), file=routes)
            NodeMatrix[i][j]=(i+1)*10+(j+1)
            Intersection += 1
    print("</nodes>", file=routes)
    
# Demand Point
NodeUp = NodeMatrix[0]
NodeDown = NodeMatrix[R-1]
NodeLeft = NodeMatrix[:,0]
NodeRight = NodeMatrix[:,R-1]
NodeDemand = np.matrix([NodeUp[1:C-1], NodeDown[1:C-1], NodeLeft[1:R-1], NodeRight[1:R-1]])
NodeDemand = np.transpose(NodeDemand.reshape((R-2)*4,order="C"))

# Edge   
with open("MFDGrid.edg.xml", "w") as routes:
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=routes)
    print("""<edges  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">""", file=routes)
    Intersection = 1
    # Connect Horizontal Nodes
    for i in range(1,R-1):
        Row = NodeMatrix[i]
        for j in range(R-1):
            print('                <edge id="%i" from="%i" to="%i" priority="1" numLanes="4" speed="18" />' % (Row[j]*1000+Row[j+1],Row[j],Row[j+1]), file=routes) 
            print('                <edge id="%i" from="%i" to="%i" priority="1" numLanes="4" speed="18" />' % (Row[j+1]*1000+Row[j],Row[j+1],Row[j]), file=routes)
    # Connect Vertical Nodes
    for i in range(1,C-1):
        Column = NodeMatrix[:,i]
        for j in range(C-1):
            print('                <edge id="%i" from="%i" to="%i" priority="1" numLanes="4" speed="18" />' % (Column[j]*1000+Column[j+1],Column[j],Column[j+1]), file=routes) 
            print('                <edge id="%i" from="%i" to="%i" priority="1" numLanes="4" speed="18" />' % (Column[j+1]*1000+Column[j],Column[j+1],Column[j]), file=routes)
    print("</edges>", file=routes)

# Demand Edge
# Only use for square network when R=C
EdgeOrigin = np.zeros([4,R-2])
EdgeDestination = np.zeros([4,R-2])
for i in range(np.size(NodeUp)-2):
    EdgeOrigin[0][i] = NodeUp[i+1]*1000+NodeUp[i+1]+10
    EdgeOrigin[1][i] = NodeDown[i+1]*1000+NodeDown[i+1]-10
    EdgeOrigin[2][i] = NodeLeft[i+1]*1000+NodeLeft[i+1]+1
    EdgeOrigin[3][i] = NodeRight[i+1]*1000+NodeRight[i+1]-1
    
for i in range(np.size(NodeUp)-2):
    EdgeDestination[0][i] = (NodeUp[i+1]+10)*1000+NodeUp[i+1]
    EdgeDestination[1][i] = (NodeDown[i+1]-10)*1000+NodeDown[i+1]
    EdgeDestination[2][i] = (NodeLeft[i+1]+1)*1000+NodeLeft[i+1]
    EdgeDestination[3][i] = (NodeRight[i+1]-1)*1000+NodeRight[i+1]
    
EdgeIn = EdgeOrigin.reshape((R-2)*4,order="C") 
EdgeOut = EdgeDestination.reshape((R-2)*4,order="C") 

# Route
Nodes = np.array(NodeMatrix).reshape(R*C,order='c')
with open("MFDGrid.rou.xml", "w") as routes:
    print("""<routes>
          <vType id="Car0" carFollowModel="Krauss" accel="2.6" decel="4.5" tau="2.0" sigma="0.5" length="5" minGap="2.5" maxSpeed="18"/>
          <vehicles>""", file=routes)
    Low = random.randint(151,251)
    Middle = random.randint(251,400)
    High = random.randint(401,800)
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

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


