import csv
import math
import Tkinter as Tk
import os, sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import utils
import model
import mechanism

def distance(a, b):
    """ The distance between two (x, y) points. """
    return math.hypot((a[0] - b[0]), (a[1] - b[1]))


def findFreeTime(list, occ):
	for i in range(10):
		obj = MeetTime(timeSlot[occ.index(min(occ))])
		list.append(obj)
		del timeSlot[occ.index(min(occ))]
		occ.remove(min(occ))

BLACK = "#333"
GRAY_r = "#ccc9c9"
GRAY_b = "#a5a2a2"
RED = "#ff7d70"
BLUE = "#3498db"

cd = os.path.dirname(os.path.realpath(__file__))
p = os.path.join('UPD_Map.gif')

root = Tk.Tk()
root.resizable(width=False, height=False)

bg_image = Tk.PhotoImage(file=p)
w_width, w_height = bg_image.width()-5, bg_image.height()

canvas = Tk.Canvas()
canvas.pack(expand = Tk.YES, fill = Tk.BOTH)
canvas.create_image(0, 0, image = bg_image, anchor = Tk.NW)

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

users = []          #list ng object ng attendee class

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
tempInterOp['Area 2'] = 'AREA2'
tempInterOp['NISMED/ITDC'] = 'ITDC'
tempInterOp['Melchor Hall'] = 'MELCHOR'
tempInterOp['AS'] = 'PALMA'
tempInterOp['Infirmary'] = 'UHS'
tempInterOp['Main Lib'] = 'LIB'
tempInterOp['Balay Kalinaw'] = 'BALAY'
tempInterOp['Business Ad'] = 'BA'
tempInterOp['Vinzons Hall'] = 'VINZONS'
tempInterOp['CS Lib'] = 'CSLIB'

class Attendee:
	def __init__(self, username):
		self.name = username
		self.schedule = []
		self.rating = []
		self.location = []
		self.mplace = ''

	def fixSchedule(self, occurrence, timeSlot):
		classes = []
		for val in self.rating:
			if val == '0':
				occurrence[self.rating.index(val)] +=1              #if zero ilagay sa isang list
				classes.append(timeSlot[self.rating.index(val)])
				self.rating[self.rating.index(val)] = "-1"
			else:
				continue

		self.schedule = classes

		for val in self.rating:
			if val == "-1": self.rating[self.rating.index(val)] = 0

class MeetTime:
	def __init__(self, time):
		self.time = time
		self.attendees = []
		self.finalMplace = ''
		self.MplaceChoices = []
		self.distances = {}
		self.rate = 0

	# NOTE : create a function na magtatanggal ng freetime na 1 lang yung attendee

	def getAttendees(self, User):          #schedule is from attendees.schedule or should this be a class?
		if self.time not in User.schedule and User.name not in self.attendees:
			self.attendees.append(User)

	def getMplaceChoices(self):
		for person in self.attendees:
			if person.mplace not in self.MplaceChoices:
				self.MplaceChoices.append(person.mplace)

	def distance(self, a, b):
		""" The distance between two (x, y) points. """
		return math.hypot((a[0] - b[0]), (a[1] - b[1]))

	def findFinalMplace(self):
		for place, dist in self.distances.iteritems():
			if dist == min(self.distances.values()):
				self.finalMplace = place

	def computeRating(self, unionAttendees):
		currSum = 0
		for person in unionAttendees:
			currSum = currSum + int(person.rating[timeSlot.index(self.time)])
		self.rate = float(currSum)/len(unionAttendees)

	def getDistance(self, timeSlot):
		global unionAttendees
		for place in self.MplaceChoices:
			index = timeSlot.index(self.time) - 1
			distToMplace = []
			for person in self.attendees:
				if index < 0 : index = 0
				distToMplace.append(distance(up_bldgs[person.location[index]], up_bldgs[place]))
			self.distances[place] = float(sum(distToMplace))/ len(unionAttendees)

""" IMPORT CSV FILES """

with open('MeetUP.csv', 'rb') as csvfile:
	node = csv.reader(csvfile, delimiter=',', quotechar='|')

	for n in node:
		if (n[0].strip() != "Timestamp"):

			username = Attendee(n[1].strip())
			users.append(username)

			col=2

			""" FREE TIME RANKING """
			rank=[]
			for counter in range(26):
				rank.append(n[col].strip()); col+=1
			username.rating = rank

			""" LOCATION AT EACH TIME """
			loc = []
			for counter in range(26):
				p = n[col].strip()
				if p in tempInterOp.keys():
					loc.append(tempInterOp[p])
				else:
					loc.append(p.upper())
				col+=1
			username.location = loc
			""" PREFERRED MEETING PLACE """

			p = n[col].strip()
			if p in tempInterOp.keys():
				mplace =  tempInterOp[p]
			else:
				mplace = p.upper()
			username.mplace = mplace


unionAttendees = []
occurrence = [0]* 26

for obj in users:
	obj.fixSchedule(occurrence, timeSlot)

freeTime = []

findFreeTime(freeTime, occurrence)
for time in freeTime:
	for obj in users:
		time.getAttendees(obj)
	if len(time.attendees) == 1: freeTime.remove(time) #check kung gumagana this some time

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
for time in freeTime:
	for person in time.attendees:
		if person not in unionAttendees:
			unionAttendees.append(person)

rating_list = {}
for time in freeTime:
	time.computeRating(unionAttendees)
	# print time.time, time.rate

