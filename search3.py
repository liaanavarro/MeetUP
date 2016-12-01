import csv
import os
# import utils
import math

def distance(a, b):
    """ The distance between two (x, y) points. """
    return math.hypot((a[0] - b[0]), (a[1] - b[1]))

schedule = {}
location = {}
TimeRanking = {}
mplace = {}

timeSlot = ['7:00 AM - 7:30 AM', '7:30 AM - 8:00 AM', '8:00 AM - 8:30 AM', '8:30 AM - 9:00 AM', '9:00 AM - 9:30 AM',
			'9:30 AM - 10:00 AM', '10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM', '11:30 AM - 12:00 PM',
			'12:00 PM - 12:30 PM', '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM',
			'2:30 PM - 3:00 PM', '3:00 PM - 3:30 PM', '3:30 PM - 4:00 PM', '4:00 PM - 4:30 PM', '4:30 PM - 5:00 PM',
			'5:00 PM - 5:30 PM', '5:30 PM - 6:00 PM', '6:00 PM - 6:30 PM', '6:30 PM - 7:00 PM', '7:00 PM - 7:30 PM',
			'7:30 PM - 8:00 PM']

occurrence = []

tempInterOp = {}
tempInterOp['Quezon Hall'] = 'QUEZON'
tempInterOp['University Theater'] = 'THEATER'
tempInterOp['Vargas Museum'] = 'VARGAS'
tempInterOp['Area 2'] = "AREA"
tempInterOp['NISMED/ITDC'] = 'ITDC'
tempInterOp['Melchor Hall'] = 'MELCHOR'
tempInterOp['AS'] = 'PALMA'
tempInterOp['Infirmary'] = 'UHS'
tempInterOp['Main Lib'] = 'LIB'
tempInterOp['Balay Kalinaw'] = 'BALAY'
tempInterOp['Business Ad'] = 'BA'
tempInterOp['Vinzons Hall'] = 'VINZONS'
tempInterOp['CS Lib'] = 'CS'



""" IMPORT CSV FILES """

with open('MeetUP.csv', 'rb') as csvfile:
	node = csv.reader(csvfile, delimiter=',', quotechar='|')
	
	for n in node:
		username = n[1].strip()
		if (username[0] != '#' and n[0].strip() != "Timestamp"):
			
			""" SCHEDULE """
			# sched = n[2].strip('"')
			col=2
			# schedList = []
			# while (sched[-1] == 'M'):
			# 	if (sched[0] == ' '):
			# 		sched = sched[1:]
			# 	schedList.append(sched)
			# 	sched = n[col].strip('"'); col+=1
			
			""" FREE TIME RANKING """
			rank=[]
			# col=col-1
			for counter in range(26):
				rank.append(n[col].strip()); col+=1
			TimeRanking[username] = rank

			# schedule[username] = schedList

			""" LOCATION AT EACH TIME """
			loc = []
			for counter in range(26):
				p = n[col].strip()
				if p in tempInterOp.keys():
					loc.append(tempInterOp[p])
				else: 
					loc.append(p.upper())
				col+=1
				# occurrence.append(0) #to count the occurence of time slot
			location[username] = loc

			""" PREFERRED MEETING PLACE """
			p = n[col].strip()
			if p in tempInterOp.keys():
				mplace[username] =  tempInterOp[p]
			else:
				mplace[username] = p.upper()
		
		# elif (n[0].strip() != "Timestamp"):
		# 	time =  n[2].strip('"')
		# 	for col in range(3,29):
		# 		if (time[0] == ' '): time = time[1:]
		# 		timeSlot.append(time)
		# 		occurrence.append(0)
		# 		time = n[col].strip('"')

	# print "SCHED: ", schedule, '\n'
	# print "RANKING: ",  TimeRanking, '\n'

print "LOCATION: ", location, '\n'
print TimeRanking
print mplace
	# print "MP: ", mplace
schedule = {}

