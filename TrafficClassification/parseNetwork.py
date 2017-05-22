_Author_ = "Ashwin Kini"


import time
##This script reads from the /proc/net/dev and pushes the stats. This file has stats for all interfaces. 
##We pick interface of out interest.


while(1):
	##opening and closing file everytime as the file keeps on updating
	fo = open("/proc/net/dev", "r")
	print "\t\t\t\t\t\tThe statistics for interface \n"
	lines = fo.readlines()

	##First Row has the columns that we need to pick up
	rowFirst = lines[1]


	##split the line to get fields.
	junk, recievedColumns, transmittedColumns = rowFirst.split("|")

	##get fields for the recived and transmitted sections.
	recievedColumns = map(lambda a: "recieved_"+a , recievedColumns.split())
	transmittedColumns = map (lambda a : "Transmitted_"+a , transmittedColumns.split()) 


	##add all fields in one list
	finalColumns = recievedColumns + transmittedColumns

	##find the line with desired interface entry
	for line in lines[2:]:
		if("qvo39e66dda-56" in line):
			interfaceName, data = line.split(":")
			interfaData = zip(finalColumns, data.split())
			break
	for data in interfaData:
		print "\t\t\t\t\t\t" + str(data)


	print "\n\n\t\t\t\t\t\tNext entry \n\n"
	fo.close()
	time.sleep(1)







