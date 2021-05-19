from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import random
import copy

processlist = []
start_time = []
end_time = []
response_time = []
ta_time = []
waiting_time = []
totalWT = 0
totalTT = 0
totalRT = 0
process = 0
time = 0
tq = 0
color_dict = {'P1':'#98AFC7', 'P2':'#1F45FC', 'P3':'#00FFFF','P4':'#00FF00','P5':'#6AFB92',
				'P6':'#893BFF','P7':'#FFFF00','P8':'#F75D59', 'P9':'#FAAFBE', 'P10':'#FF00FF','Idle':'#FFFFFF'}

def average():
	global process
	print("\nAverage Response Time = {:.2f}".format(float(totalRT/process)))
	print("Average Turnaround Time = {:.2f}".format(float(totalTT/process)))
	print("Average Waiting Time = {:.2f}".format(float(totalWT/process)))

def showganttchaart(process_data,ticks):	
	left = 0
	plt.ylabel("Burst time")
	for i in range(len(process_data)):
		plt.barh(1,process_data[i][1],color=color_dict[process_data[i][0]],left=left)
		plt.text(left-.25+(float(process_data[i][1]/2)),1,process_data[i][0])
		left += process_data[i][1]	 
	plt.xticks(ticks)
	plt.yticks([0])
	plt.show()

def computation(processedqueue):
	global totalRT,totalTT,totalWT
	# 0 - process name  = processlist[i][0]
	# 1 - bursttime = processlist[i][1]
	# 2 - arrival time = processlist[i][2]
	# 3 - priority = processlist[i][3]
	# 4 - start time = processlist[i][4]
	# 5 - endtime = processlist[i][5]
	# 6 - response time = processlist[i][6]
	# 7 - turn around time = processlist[i][7]
	# 8 - waiting time = processlist[i][8]
	# sort by pname = processlist.sort(key=lambda x:x[0])
	# sort by burst time = processlist.sort(key=lambda x:x[1])
	# sort by arrival time = processlist.sort(key=lambda x:x[2])
	# sort by priority = processlist.sort(key=lambda x:x[3])

	for i in range(len(processlist)):
		processedqueue[i][6] = processedqueue[i][4]-processedqueue[i][2]		 #response time
		totalRT += processedqueue[i][4]-processedqueue[i][2]
		processedqueue[i][7] = processedqueue[i][5]-processedqueue[i][2]		 #turn around time
		totalTT += processedqueue[i][5]-processedqueue[i][2]
		processedqueue[i][8] = processedqueue[i][7]-processedqueue[i][1]		 # waiting time
		totalWT += processedqueue[i][7]-processedqueue[i][1]
	return processedqueue

def printtable(data):
	table = DataFrame(data, columns = ['Process List','Burst Time','Arrival Time','Priority','Start Time',
					'End Time','Response Time','Turnaround Time','Waiting Time'])
	print(table)

def CpuUtil(idletime,totaltime):
	CPUUtil = ((float(totaltime-idletime)/totaltime))*100

	print("CPU Utilization = ",round(CPUUtil,2), "%")

def FCFS():
	global time
	ticks = [0]
	idletime = 0
	zeroes = 0
	ti = 0
	FCFSProcessedqueue = []
	Ganttqueue = []
	for x in range(len(processlist)):
		if(processlist[x][2] == 0):
			zeroes += 1
	if (zeroes != process):
		processlist.sort(key=lambda x:x[2])			# Sort by arrival time					
	FCFSProcessedqueue = copy.deepcopy(processlist) 
	for i in range(len(FCFSProcessedqueue)):
		if (time<FCFSProcessedqueue[i][2]):
			Ganttqueue.append(['Idle',FCFSProcessedqueue[i][2]-time])		# For idle
			ti += (FCFSProcessedqueue[i][2]-time)
			time += (FCFSProcessedqueue[i][2]-time)
			ticks.append(time)
		print("Value of ti = ", ti)
		Ganttqueue.append([FCFSProcessedqueue[i][0],FCFSProcessedqueue[i][1]])
		FCFSProcessedqueue[i][4] = time    # Start time
		time += FCFSProcessedqueue[i][1]   
		FCFSProcessedqueue[i][5] = time    # End time 
		ticks.append(time)
	computation(FCFSProcessedqueue)
	plt.title("Gantt Chart of First come, First Served Scheduling")
	processlist.sort(key=lambda x:x[0])				# Sort by Process Name
	FCFSProcessedqueue.sort(key=lambda x:x[0])		# Sort by Process Name
	print("-"+"-"*120+"\n")
	print("First Come, First Served simulation result:\n")	
	printtable(FCFSProcessedqueue)
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)