unionAttendees = []
occurrence = [0]* 26
for user, rank in TimeRanking.iteritems():
	print "RANK IS ", rank 
	classes = []
	for value in rank:
		# int(value)
		if value != '0': #meaning no class
			if user not in unionAttendees:
				unionAttendees.append(user)
			
			
			# print "HI ", classes
		else:
			occurrence[rank.index(value)] +=1 #if zero ilagay sa isang list
			classes.append(timeSlot[rank.index(value)])
			rank[rank.index(value)] = "-1"
		
	schedule[user] = classes

for user, rank in TimeRanking.iteritems():
	for value in rank:
		if value == "-1":
			rank[rank.index(value)] = 0

print "OCCURRENCE: ", occurrence, "\n"
print "SCHEDULE: ", schedule
# """ GET TOP 10 SCHEDULES (MAX ATTENDEES) """
# sched = schedule.values()
# occurrence = [0] * 26 #initialy 0 yung count. counts kung iang people yung di free at each timeslot
# # print sched
# for List in sched:
# 	for time in List:
# 		occurrence[timeSlot.index(time)] +=1

freeTime = [] # LAHAT NG  AVAILABLE NA TIME
		
# for i in range(26): 
# 	if occurrence[i] == 0: #meaning may common time na free lahat
# 		freeTime.append(timeSlot[i])

'''
attendees[] - list of lists ng attendees per available time
freeTime[] - list ng available free time
'''
attendees = {}
users = schedule.keys()
sched = schedule.values()
# if freeTime == []: #conflicting schedule
# 	for i in range(5): # the number(n) inside range means output top n time slots
# 		#gawa pa ng condition dito. output 5 only if len(freeTime) >= 5
# 		freeTime.append(timeSlot[occurrence.index(min(occurrence))])
# 		del timeSlot[occurrence.index(min(occurrence))] #delete top 5 time slot here
# 		occurrence.remove(min(occurrence))
	
# 	for time in freeTime:
# 		att = []
# 		timeSlot.append(time) #append top 5 time slot here
# 		for List in sched:
# 			if time not in List and users[sched.index(List)] not in att:
# 				att.append(users[sched.index(List)])
# 		attendees[time] = att
# 		if len(att) > 1: # at least 2 attendees
# 			print "\nMeeting time: ", time, "\nAttendees: ", att
# 			# for person in att:
# 			# 	print "\n", person, location[person]
# else:
# 	print "All users can attend the meeting. Possible time:"
# 	for i in freeTime:
# 		print "\n-------------------------------------------"
# 		print i
# 		attendees[i] = users
# 		print attendees[i]
# 		# for person in users:
# 		# 	print  "\n", person, location[person]


for i in range(10): # the number(n) inside range means output top n time slots
		#gawa pa ng condition dito. output 5 only if len(freeTime) >= 5
	freeTime.append(timeSlot[occurrence.index(min(occurrence))])
	del timeSlot[occurrence.index(min(occurrence))] #delete top 5 time slot here
	occurrence.remove(min(occurrence))
	
print "FREE TIME: ", freeTime	
for time in freeTime:
	att = []
	# timeSlot.append(time) #append top 5 time slot here
	for List in sched:
		# print "LIST ", List
		if time not in List and users[sched.index(List)] not in att:
			att.append(users[sched.index(List)])
	
	if len(att) == 1: freeTime.remove(time)
	if len(att) > 1: # at least 2 attendees
		print "\nMeeting time: ", time, "\nAttendees: ", att
		attendees[time] = att
			# for person in att:
# 			# 	print "\n", person, location[person]
# unionAttendees = []
# for mylist in attendees.values():
# 	for person in mylist:
# 		if person not in unionAttendees:
# 			unionAttendees.append(person)
#list yung top 5 na pinakamaraming attendees

# print location
# print mplace
# print attendees #lahat ng time slot from 7 am to 8 pm

timeSlot = ['7:00 AM - 7:30 AM', '7:30 AM - 8:00 AM', '8:00 AM - 8:30 AM', '8:30 AM - 9:00 AM', '9:00 AM - 9:30 AM',
			'9:30 AM - 10:00 AM', '10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM', '11:30 AM - 12:00 PM',
			'12:00 PM - 12:30 PM', '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM',
			'2:30 PM - 3:00 PM', '3:00 PM - 3:30 PM', '3:30 PM - 4:00 PM', '4:00 PM - 4:30 PM', '4:30 PM - 5:00 PM',
			'5:00 PM - 5:30 PM', '5:30 PM - 6:00 PM', '6:00 PM - 6:30 PM', '6:30 PM - 7:00 PM', '7:00 PM - 7:30 PM',
			'7:30 PM - 8:00 PM']
