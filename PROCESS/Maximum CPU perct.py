import psutil


import paho.mqtt.client as mqttclient
import time


def on_connect(client,userdata,flags,rc):
	if rc==0:
		print("client is connected\n")
		global connected
		connected=True
	else:
		print("connection failed\n")


def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []


    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'cpu_times', 'status'])
          # pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass


    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['cpu_percent'], reverse=True)
    return listOfProcObjects

def main():
    print("*** Iterate over all running process and print process ID & Name ***")
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
	    #processCPU = psutil.cpu_percent()
	    
            #print(processName, processID, processCPU)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print('*** Create a list of all running processes ***')
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
       # Get process detail as dictionary
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       # Append dict of process detail in list
       listOfProcessNames.append(pInfoDict)
    # Iterate over the list of dictionary and print each elem
    #for elem in listOfProcessNames:
    	#print(elem)

    print('*** Top 5 process with highest memory usage ***')
    listOfRunningProcess = getListOfProcessSortedByMemory()
   
        
    global flag
    flag=1
    global combined
    combined = []
    connected = False

    broker_address ="maqiatto.com"
    port = 1883
    user = "rajini.my98@gmail.com"
    password = "poojabhagavan"
	


    client=mqttclient.Client("MQTT")
    client.username_pw_set(user,password=password)
    print("hii")

    client.on_connect=on_connect
	
    client.connect(broker_address,port=port)
   
    client.loop_start()
    while connected!=True:
	time.sleep(0.2)
	while flag!=0:

    		for elem in listOfRunningProcess[:5] :
			data=str(elem)
			#client.publish("rajini.my98@gmail.com/test1",data)
			combined.append(data)
			combined.append('\n')

		
		

		listToStr = ' '.join([str(elem) for elem in combined])
		 
  
		print(listToStr)



    		client.publish("rajini.my98@gmail.com/test1",listToStr)
		flag=0
   		client.loop_stop()
		break

main()
    





