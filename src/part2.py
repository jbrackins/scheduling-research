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
        for i in range(2, len(ws.rows)):
            s = RoomScore()
            r = CourseRecord()
            r.read_rec(ws,i)
            records.append([r,s])
        semester, year = get_semester(filename)

    e = ScheduleEvaluation(records)


    print(e.count_records(), "Records")
    e.prune_records()
    print(e.count_records(), "Records after Pruning")

    e.calc_data()
    e.score_records()
    #e.print_records()
    #e.print_hourly_usage()

    #mondays = e.get_courses_on_date("Monday")

    #eMondays = ScheduleEvaluation(mondays)
    #eMondays.print_records(True,True)
    #e.print_rooms("MCM")

    #buildings = e.get_buildings()

    l = Classrooms("large")
    print("Big ol rooms")
    large = e.get_courses_in_location_list(l.get_rooms())
    large = ScheduleEvaluation(large)
    #large.print_records(True,True)

    i = 0

    room_dict = {}

    # # UGH do this the other way around........
    # for day in ["M", "T", "W", "R", "F", "S"]:
    #     day_data = large.get_courses_on_date(day)
    #     day_data = ScheduleEvaluation(day_data)
    #     #day_data.print_records(True,True)

    #     for room in l.get_rooms():
    #         room_data       = day_data.get_courses_in_location(room)
    #         room_data       = ScheduleEvaluation(room_data)
    #         room_dict[room] = LocationScore(room_data)

    #         print("ROOOM",room)
    #         if len(room_dict[room].get_evals().get_records()) > 1:

    #             # go to first value and extract the room capacity
    #             for course,score in room_data.get_records():
    #                 capacity = course.rec["ROOM_CAPACITY"]
    #                 break
    #             day_plot = ScheduleReport(year, semester, room_dict[room].get_evals(), "Course Time", "Percentage of Room Filled")
    #             day_plot.plot_seat_percentage(room,day,capacity,i)
    #             #room_data.print_records(True,True)
    #             print("DONE=====================")
    #         else:
    #             print("OOPS")
    #     i += 1


    # For every room, generate a plot for each day
    #   (two for loops)

    for room in l.get_rooms():
        room_data       = large.get_courses_in_location(room)

        # Only generate if this room was actually used at all this semester.
        if len(room_data) > 1:
            room_data       = ScheduleEvaluation(room_data)
            room_dict[room] = LocationScore(room_data)

            print("Score for ", room_dict[room].get_location(), room_dict[room].get_final_weighted_score())
            i = 0
            for day in ["M", "T", "W", "R", "F", "S"]:
                day_data = room_dict[room].get_evals().get_courses_on_date(day)
                day_data = ScheduleEvaluation(day_data)

                # Only generate if the room actually has any classes that day
                if len(day_data.get_records()) > 1:

                    # go to first value and extract the room capacity
                    for course,score in day_data.get_records():
                        capacity = course.rec["ROOM_CAPACITY"]
                        break
                    day_plot = ScheduleReport(year, semester, day_data, "Course Time", "Percentage of Room Filled")
                    day_plot.plot_seat_percentage(room,day,capacity,i)
                    #room_data.print_records(True,True)
                else:
                    continue
                i += 1

    #percent_plots
    # print("--------------------------------------------------------")
    # for building in sorted(buildings):
    #     print("Stats for", building)
    #     e.print_rooms(building)
    #     print("--------------------------------------------------------")

    # print("Stats for all buildings")
    # e.print_buildings()
    # print("--------------------------------------------------------")


    # print("min", e.hourly_min, "max", e.hourly_max)