def SJF():
	global time
	samp = 0
	ticks = [0]
	zeroes = 0
	counter = 0
	ti = 0
	SJFProcessedqueue = []
	Ganttqueue = []
	readyqueue = []
	for x in range(len(processlist)):
		if(processlist[x][2] == 0):
			zeroes += 1
	if (zeroes != process):
		processlist.sort(key=lambda x:x[2])			# Sort by arrival time
	else:
		processlist.sort(key=lambda x:x[1])			# Sort by burst time	
	while(counter != len(processlist)):
		if(time<processlist[counter][2]):
			Ganttqueue.append(['Idle',processlist[counter][2]-time])		# For idle
			ti += (processlist[counter][2]-time)
			time += (processlist[counter][2]-time)
			ticks.append(time)
			counter -=1
		else:
			for x in range(len(processlist)):
				if(processlist[x][2]<=time and processlist[x] not in SJFProcessedqueue):
					readyqueue.append(processlist[x])
			readyqueue.sort(key=lambda x:x[1]) 		# Sort by burst time
			readyqueue[0][4] = time
			time += readyqueue[0][1]
			readyqueue[0][5] = time
			Ganttqueue.append([readyqueue[0][0],readyqueue[0][1]])
			ticks.append(time)
			SJFProcessedqueue.append(readyqueue[0])
			readyqueue = []
		counter +=1

	computation(SJFProcessedqueue)
	

	plt.title("Gantt Chart of Shortest Job First Scheduling")
	processlist.sort(key=lambda x:x[0])
	SJFProcessedqueue.sort(key=lambda x:x[0])
	
	print("-"+"-"*120+"\n")
	print("Shortest Job First simulation result:\n")
	printtable(SJFProcessedqueue)	
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)

def NonPrempPrio():
	ticks = [0]
	global time
	zeroes = 0 
	counter = 0
	ti = 0
	NonPrempPrioqueue = []
	readyqueue = []
	Ganttqueue = []
	for x in range(len(processlist)):
		if(processlist[x][2] == 0):
			zeroes += 1
	if (zeroes != process):
		processlist.sort(key=lambda x:x[2])			# Sort by arrival time	
	else:
		processlist.sort(key=lambda x:x[3])			# Sort by priority time
	while(counter != len(processlist)):
		if(time<processlist[counter][2]):
			Ganttqueue.append(['Idle',processlist[counter][2]-time])		# For idle
			ti += (processlist[counter][2]-time)
			time += (processlist[counter][2]-time)
			ticks.append(time)
			counter -=1
		else:
			for x in range(len(processlist)):
				if(processlist[x][2]<=time and processlist[x] not in NonPrempPrioqueue):
					readyqueue.append(processlist[x])
			readyqueue.sort(key=lambda x:x[3]) 		# Sort by priority time
			readyqueue[0][4] = time
			time += readyqueue[0][1]
			readyqueue[0][5] = time
			Ganttqueue.append([readyqueue[0][0],readyqueue[0][1]])
			ticks.append(time)
			NonPrempPrioqueue.append(readyqueue[0])
			readyqueue = []
		counter +=1

	computation(NonPrempPrioqueue)
	plt.title("Gantt Chart of Non Preemptive Priority Scheduling")
	processlist.sort(key=lambda x:x[0])

	NonPrempPrioqueue.sort(key=lambda x:x[0])	
	
	print("-"+"-"*120+"\n")
	print("Non Preemptive Priority simulation result:\n")
	printtable(NonPrempPrioqueue)
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)