# ----------------------------------------------
# R E C O M M E N D A T I O N   N G   T I M E 
	#getting top5 schedule (if freeTime > 5)


#print "timeRanking:"
#print TimeRanking

unionAttendees = []

for mylist in attendees.values():
	for person in mylist:
		if person not in unionAttendees:
			unionAttendees.append(person)

#print "union: "
#print unionAttendees		

number_attendees = len(unionAttendees)
number_best_scheds = len(freeTime)

index_list = [] #contains index ng mga freeTime
for i in range(0, number_best_scheds):
	index_list.append(timeSlot.index(freeTime[i])) #PWEDE SINCE VAL IN FREE TIME IS UNIQUE
print "INDEX LIST",  index_list

print "FREE TIME ", freeTime
#Getting the ratings ng mga attendees
rating_time = []
for key, value in TimeRanking.iteritems():
	personList = []
	print "\nTIME RANKING KEY \n",TimeRanking[key]
	for free_time_index in index_list:
		#print TimeRanking[key][free_time_index]
		personList.append(TimeRanking[key][free_time_index])
	rating_time.append(personList)
	print "RATING TIME: ", rating_time
	#print '\n'

rating_list = [None]*number_best_scheds #eto yung storage ng mga average rating ng freeTime

#Ilagay sa rating_list yung average rating
# for iter in range(0,number_best_scheds):
# 	mySum = 0
# 	for i in rating_time:
# 		print "i[iter] is ", i[iter]
# 		for j in i[iter]: # i is the 
# 			print "j is ", j
# 			mySum = mySum+int(j)
# 		print mySum
# 	print "new"
# 	rating_list[iter] = float(mySum)/number_attendees
# print "\nNUMBER OF ATTENDEES: \n", number_attendees
# ==================================
for index in range(0, number_best_scheds):
	mySum = 0
	for iter in range(0, len(rating_time)):
		mySum +=  int(rating_time[iter][index])
	rating_list[index] = float(mySum)/number_attendees
print rating_list

for i in rating_list:
	print timeSlot[index_list[rating_list.index(i)]], i
# ==================================
#print rating_list
#rating_list = [7.2, 8.1, 4.3, 9.2, 1.0, 7.5, 6.3, 9.9] #DUMMY

# rating_list.sort(reverse = True)

# if (len(rating_list) > 5):
# 	for i in range(0, len(rating_list)):
# 		if i >= 5:
# 			del rating_list[-1]

print "RATING LIST: ", rating_list
while(len(rating_list) > 5):
	minimum = min(rating_list)
	del index_list[rating_list.index(minimum)]
	rating_list.remove(minimum)
	

print rating_list

# --------------------------------------------- 





""" RECOMMENDATION NA NG PLACE TO """

#GAWAN NG WAY PARA MAKUHA FROM RECOMMENDER. KUHA NG AT MOST 5
meetingTime = []
for i in index_list:
	meetingTime.append(timeSlot[i])
# meetingTime = ['6:00 PM - 6:30 PM', '6:30 PM - 7:00 PM', '7:00 PM - 7:30 PM','7:30 PM - 8:00 PM', '7:00 AM - 7:30 AM',
				# '7:30 AM - 8:00 AM', '8:00 AM - 8:30 AM', '5:30 PM - 6:00 PM', '11:30 AM - 12:00 PM', '12:00 PM - 12:30 PM',] #assuming na ito muna yung output na top
# index = timeSlot.index(meetingTime)
locB4Meet = {} #keys: time, values: dictionary: keys : person, values: location before time na yun
# shallAttend = attendees[meetingTime] #final list ng aattend
shallAttend = {} # key: time (string), values: attendees (list)
print timeSlot 
for time in meetingTime:
	shallAttend[time] = attendees[time]
	# print time
	# print timeSlot
	index = timeSlot.index(time)
	if index-1 >=0 : index = index-1
	print "index is ", timeSlot.index(time),  "time is ", time
	loc = {}
	for person in shallAttend[time]:
		# loc.append(person)
		# loc.append(location[person][index-1])
		loc[person] = location[person][index]
	locB4Meet[time] = loc #same sila ng key ng shallattend
		# loc = []


