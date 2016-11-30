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

from rec import CourseRecord
from evaluation import ScheduleEvaluation
from score import RoomScore

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


    e = ScheduleEvaluation(records)


    print(e.count_records(), "Records")
    e.prune_records()
    print(e.count_records(), "Records after Pruning")

    e.calc_data()
    e.score_records()
    e.print_records()
    e.print_hourly_usage()

    mondays = e.get_courses_on_date("Monday")

    eMondays = ScheduleEvaluation(mondays)
    eMondays.print_records(False,True)
    #e.print_rooms("MCM")

    buildings = e.get_buildings()

    print("--------------------------------------------------------")
    for building in sorted(buildings):
        print("Stats for", building)
        e.print_rooms(building)
        print("--------------------------------------------------------")

    print("Stats for all buildings")
    e.print_buildings()
    print("--------------------------------------------------------")