def RoundRobin():
	ticks = [0]
	global time, tq, process
	processed = [] 
	done = 0
	ti = 0
	RRqueue  = copy.deepcopy(processlist)
	Process_preempted = []
	for i in range(len(RRqueue)):
		Process_preempted.append([RRqueue[i][0],0])					# 0 = Not Preempted, 1 = Preempted
	Ganttqueue = []	
	pque = []
	while(True):
		RRqueue.sort(key=lambda x:x[2])
		if(RRqueue[0][2]>time):
			Ganttqueue.append(['Idle',RRqueue[0][2]-time])	
			ti += (RRqueue[0][2]-time)	
			time += (RRqueue[0][2]-time)
			ticks.append(time)
		for z in range(len(RRqueue)):
			if(RRqueue[0][0]==Process_preempted[z][0] and Process_preempted[z][1]==0):		# Check if preempted
				RRqueue[0][4] = time 						# If not preempted before, that's the start time
		if(RRqueue[0][1]>tq):
			RRqueue[0][1] -= tq
			Ganttqueue.append([RRqueue[0][0],tq])
			time += tq
			RRqueue[0][2] = time	
			for i in range(len(RRqueue)):
				if(RRqueue[0][0]==Process_preempted[i][0]):
					Process_preempted[i][1] = 1						# Process is preempted		
		else:
			Ganttqueue.append([RRqueue[0][0],RRqueue[0][1]])
			hold = copy.deepcopy(Process_preempted)
			for i in range(len(Process_preempted)):
				if(Process_preempted[i][0] == RRqueue[0][0]):
					hold.pop(i)
			Process_preempted = copy.deepcopy(hold)
			time += RRqueue[0][1]
			RRqueue[0][1]  = 0
			RRqueue[0][5] = time
			processed.append(RRqueue[0])
			RRqueue.pop(0)
		ticks.append(time)
		if not RRqueue:
			break
	RRqueue = copy.deepcopy(processed)
	RRqueue.sort(key=lambda x:x[0])
	for i in range(len(RRqueue)):
		RRqueue[i][1] = processlist[i][1]
		RRqueue[i][2] = processlist[i][2]
	print("-"+"-"*120+"\n")
	print("Round Robin simulation result:\n")
	plt.title("Gantt Chart of Round Robin Scheduling")
	computation(RRqueue)
	printtable(RRqueue)
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)	

def SRTF():
	ticks = [0]
	global time, process
	processed = [] 
	done = 0
	ti = 0
	SRTFqueue  = copy.deepcopy(processlist)
	Process_preempted = []
	readyqueue = []
	processed = []
	normqueue = []
	Ganttqueue = []
	temp = []
	counter = 0
	for i in range(len(SRTFqueue)):
		Process_preempted.append([SRTFqueue[i][0],0])					# 0 = Not Preempted, 1 = Preempted
	while(True):
		SRTFqueue.sort(key=lambda x:x[2])								# sort by arrival time
		if(SRTFqueue[0][2]>time):										# for idle
			Ganttqueue.append(['Idle',SRTFqueue[0][2]-time])
			ti += (SRTFqueue[0][2]-time)			
			time += (SRTFqueue[0][2]-time)
			ticks.append(time)
		for i in range(len(SRTFqueue)):
			if(SRTFqueue[i][2]<=time):
				readyqueue.append(SRTFqueue[i])							# ready queue
		for x in range(len(SRTFqueue)):
			if(SRTFqueue[x] not in readyqueue):							# append to normal queue if process is in the ready queue
				normqueue.append(SRTFqueue[x])
		normqueue.sort(key=lambda x:x[2])								# sort by arrival time
		readyqueue.sort(key=lambda x:x[1])								# sort by burst time
		for z in range(len(Process_preempted)):
				if(readyqueue[0][0]==Process_preempted[z][0] and Process_preempted[z][1]==0):		# Check if preempted
					readyqueue[0][4] = time 														# If not preempted before, that's the start time

		if(normqueue and readyqueue[0][1]+time > normqueue[0][2]):
			Ganttqueue.append([readyqueue[0][0],normqueue[0][2]-time])
			readyqueue[0][1] -= normqueue[0][2]-time
			time += (normqueue[0][2]-time)
			readyqueue[0][2] = time
			ticks.append(time)
			for i in range(len(Process_preempted)):
				if(readyqueue[0][0]==Process_preempted[i][0]):
					Process_preempted[i][1] = 1						# Process is preempted
		else:
			Ganttqueue.append([readyqueue[0][0],readyqueue[0][1]])
			time += readyqueue[0][1]
			readyqueue[0][1] = 0
			readyqueue[0][5] = time
			ticks.append(time)
			processed.append(readyqueue[0])
		for y in range(len(readyqueue)):
			temp.append(readyqueue[y])
		for y in range(len(normqueue)):
			temp.append(normqueue[y])
		for i in range(len(SRTFqueue)):
			SRTFqueue[i] = temp[i]
		SRTFtemp = copy.deepcopy(SRTFqueue)
		for x in range(len(SRTFqueue)):
			if(SRTFqueue[x][1] == 0):
				SRTFtemp.pop(x)
		SRTFqueue = copy.deepcopy(SRTFtemp)
		readyqueue = []
		normqueue = []
		temp = []
		if not SRTFqueue:
			break
	SRTFqueue = copy.deepcopy(processed)
	SRTFqueue.sort(key=lambda x:x[0])
	for i in range(len(SRTFqueue)):
		SRTFqueue[i][1] = processlist[i][1]
		SRTFqueue[i][2] = processlist[i][2]
	print("-"+"-"*120+"\n")
	print("Shortest Remaining Time First result:\n")
	plt.title("Gantt Chart of Shortest Remaining Time First")
	computation(SRTFqueue)
	printtable(SRTFqueue)
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)	

