#Author : Eiman Ahmed
#Python file to calculate and export inflows of any given station at any given time
import sys
import fileinput
import networkx as nx
import matplotlib.pyplot as plt
import csv

#change this directory to wherever you located the TrainTravel.csv file 
openingfile = open("SingularTrainFlow.csv")
traindata = openingfile.readlines()
openingfile.close()

#initializing the lists(features) we are going to need to graph with
#You can also use a dictionary to store in the following format - {"TrainName",[FromStation,ToStation,TravelTime]}

trains=[]
stations=[]
traveltime=[]

traindata.pop(0)
#Extracting data into select initalized lists ^ 
for line in traindata:
	traintravel = line.rstrip('\n').split(',')
	trains.append(traintravel[1])
	stations.append(traintravel[4])
	traveltime.append(int(traintravel[5]))

#initializing a graph to represent the connections on 
G= nx.DiGraph()

#Connecting all stations with one another on the graph
length = xrange(1, len(trains))

for i in length:
	if(trains[i-1]==trains[i]):
		G.add_edge(stations[i-1],stations[i],weight=traveltime[i])
		G.add_edge(stations[i],stations[i-1],weight=traveltime[i])

#nx.draw_spring(G, with_labels=True, node_color='w', node_size=300, font_size=6)
#plt.show()

files = ['f_latenight.csv','f_morning.csv','f_noon2.csv','f_evening.csv','f_night.csv','f_latemorning.csv','f_am.csv','f_pm.csv','f_allday.csv']
for name in files:

	openingfile = open("/home/ewahmed/subway-flow/PrePres/"+name)
	noondata = openingfile.readlines()
	openingfile.close()

	name= name[2:len(name)-4]

	#Extracting data into select initalized lists ^ 
	noondata.pop(0)
	total = 0
	for line in noondata:
		_, _, station, exits, entries,stationid = line.rstrip('\n').split(',')
		G.node[station]["entries"] = int(entries)
		G.node[station]["exits"] = int(exits)
		G.node[station]["demand"]=int(exits)-int(entries)
		G.node[station]["stationid"]=stationid
		total += int(exits) - int(entries)

	for n in G.nodes():
		if "demand" not in G.node[n]:
			G.remove_node(n)

	turnstile_stations = [record.strip().split(',')[2] for record in noondata]
	gtfs_stations = G.nodes()

	#print set(turnstile_stations) - set(gtfs_stations)
	extra_nodes = set(gtfs_stations) - set(turnstile_stations)

	nx.draw_spring(G, with_labels=True, node_color='w', node_size=350, font_size=7)
	#plt.show()

	flow = nx.min_cost_flow(G)

	inflowstation=[]
	inflow=[]
	
	for x in G.nodes():
		total = 0
		inflowstation.append(x)
		for p in G.predecessors(x):
			total = total+ flow[p][x]
		inflow.append(total)

    
	rows = zip(inflowstation,inflow)

	length= range(0,len(inflowstation))

        if not os.path.exists('Inflows'):
            os.mkdir('Inflows')

	out= open("Inflows/" + name+"inflows.csv", "wb")
	out.write('\n')
	for i in length: 
		out.write(inflowstation[i] +',' + str(inflow[i]) + '\n')
	out.close()