print "\nTHISSSSSSSSSSSSS\n", locB4Meet

# for meeting place, use mplace{} nalang



# shallAttend = attendees[meetingTime] #final list ng aattend
# attendees[meetingTime] key: time, values: aattend na list	
# print "meetplace", mplace
# for attendeesList in (shallAttend.values()):
# 	for person in attendeesList:
# 		MeetingPlaceChoices[person] = mplace[person] #final list ng pagpipiliang meeting place, ginawa ulit kasi pwedeng
# print "\nPLACE: ", MeetingPlaceChoices

# print MeetingPlaceChoices
# print shallAttend
# LocB4Meet = {}
# for time in meetingTime:
# 	index = timeSlot(time)
# 	for attendeesList in shallAttend.values():
# 		for person in attendeesList: 
# 			LocB4Meet[person] = location[person][index-1]

# print LocB4Meet

# """
#  for each place in MPChoices, i check kung gaano kalapit per person
# choose meeting place based on what? nearness. so parang average lang?
# total distance travelled over number of attendees?
#  """


up_bldg = os.path.join('up_bldg.csv')
up_road = os.path.join('up_road.csv')
up_edge = os.path.join('up_edge.csv')

up_bldgs = {}
up_names = {}
with open(up_bldg, 'rb') as csvfile:
    node = csv.reader(csvfile, delimiter=',', quotechar='|')
    for n in node:
        l_name = n[0].strip()
        l_x = n[1].strip()
        l_y = n[2].strip()
        up_bldgs[l_name] = (int(l_x), int(l_y))
        

up_roads = up_bldgs
with open(up_road, 'rb') as csvfile:
    node = csv.reader(csvfile, delimiter=',', quotechar='|')
    for n in node:
        l_name  = n[0].strip()
        l_x  = n[1].strip()
        l_y  = n[2].strip()
        up_roads[l_name] = (int(l_x), int(l_y))
        
up_edges = {}
with open(up_edge, 'rb') as csvfile:
    node = csv.reader(csvfile, delimiter=',', quotechar='|')
    for n in node:
        l_name  = n[0].strip()
        l_loc = up_roads[l_name]

        connected_roads = {}
        for link in n[1:]:
            m_id = link.strip()
            m_loc = up_roads[m_id]
            dist = distance(l_loc, m_loc)
            connected_roads[m_id] = distance(l_loc, m_loc)
            # print
        up_edges[l_name] = connected_roads
        # print connected_roads

            # print l_name, ':', up_edges[l_name], '\n',

# START HERE

MeetingPlaceChoices = {}
for time in meetingTime:
	meetplaceAtTime = []
	for person in shallAttend[time]:
		if (mplace[person] not in meetplaceAtTime): meetplaceAtTime.append(mplace[person])
	MeetingPlaceChoices[time] = meetplaceAtTime

print "\nMPLACE\n", MeetingPlaceChoices 

distAtTime = {} #distances
for time in meetingTime:
	distToMplace = {}
	for place in MeetingPlaceChoices[time]:
		dist = []
		for loc in locB4Meet[time].values():
			dist.append((distance(up_bldgs[loc.upper()], up_bldgs[place.upper()])))
		#na average na ung dist for that certain place
		distToMplace[place] = sum(dist)/len(shallAttend[time])
	distAtTime[time] = distToMplace


print "\nHERE WE ARE AGAIN\n"
for dist in distAtTime:
	print dist, locB4Meet[dist]
	print dist, distAtTime[dist]
	print "\n"

# print distAtTime['6:00 PM - 6:30 PM'].values()
""" get final meeting places """

print "\nFINAL\n"
finalMplace = {}
for time in meetingTime:
	finalMplace[time] =  distAtTime[time].keys()[distAtTime[time].values().index(min(distAtTime[time].values()))]   
	print time, finalMplace[time]

print finalMplace
# END HERE


# experiment coding start here huhu

# currTime2 = r_time[r_rate.index(min(r_rate))]