def PreempPrio():
	ticks = [0]
	global time, process
	processed = [] 
	done = 0
	ti = 0
	Preempprioqueue  = copy.deepcopy(processlist)
	Process_preempted = []
	readyqueue = []
	processed = []
	normqueue = []
	Ganttqueue = []
	temp = []
	counter = 0
	for i in range(len(Preempprioqueue)):
		Process_preempted.append([Preempprioqueue[i][0],0])					# 0 = Not Preempted, 1 = Preempted
	while(True):
		Preempprioqueue.sort(key=lambda x:x[2])								# sort by arrival time
		if(Preempprioqueue[0][2]>time):										# for idle
			Ganttqueue.append(['Idle',Preempprioqueue[0][2]-time])
			ti += (Preempprioqueue[0][2]-time)			
			time += (Preempprioqueue[0][2]-time)
			ticks.append(time)
		for i in range(len(Preempprioqueue)):
			if(Preempprioqueue[i][2]<=time):
				readyqueue.append(Preempprioqueue[i])							# ready queue
		for x in range(len(Preempprioqueue)):
			if(Preempprioqueue[x] not in readyqueue):							# append to normal queue if process is in the ready queue
				normqueue.append(Preempprioqueue[x])
		normqueue.sort(key=lambda x:x[2])								# sort by arrival time
		readyqueue.sort(key=lambda x:x[0])								# sort by process name
		readyqueue.sort(key=lambda x:x[3])								# sort by priority
		for z in range(len(Process_preempted)):
				if(readyqueue[0][0]==Process_preempted[z][0] and Process_preempted[z][1]==0):		# Check if preempted
					readyqueue[0][4] = time 														# If not preempted before, that's the start time

		if(normqueue and readyqueue[0][1]+time > normqueue[0][2]):
			Ganttqueue.append([readyqueue[0][0],normqueue[0][2]-time])
			readyqueue[0][1] -= normqueue[0][2]-time
			time += (normqueue[0][2]-time)
			readyqueue[0][2] = time
			ticks.append(time)
			for i in range(len(Process_preempted)):
				if(readyqueue[0][0]==Process_preempted[i][0]):
					Process_preempted[i][1] = 1						# Process is preempted
		else:
			Ganttqueue.append([readyqueue[0][0],readyqueue[0][1]])
			time += readyqueue[0][1]
			readyqueue[0][1] = 0
			readyqueue[0][5] = time
			ticks.append(time)
			processed.append(readyqueue[0])
		for y in range(len(readyqueue)):
			temp.append(readyqueue[y])
		for y in range(len(normqueue)):
			temp.append(normqueue[y])
		for i in range(len(Preempprioqueue)):
			Preempprioqueue[i] = temp[i]
		Preempprioqueuetemp = copy.deepcopy(Preempprioqueue)
		for x in range(len(Preempprioqueue)):
			if(Preempprioqueue[x][1] == 0):
				Preempprioqueuetemp.pop(x)
		Preempprioqueue = copy.deepcopy(Preempprioqueuetemp)
		readyqueue = []
		normqueue = []
		temp = []
		if not Preempprioqueue:
			break
	Preempprioqueue = copy.deepcopy(processed)
	Preempprioqueue.sort(key=lambda x:x[0])
	for i in range(len(Preempprioqueue)):
		Preempprioqueue[i][1] = processlist[i][1]
		Preempprioqueue[i][2] = processlist[i][2]
	print("-"+"-"*120+"\n")
	print("Preemptive Priority result:\n")
	plt.title("Gantt Chart of Preemptive Priority")
	computation(Preempprioqueue)
	printtable(Preempprioqueue)
	average()
	CpuUtil(ti,ticks[-1])
	showganttchaart(Ganttqueue,ticks)	

