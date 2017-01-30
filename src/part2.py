from openpyxl import Workbook
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import re
import sys
import datetime as dt
import dateutil.parser as dparser
import collections
import classrooms
import os
import platform
import textwrap as tw
import re

from rec import CourseRecord
from evaluation import ScheduleEvaluation
from score import RoomScore
from rooms import Classrooms
from reports import ScheduleReport
from location import LocationScore

def get_semester(filename):
    # Determine the semester statistics (Spring/Fall) and Year

    # todo: add search for summer as well
    semester = None
    year     = None

    # find the year
    year = re.findall(r'\d+', filename)
    year = year[0]

    # find the semester
    if "FA" in filename:
        semester = "Fall"
    if "SP" in filename:
        semester = "Spring"

    return semester, year

if __name__ == "__main__":

    records = []
    if(len(sys.argv) > 1):
        filename =  sys.argv[1] 
        wb = load_workbook(filename)
        ws = wb.active
        for i in range(2, len(ws.rows)+1): #needs +1 because apparently last entry is left off otherwise
            s = RoomScore()
            r = CourseRecord()
            r.read_rec(ws,i)
            records.append([r,s])
        semester, year = get_semester(filename)

    if(len(sys.argv) > 2):
        class_rooms = sys.argv[2]
    else:
        class_rooms = "all"

    # Any room with a rank > threshold has a good score
    good_threshold = 5.00 

    bad_scores  = collections.defaultdict(dict)
    good_scores = collections.defaultdict(dict)

    print("Evaluation of", semester, year,":")
    e = ScheduleEvaluation(records)

    # remove all unimportant rooms
    e.prune_records()
    e.calc_data()

    # score all rooms
    e.score_records()

    # reduce to only large rooms
    l = Classrooms(class_rooms)
    large = e.get_courses_in_location_list(l.get_rooms())
    large = ScheduleEvaluation(large)


    # Build a dictionary of all rooms that are relevant
    # This dict will contain score information for every course
    # related to a given room, which are all added together.
    room_dict = {}
    for room in l.get_rooms():
        room_data       = large.get_courses_in_location(room)

        # Only generate if this room was actually used at all this semester.
        if len(room_data) > 1:
            room_data       = ScheduleEvaluation(room_data)
            room_dict[room] = LocationScore(room_data)

    mini =  10000
    maxi = -10000
    # Normalize weights
    for room in room_dict:
        # Plot all room analysis
        final_score = room_dict[room].get_final_weighted_score()    

        if mini > final_score:
            mini = final_score
        if maxi < final_score:
            maxi = final_score


    # perform analysis on interested rooms
    for room in room_dict:
        #before = room_dict[room].get_final_weighted_score()
        room_dict[room].normalize_final_weighted_score(mini,maxi)

        # Plot all room analysis
        final_score = room_dict[room].get_final_weighted_score()
        rank = float(room_dict[room].get_score_rank())
        #print(room_dict[room].get_location(),"SCORE:",final_score,"RANK:",rank)
        
        loc   = room_dict[room].get_location()
        rnk  = "rank"
        scr = "score"
        if rank >= good_threshold:
            good_scores[loc][rnk]  = rank
            good_scores[loc][scr] = final_score
        else:
            bad_scores[loc][rnk]  = rank
            bad_scores[loc][scr] = final_score

        i = 0
        
        for day in ["M", "T", "W", "R", "F", "S"]:
            day_data = room_dict[room].get_evals().get_courses_on_date(day)
            day_data = ScheduleEvaluation(day_data)
            #day_data.print_hourly_usage()
            # Only generate if the room actually has any classes that day
            if len(day_data.get_records()) > 1:

                # go to first value and extract the room capacity
                for course,score in day_data.get_records():
                    capacity = course.rec["ROOM_CAPACITY"]
                    break
                day_plot = ScheduleReport(year, semester, day_data, "Course Time", "Percentage of Room Filled")
                ind   = "{0:.2f}".format(room_dict[room].get_daily_weight(day) )
                total = "{0:.2f}".format(final_score)
                day_plot.plot_seat_percentage(room,day,capacity,ind,total,rank,i,class_rooms)
                #room_data.print_records(True,True)
            else:
                continue
            i += 1

    day_plot.generate_report(good_scores,bad_scores,class_rooms,good_threshold)

    print("Evaluation Complete")