while(len(freeTime) > 5):
	toDelete = freeTime[0]
	minimum = freeTime[0].rate
	for time in freeTime:
		if minimum > time.rate:
			toDelete = time
			minimum = time.rate
	freeTime.remove(toDelete)

# """ RECOMMENDATION NA NG PLACE TO """

for time in freeTime:
	time.getMplaceChoices()

for time in freeTime:
	time.getDistance(timeSlot)
for time in freeTime:
	time.findFinalMplace()
print "Meeting Time\t\tTime Rating\t\tMeeting Place\t\tAverage Distance To Place\t\tPoints"
curr1 = freeTime[0]
currDistToPlace1 = freeTime[0].distances[time.finalMplace]
maxSoFar = 0
tempCurr = ''
tempDistToPlace = ''
w_r1 = 0; w_d1 = 0; w_r2 = 0; w_d2 = 0

for time in freeTime[1:]:
	curr2 = time
	currDistToPlace2 = time.distances[time.finalMplace]

	#SOLVE THE EQUATION HERE
	diff = abs(curr2.rate-curr1.rate)
	r_max = max(curr1.rate, curr2.rate)
	if (diff >= 0.1 and diff < 0.3):
		if r_max == curr1.rate: w_r1 = 1.2; w_r2 = 1.1
		else: w_r1 = 1.1; w_r2 = 1.2
	elif (diff >= 0.3 and diff < 1):
		if r_max == curr1.rate: w_r1 = 1.4; w_r2 = 1.2
		else: w_r1 = 1.2; w_r2 = 1.4
	elif (diff >= 1 and diff < 1.5):
		if r_max == curr1.rate: w_r1 = 1.7; w_r2 = 1.4
		else: w_r1 = 1.4; w_r2 = 1.7
	elif (diff >= 1.5 and diff < 2):
		if r_max == curr1.rate: w_r1 = 1.9; w_r2 = 1.4
		else: w_r1 = 1.4; w_r2 = 1.9
	elif (diff >= 2): #meaning masyado na malaki yung gap
		if r_max == curr1.rate: w_r1 = 2; w_r2 = 1.5
		else: w_r1 = 1.5; w_r2 = 2
	else:
		w_r1 = 1; w_r2 = 1

	diff = abs(currDistToPlace2 - currDistToPlace1)
	d_min = min(currDistToPlace1, currDistToPlace2)

	if (diff >= 30 and diff < 100):
		if d_min == currDistToPlace1: w_d1 = 0.3; w_d2 = 0.1
		else: w_d1 = 0.1; w_d2 = 0.5
	elif (diff >= 100 and diff < 175):
		if d_min == currDistToPlace1: w_d1 = 0.4; w_d2 = 0.2
		else: w_d1 = 0.2; w_d2 = 0.4
	elif (diff >= 175 and diff < 250):
		if d_min == currDistToPlace1: w_d1 = 0.7; w_d2 = 0.4
		else: w_d1 = 0.4; w_d2 = 0.7
	elif (diff >= 250 and diff < 350):
		if d_min == currDistToPlace1: w_d1 = 0.9; w_d2 = 0.4
		else: w_d1 = 0.4; w_d2 = 0.9
	elif (diff >= 350): #meaning masyado na malaki yung gap
		if d_min == currDistToPlace1: w_d1 = 1; w_d2 = 0.5
		else: w_d1 = 0.5; w_d2 = 1
	else:
		w_d1 = 1; w_d2 = 1
	#mag set ng bounds here

	total1 = w_r1*curr1.rate + w_d1*currDistToPlace1
	total2 = w_r2*curr2.rate + w_d2*currDistToPlace2
	maxSoFar = max(total1, total2)

	if maxSoFar == total2:
		print curr1.time, "\t\t", int(curr1.rate),"\t\t", curr1.finalMplace,"\t\t", int(curr1.distances[curr1.finalMplace]), "\t\t", total1
		curr1 = curr2
		currDistToPlace1 = currDistToPlace2
		tempDistToPlace = currDistToPlace2
		tempCurr = curr2
		tempTotal = total2

	else:
		print curr2.time, "\t\t", int(curr2.rate),"\t\t", curr2.finalMplace,"\t\t", int(curr2.distances[curr2.finalMplace]), "\t\t", total2
		tempDistToPlace = currDistToPlace1
		tempCurr = curr1
		tempTotal = total1

print tempCurr.time, "\t\t", int(tempCurr.rate),"\t\t", tempCurr.finalMplace,"\t\t", int(tempCurr.distances[tempCurr.finalMplace]), "\t\t", tempTotal
print "\nRECOMMENDED TIME AND PLACE\n"
print tempCurr.time, ' : ',tempCurr.finalMplace

print "Attendees: ",
for person in tempCurr.attendees:
    print person.name,
print "\n\n",

t = timeSlot.index(tempCurr.time)

up_map = model.UndirectedGraph(up_edges)
up_map.locations = up_bldgs
search = True

if __name__ == '__main__':
    user, src, dest = None, None, None
    user_found = False

    if len(sys.argv) <= 1:
        search = False
    else:
        user = sys.argv[1]
        for person in tempCurr.attendees:
            if user == person.name:
                user = person.name
                src = person.location[t-1]
                user_found = True

    if search and user_found:
        dest = tempCurr.finalMplace

        welcome = "WELCOME TO MeetUP!"
        canvas.create_text(220, 180, text=welcome, anchor="e", fill=BLACK, justify = "center")
        message = "Hi, %s! \nYour meeting is at %s to be held at %s. \nYou will be coming from %s." % (user, tempCurr.time, up_names[dest], up_names[src])
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
