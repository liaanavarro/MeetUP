import csv
import math

import Tkinter as Tk
import os, sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


import utils
import model
import mechanism
BLACK = "#333"
GRAY_r = "#ccc9c9"
GRAY_b = "#a5a2a2"

RED = "#ff7d70"
BLUE = "#3498db"
GREEN = "#93b75d"
VIOLET = "#a54281"

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
tempInterOp['Area 2'] = "AREA2"
tempInterOp['NISMED/ITDC'] = 'ITDC'
tempInterOp['Melchor Hall'] = 'MELCHOR'
tempInterOp['AS'] = 'PALMA'
tempInterOp['Infirmary'] = 'UHS'
tempInterOp['Main Lib'] = 'LIB'
tempInterOp['Balay Kalinaw'] = 'BALAY'
tempInterOp['Business Ad'] = 'BA'
tempInterOp['Vinzons Hall'] = 'VINZONS'
tempInterOp['CS Lib'] = 'CSLIB'



""" IMPORT CSV FILES """

with open('MeetUP.csv', 'rb') as csvfile:
	node = csv.reader(csvfile, delimiter=',', quotechar='|')

	for n in node:
		username = n[1].strip()
		if (username[0] != '#' and n[0].strip() != "Timestamp"):

			""" SCHEDULE """
			sched = n[2].strip('"')
			col=3
			schedList = []
			while (sched[-1] == 'M'):
				if (sched[0] == ' '):
					sched = sched[1:]
				schedList.append(sched)
				sched = n[col].strip('"'); col+=1

			""" FREE TIME RANKING """
			rank=[]
			col=col-1
			for counter in range(26):
				rank.append(n[col].strip()); col+=1
			TimeRanking[username] = rank

			schedule[username] = schedList

			""" LOCATION AT EACH TIME """
			loc = []
			for counter in range(26):
				p = n[col].strip()
				if p in tempInterOp.keys():
					loc.append(tempInterOp[p])
				else:
					loc.append(p.upper())
				col+=1
			location[username] = loc

			""" PREFERRED MEETING PLACE """
			p = n[col].strip()
			if p in tempInterOp.keys():
				mplace[username] =  tempInterOp[p]
			else:
				mplace[username] = p.upper()

""" GET TOP 10 SCHEDULES (MAX ATTENDEES) """
sched = schedule.values()
occurrence = [0] * 26 #initialy 0 yung count. counts kung iang people yung di free at each timeslot

for List in sched:
	for time in List:
		occurrence[timeSlot.index(time)] +=1

freeTime = [] # LAHAT NG  AVAILABLE NA TIME

for i in range(26):
	if occurrence[i] == 0: #meaning may common time na free lahat
		freeTime.append(timeSlot[i])

'''
attendees[] - list of lists ng attendees per available time
freeTime[] - list ng available free time
'''
attendees = {}
users = schedule.keys()
sched = schedule.values()

for i in range(10): # the number(n) inside range means output top n time slots
	freeTime.append(timeSlot[occurrence.index(min(occurrence))])
	del timeSlot[occurrence.index(min(occurrence))] #delete top 5 time slot here
	occurrence.remove(min(occurrence))

for time in freeTime:
	att = []
	timeSlot.append(time) #append top 5 time slot here
	for List in sched:
		if time not in List and users[sched.index(List)] not in att:
			att.append(users[sched.index(List)])
	attendees[time] = att

unionAttendees = []
for mylist in attendees.values():
	for person in mylist:
		if person not in unionAttendees:
			unionAttendees.append(person)

timeSlot = ['7:00 AM - 7:30 AM', '7:30 AM - 8:00 AM', '8:00 AM - 8:30 AM', '8:30 AM - 9:00 AM', '9:00 AM - 9:30 AM',
			'9:30 AM - 10:00 AM', '10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM', '11:30 AM - 12:00 PM',
			'12:00 PM - 12:30 PM', '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM',
			'2:30 PM - 3:00 PM', '3:00 PM - 3:30 PM', '3:30 PM - 4:00 PM', '4:00 PM - 4:30 PM', '4:30 PM - 5:00 PM',
			'5:00 PM - 5:30 PM', '5:30 PM - 6:00 PM', '6:00 PM - 6:30 PM', '6:30 PM - 7:00 PM', '7:00 PM - 7:30 PM',
			'7:30 PM - 8:00 PM']
# ----------------------------------------------
# R E C O M M E N D A T I O N   N G   T I M E
	#getting top5 schedule (if freeTime > 5)

unionAttendees = []

for mylist in attendees.values():
	for person in mylist:
		if person not in unionAttendees:
			unionAttendees.append(person)

