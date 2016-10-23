from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt

import sys

import classrooms

courses      = {}
rooms_used   = {}

# list of buildings
buildings    = {}

# list of rooms for a given building
rooms        = {}


if __name__ == "__main__":
    if(len(sys.argv) > 1):
        filename =  sys.argv[1] 
        wb = load_workbook(filename)
        ws = wb.active
        for i in range(2, len(ws.rows)):
            index_building = "AC" + str(i)
            index_room     = "AD" + str(i)
            index_course = "I" + str(i)
            index_count  = "M" + str(i)
            course = ws[index_course].value
            count  = ws[index_count].value

            building = ws[index_building].value
            room     = ws[index_room].value
            location = str(building) + " " + str(room)

            if building not in buildings:
                # add new building to dictionary
                buildings[building] = {}

            #print(room in buildings[building])
            if room in buildings[building]:
                buildings[building][room] = buildings[building][room] + 1
            else:
                buildings[building][room] = 1


            # tally of the number of courses that use this room
            #if location in buildings[rooms[location]]:
            #    buildings[rooms[location]] = buildings[rooms[location]] + 1
            #else:
            #    buildings[rooms[location]] = 1

            #if course in courses:
            #    courses[course] = courses[course] + count 
            #else:
            #    courses[course] = count

    del buildings[None]
    del buildings["COFC"]
    #for course, count in courses.items():
    #    print(course, count)


    for loc, value in buildings.items():
        #print(loc)
        if loc in classrooms.code:
            print(classrooms.code[loc], "(" + loc + ")")
        else:
            print("Unknown Location", "(" + loc + ")")
        for i, ct in value.items():
            print("\t",i, ct)
        #for room in loc.items():
        #    print(room)


    #D = {u'Label1':26, u'Label2': 17, u'Label3':30}

    # Remove courses with no room assigned
    #del buildings[rooms['None None']]
    #plt.bar(range(len(rooms_used)), rooms_used.values(), align='center')
    #plt.xticks(range(len(rooms_used)), list(rooms_used.keys()))

    #plt.show()