def prompt():
	while(True):
		print("\n\nChoose Simulation Method: \n")
		print("[1] First Come, First Serve\n")
		print("[2] Shortest Job First\n")
		print("[3] Non Preemptive Priority\n")
		print("[4] Round Robin\n")
		print("[5] Shortest Remaining Time First\n")
		print("[6] Preemptive Priority\n")
		choice = int(input("Choice >> "))
		if (choice == 1):
			FCFS()
			break
		elif(choice == 2):
			SJF()
			break
		elif(choice == 3):
			NonPrempPrio()
			break
		elif(choice == 4):
			RoundRobin()
			break
		elif(choice == 5):
			SRTF()
			break
		elif(choice == 6):
			PreempPrio()
			break
		else:
			print("Invalid Choice, Please try again\n")
			print("-"+"-"*120+"\n")
	
# --------------------------------------------- MAIN ---------------------------------------#

while (True):
	process = int(input("\nEnter number of processes to be simulated >> "))
	if (process<3):
		input("Error:Minimum Processes should be 3, please any key to try again....")
		print("-"+"-"*120+"\n")
	elif (process>10):
		input("Error:Maximum Processes should be 10, please any key to try again....")
		print("-"+"-"*120+"\n")
	else:
		print("\n")
		break

for i in range(process):
	processlist.append([])
	bt = int(input("Enter burst time for P{:} ---> ".format(i+1)))
	at = int(input("Enter arrival time for P{:} ---> ".format(i+1)))
	prio = int(input("Enter priority for P{:} ---> ".format(i+1)))
	processlist[i].append("P"+str(i+1))
	processlist[i].append(bt)
	processlist[i].append(at)	
	processlist[i].append(prio)
	processlist[i].append(0)	# Start Time
	processlist[i].append(0)	# End Time
	processlist[i].append(0)	# TT
	processlist[i].append(0)	# Wt
	processlist[i].append(0)	# Rt
	print("-"+"-"*100+"\n")
tq = int(input("Enter Time Quantum ---> "))
print("-"+"-"*120+"\n")

prompt()
while(True):
	print("\n-"+"-"*120+"\n")
	a = input("Do you want to simulate again using the same data? [Y/N] >> ")
	if (a=='Y' or a =='y'):
		totalWT = 0
		totalTT = 0
		totalRT = 0
		time = 0
		prompt()
	elif (a=='N' or a =='n'):
		print("-"+"-"*120+"\n")
		print(" "*53+"Submitted By:\n"+" "*54+"William Hod\n"+" "*54+"Kian Lejano\n"+
				" "*52+"Alyssa Perpetua\n"+" "*54+"Aileen Gomez\n"+" "*50+"Austin Charles Burog\n"+"\n\n"+" "*56+"BSCS-N2A\n")
		print("-"+"-"*120)
		break
	else:
		print("Invalid Choice, try again\n")
		print("-"+"-"*120+"\n")