# del r_time[r_rate.index(min(r_rate))]
# r_rate.remove(min(r_rate))

# ratings = {'6:00 PM - 6:30 PM':6, '6:30 PM - 7:00 PM':7, '7:00 PM - 7:30 PM':7,'7:30 PM - 8:00 PM': 5,'7:00 AM - 7:30 AM': 2
# 			'7:30 AM - 8:00 AM':2, '8:00 AM - 8:30 AM':2, '5:30 PM - 6:00 PM':6, '11:30 AM - 12:00 PM':4, 
# 			'12:00 PM - 12:30 PM':4}

ratings = {}
for rate in rating_list:
	ratings[timeSlot[index_list[rating_list.index(rate)]]] = rate
print ratings
# ^ dummy ratings

#dummy score

# score_place = {'6:00 PM - 6:30 PM':{'DCS': min(distAtTime['6:00 PM - 6:30 PM'].values())},
# 				'6:30 PM - 7:00 PM':{'PALMA':min(distAtTime['6:30 PM - 7:00 PM'].values())},
# 				'7:00 PM - 7:30 PM':{'PALMA':min(distAtTime['7:00 PM - 7:30 PM'].values())},
# 				'7:30 PM - 8:00 PM': {'PALMA':min(distAtTime['7:30 PM - 8:00 PM'].values())},
# 				'7:00 AM - 7:30 AM': {'DCS':min(distAtTime['7:00 AM - 7:30 AM'].values())},
# 				'7:30 AM - 8:00 AM': {'DCS':min(distAtTime['7:30 AM - 8:00 AM'].values())},
# 				'8:00 AM - 8:30 AM': {'PALMA':min(distAtTime['8:00 AM - 8:30 AM'].values())},
# 				'5:30 PM - 6:00 PM': {'PALMA':min(distAtTime['5:30 PM - 6:00 PM'].values())},
# 				'11:30 AM - 12:00 PM': {'PALMA':min(distAtTime['11:30 AM - 12:00 PM'].values())},
# 				'12:00 PM - 12:30 PM': {'PALMA':min(distAtTime['12:00 PM - 12:30 PM'].values())},
# 				}

print finalMplace
score_place = {}
for time in meetingTime:
	score_place[time] = {finalMplace[time] : min(distAtTime[time].values())}
print score_place

print score_place

alreadyChecked = []
r_time = ratings.keys()
r_rate = ratings.values()

currRate1 = min(r_rate)
currTime1 = r_time[r_rate.index(currRate1)]
currPlace1 = score_place[currTime1].values()[0]
print "herehere", currPlace1

del r_time[r_rate.index(min(r_rate))]
r_rate.remove(min(r_rate))

