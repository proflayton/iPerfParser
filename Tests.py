'''
Tests.py

Class to hold information for each iPerf tests

Author: Brandon Layton
'''

class Test():

	Time 		= "UNKNOWN"

	OSName 		= "UNKNOWN"
	OSArchitectue="UNKNOWN"
	OSVersion 	= "UNKNOWN"

	JavaVersion = "UNKNOWN"
	JavaVender  = "UNKNOWN"

	Networktype = "UNKNWON"

	Server 		= "UNKNOWN"
	Host		= "UNKNOWN"

	NetworkProvider = "UNKNOWN"
	NetworkOperator = "UNKNOWN"
	DeviceID = "UNKNOWN"
	ConnectionType = "UNKNOWN"

	def __init__(self,filePath):
		self.load(filePath)

	def load(self,filePath):
		print("Loading in " + str(filePath));
		f = open(filePath,'r')
		f.readline() #CPUC Tester Beta v2.0
		time = f.readline()
		time = time.split("at ")[1]
		print(time)
		self.Time = time

		
		temp = f.readline()
		while "OS:" not in temp:
			temp = f.readline()

		try:
			self.OSName = temp.split("Name = ")[1].split(",")[0]
			self.OSArchitectue = temp.split("Architecture = ")[1].split(",")[0]
			self.OSVersion = temp.split("Version = ")[1]
		except:
			print("ERROR LOADING")
			return

		print(temp)

		f.close()


	def __repr__(self):
		return ("Test @ " + str(self.Time) + "" + 
				"       OS: " + str(self.OSName) + ", " + self.OSArchitectue + ", " + self.OSVersion + "\n"
				)

#Small tests within each Test file
class SubTest():

	Latitude = 0.0
	Longitude= 0.0

	#Example: Iperf TCP West
	Type 	 = "UNKNOWN" 

	IP 		 = "UNKNOWN"
	Port	 = 0000

	WindowSz = 0 #In KByte

	pings = []

	def __init__(self):
		pass

#Each subset of pings within each subset (represented by a numbered thread)
class Pings():
	localHost = "UNKNOWN"
	localPort = 0
	serverHost= "UNKNWON"
	serverPort= 0

	pings = []

	def __init__(self):
		pass

#Each ping within a subset of pings
class Ping():
	#second started to second ended
	secIntervalStart = 0
	secIntervalEnd	 = 0

	size 			 = 0
	speed			 = 0

	def __init__(self):
		pass
