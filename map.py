import Tkinter as Tk
import os, sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


import utils
import model
import mechanism
import csv

# GUI Setup
RED = "#ff7d70"
BLACK = "#333"
GRAY_r = "#ccc9c9"
GRAY_b = "#a5a2a2"
BLUE = "#3498db"

if __name__ == '__main__':
    src, dest = None, None

    cd = os.path.dirname(os.path.realpath(__file__))
    p = os.path.join('UPD_Map.gif')

    root = Tk.Tk()
    root.resizable(width=False, height=False)

    bg_image = Tk.PhotoImage(file=p)
    w_width, w_height = bg_image.width()-5, bg_image.height()

    canvas = Tk.Canvas()
    canvas.pack(expand = Tk.YES, fill = Tk.BOTH)
    canvas.create_image(0, 0, image = bg_image, anchor = Tk.NW)

# Get locations
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
                dist = utils.distance(l_loc, m_loc)
                connected_roads[m_id] = utils.distance(l_loc, m_loc)

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

# Path Finding
    up_map = model.UndirectedGraph(up_edges)
    up_map.locations = up_bldgs

    src = None
    dest = None
# Get data from csv file from survey
    src = 'DCS'
    dest = 'CHK'
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

# ______________________________________________________________________________