maxSoFar = 0
tempPlace = ''
tempTime = ''
w_r1 = 0
w_d1 = 0
w_r2 = 0
w_d2 = 0
while (len(r_time) != 0 ):
	currRate2 = min(r_rate)
	currTime2 = r_time[r_rate.index(currRate2)]
	currPlace2 = score_place[currTime2].values()[0]

	del r_time[r_rate.index(min(r_rate))]
	r_rate.remove(min(r_rate))

	#SOLVE THE EQUATION HERE
	diff = abs(currRate2-currRate1)
	r_max = max(currRate1, currRate2)
	if (diff >= 0.1 and diff < 0.3):
		if r_max == currRate1: w_r1 = 1.2; w_r2 = 1.1 
		else: w_r1 = 1.1; w_r2 = 1.2
	elif (diff >= 0.3 and diff < 1):
		if r_max == currRate1: w_r1 = 1.4; w_r2 = 1.2 
		else: w_r1 = 1.2; w_r2 = 1.4
	elif (diff >= 1 and diff < 1.5):
		if r_max == currRate1: w_r1 = 1.7; w_r2 = 1.4
		else: w_r1 = 1.4; w_r2 = 1.7
	elif (diff >= 1.5 and diff < 2):
		if r_max == currRate1: w_r1 = 1.9; w_r2 = 1.4
		else: w_r1 = 1.4; w_r2 = 1.9
	elif (diff >= 2): #meaning masyado na malaki yung gap
		if r_max == currRate1: w_r1 = 2; w_r2 = 1.5 
		else: w_r1 = 1.5; w_r2 = 2
	else:
		w_r1 = 1; w_r2 = 1

	diff = abs(currPlace2 - currPlace1)
	d_min = min(currPlace1, currPlace2)

	if (diff >= 30 and diff < 100):
		if d_min == currPlace1: w_d1 = 0.3; w_d2 = 0.1 
		else: w_d1 = 0.1; w_d2 = 0.5 
	elif (diff >= 100 and diff < 175):
		if d_min == currPlace1: w_d1 = 0.4; w_d2 = 0.2
		else: w_d1 = 0.2; w_d2 = 0.4
	elif (diff >= 175 and diff < 250):
		if d_min == currPlace1: w_d1 = 0.7; w_d2 = 0.4 
		else: w_d1 = 0.4; w_d2 = 0.7
	elif (diff >= 250 and diff < 350):
		if d_min == currPlace1: w_d1 = 0.9; w_d2 = 0.4
		else: w_d1 = 0.4; w_d2 = 0.9
	elif (diff >= 350): #meaning masyado na malaki yung gap
		if d_min == currPlace1: w_d1 = 1; w_d2 = 0.5 
		else: w_d1 = 0.5; w_d2 = 1
	else:
		w_d1 = 1; w_d2 = 1
	#mag set ng bounds here

	total1 = w_r1*currRate1 + w_d1*currPlace1
	total2 = w_r2*currRate2 + w_d2*currPlace2
	maxSoFar = max(total1, total2)
	print "currTime1 : currRate1 : score_place[currTime1]  :  total1  : w_r1  :  currRate1  :   w_d1 : currPlace1"
	print currTime1, " : ", currRate1, " : ", score_place[currTime1]," : ",  total1, " : ",w_r1, " : ",currRate1 ," : ",  w_d1, " : ",currPlace1
	print currTime2, " : ", currRate2, " : ", score_place[currTime2]," : ",  total2," : ",w_r2, " : ",currRate2 ," : ",  w_d2, " : ",currPlace2
	print maxSoFar
	if maxSoFar == total2:
		currRate1 = currRate2
		currPlace1 = currPlace2
		currTime1 = currTime2
		tempPlace = currPlace2
		tempTime = currTime2
	else:
		tempPlace = currPlace1
		tempTime = currTime1

print "\nRECOMMENDED TIME : PLACE\n"
print tempTime, ' : ', tempPlace, score_place[tempTime].keys()[0]
# experiment coding end here

# shallAttend = attendees[meetingTime] #final list ng aattend
# attendees[meetingTime] key: time, values: aattend na list





# newdicTime = {}
# newdicMplace = {}
# placedist = []
# for time in meetingTime:
# 	for place in MeetingPlaceChoices.values():
# 		for mylist in shallAttend.values():
# 			for person in mylist:
# 				# print up_bldgs[LocB4Meet[person].upper()], up_bldgs[place.upper()]
# 				placedist.append(utils.distance(up_bldgs[(locB4Meet[time][person]).upper()], up_bldgs[place.upper()]))
# 			newdicMplace[place] = placedist
# 			newdicTime = newdicMplace
# 			placedist = []

# print newdicTime
# print "Loc", LocB4Meet
# print "mp", MeetingPlaceChoices
# places = newdicMplace.keys()
# # print "THIS ", places
# dist = newdicMplace.values()
# mindist = sum(dist[0])/len(shallAttend)
# minlist = dist[0]
# minlist = []

# print "\nRECOMMENDED TIME: \n", meetingTime
# print "\nATTENDEES: \n", shallAttend
# print "\nLocation before meeting time: \n", LocB4Meet
# print "\npreferred meet place: \n", MeetingPlaceChoices

# print "\nMEETING PLACE: DISTANCES \n", newdicMplace
# print "\n"
# for a in dist:
# 	print places[dist.index(a)]," : ", a, sum(a)/len(shallAttend)
# 	if (mindist > sum(a)/len(shallAttend)): mindist = sum(a)/len(shallAttend); minlist = a

# print "\nRecommended Meeting Place: ", places[dist.index(minlist)]s