number_attendees = len(unionAttendees)
number_best_scheds = len(freeTime)

index_list = [] #contains index ng mga freeTime
for i in range(0, number_best_scheds):
	index_list.append(timeSlot.index(freeTime[i]))

#Getting the ratings ng mga attendees
rating_time = []
for key, value in TimeRanking.iteritems():
	personList = []
	for free_time_index in index_list:
		personList.append(TimeRanking[key][free_time_index])
	rating_time.append(personList)

rating_list = [None]*number_best_scheds #eto yung storage ng mga average rating ng freeTime

#Ilagay sa rating_list yung average rating
for iter in range(0,number_best_scheds):
	mySum = 0
	for i in rating_time:
		for j in i[iter]: # i is the
			mySum = mySum+int(j)
	rating_list[iter] = float(mySum)/number_attendees

rating_list.sort(reverse = True)

while(len(rating_list) > 5):
	minimum = min(rating_list)
	del index_list[rating_list.index(minimum)]
	rating_list.remove(minimum)

# ---------------------------------------------

""" RECOMMENDATION NA NG PLACE TO """

#GAWAN NG WAY PARA MAKUHA FROM RECOMMENDER. KUHA NG AT MOST 5
meetingTime = []
for i in index_list:
	meetingTime.append(timeSlot[i])
locB4Meet = {} #keys: time, values: dictionary: keys : person, values: location before time na yun
# shallAttend = attendees[meetingTime] #final list ng aattend
shallAttend = {} # key: time (string), values: attendees (list)
for time in meetingTime:
	shallAttend[time] = attendees[time]
	index = timeSlot.index(time)
	if index-1 >=0 : index = index-1
	loc = {}
	for person in shallAttend[time]:
		loc[person] = location[person][index]
	locB4Meet[time] = loc #same sila ng key ng shallattend



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
        name = n[3].strip()
        up_bldgs[l_name] = (int(l_x), int(l_y))
        up_names[l_name] = name


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
        up_edges[l_name] = connected_roads

# START HERE

MeetingPlaceChoices = {}
for time in meetingTime:
	meetplaceAtTime = []
	for person in shallAttend[time]:
		if (mplace[person] not in meetplaceAtTime): meetplaceAtTime.append(mplace[person])
	MeetingPlaceChoices[time] = meetplaceAtTime

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


finalMplace = {}
for time in meetingTime:
	finalMplace[time] =  distAtTime[time].keys()[distAtTime[time].values().index(min(distAtTime[time].values()))]
# END HERE

ratings = {}
for rate in rating_list:
	ratings[timeSlot[index_list[rating_list.index(rate)]]] = rate

score_place = {}
for time in meetingTime:
	score_place[time] = {finalMplace[time] : min(distAtTime[time].values())}

alreadyChecked = []
r_time = ratings.keys()
r_rate = ratings.values()

currRate1 = min(r_rate)
currTime1 = r_time[r_rate.index(currRate1)]
currPlace1 = score_place[currTime1].values()[0]


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

t = timeSlot.index(tempTime)

cd = os.path.dirname(os.path.realpath(__file__))
p = os.path.join('UPD_Map.gif')

root = Tk.Tk()
root.resizable(width=False, height=False)

bg_image = Tk.PhotoImage(file=p)
w_width, w_height = bg_image.width()-5, bg_image.height()

canvas = Tk.Canvas()
canvas.pack(expand = Tk.YES, fill = Tk.BOTH)
canvas.create_image(0, 0, image = bg_image, anchor = Tk.NW)

# Plot map on canvas
canvas_edges = {}
for node_1, connected_nodes in up_edges.iteritems():
    for node_2 in connected_nodes.keys():
        loc_1 = up_roads[node_1]
        loc_2 = up_roads[node_2]

        x0 = loc_1[0]
        x1 = loc_2[0]
        y0 = loc_1[1]
        y1 = loc_2[1]

        item = canvas.create_line(x0, y0, x1, y1, fill=GRAY_r, width=2.0, dash=(4, 2))
        canvas_edges[tuple(sorted((node_1, node_2)))] = item

canvas_nodes = {}
item_locs = {}
canvas_text = {}
for node, loc in up_bldgs.iteritems():
    name, color = '', GRAY_b
    radius = 2
    if "-" not in node:
        radius = 5
        color = RED
        name = up_names[node]

    x0, x1 = loc[0] - radius, loc[0] + radius
    y0, y1 = loc[1] - radius, loc[1] + radius

    item = canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)
    canvas_nodes[node] = item

    item_locs[item] = loc[0], loc[1]

    if name:
        text_id = canvas.create_text(x1-15, y1-radius, anchor="e", fill=GRAY_b, justify="center")

        if node == "BA":
                canvas.itemconfig(text_id, width=150)
                canvas.coords(text_id, x1+3, y1-12)
        elif node == "ECON":
            canvas.itemconfig(text_id, width=100)
            canvas.coords(text_id, x1+35, y1-30)
        elif node == "CHEM":
            canvas.coords(text_id, x1+70, y1-18)
        elif node == "ITDC":
            canvas.itemconfig(text_id, width=250)
            canvas.coords(text_id, x1+187, y1)
        elif node == "CHK":
            canvas.coords(text_id, x1+177, y1-radius)
        elif node == "NIP":
            canvas.itemconfig(text_id, width=150)
            canvas.coords(text_id, x1+55, y1+18)
        elif node == "CMC":
            canvas.itemconfig(text_id, width=150)
            canvas.coords(text_id, x1-12, y1+3)
        elif node == "SURP":
            canvas.itemconfig(text_id, width=120)
            canvas.coords(text_id, x1+3, y1-13)
        elif node == "VARGAS":
            canvas.coords(text_id, x1+107, y1-radius)
        elif node == "NIGS":
            canvas.coords(text_id, x1-13, y1)
        elif node == "QUEZON":
            canvas.coords(text_id, x1+83, y1-radius)
        elif node == "UHS":
            canvas.coords(text_id, x1+163, y1+9)
        elif node == "FA":
            canvas.coords(text_id, x1+133, y1-radius)
        elif node == "EDUC":
            canvas.coords(text_id, x1+60, y1+9)
        elif node == "CSLIB":
            canvas.itemconfig(text_id, width=100)
            canvas.coords(text_id, x1+88, y1+6)
        elif node == "OUR":
            canvas.itemconfig(text_id, width=90)
            canvas.coords(text_id, x1+87, y1+15)
        elif node == "SC":
            canvas.coords(text_id, x1+27, y1+7)
        elif node == "ARKI":
            canvas.coords(text_id, x1+3, y1+7)
        elif node == "THEATER":
            canvas.itemconfig(text_id, width=150)
            canvas.coords(text_id, x1+123, y1-radius)
        elif node == "MUSIC":
            canvas.itemconfig(text_id, width=150)
            canvas.coords(text_id, x1+115, y1-radius)
        elif node == "CSWCD":
            canvas.coords(text_id, x1+345, y1-radius)
        elif node == "MATH":
            canvas.coords(text_id, x1+70, y1+10)

        canvas.itemconfig(text_id, text=name)
        canvas_text[node] = text_id

up_map = model.UndirectedGraph(up_edges)
up_map.locations = up_bldgs

search = True

if __name__ == '__main__':
    user, src, dest = None, None, None

    if len(sys.argv) <= 1:
        search = False
    else:
        user = sys.argv[1]
        if user not in users:
            user = None

    if search and user:
        src = location[user][t-1]
        dest = score_place[tempTime].keys()[0]

        message = "Hi, %s! \nYour meeting is at %s to be held at %s. \nYou will be coming from %s." % (user, tempTime, up_names[dest], up_names[src])
        canvas.create_text(265, 300, text=message, anchor="e", fill=BLACK, justify="center", width=250)

        result = mechanism.astar_search(model.GraphProblem(src, dest, up_map))

        path = result.solution()
        a = src
        text = canvas_text[a]
        canvas.itemconfig(text, fill=BLACK)

        for i in range(len(path)):
            b = path[i]
            item = canvas_edges[tuple(sorted((a,b)))]
            canvas.itemconfig(item, fill=BLUE, width=3.0)
            item = canvas_nodes[a]
            loc = item_locs[item]
            radius = 3.5
            if "-" not in a:
                radius = 7

            x0, x1 = loc[0] - radius, loc[0] + radius
            y0, y1 = loc[1] - radius, loc[1] + radius

            canvas.delete(item)
            canvas.create_oval(x0, y0, x1, y1, fill=BLUE, outline=BLUE)

            a = b

        text = canvas_text[a]
        canvas.itemconfig(text, fill=BLACK)

        item = canvas_nodes[a]
        loc = item_locs[item]
        x0, x1 = loc[0] - 7, loc[0] + 7
        y0, y1 = loc[1] - 7, loc[1] + 7

        canvas.delete(item)
        canvas.create_oval(x0, y0, x1, y1, fill=BLUE, outline=BLUE)

    root.wm_title("UP Map")
    root.state('zoomed')
    w,h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' % (w, h, -w, 0))
    root.mainloop()
