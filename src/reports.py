import matplotlib.pyplot as plt
import os
import datetime as dt
import dateutil.parser as dparser
import collections
import matplotlib.dates as md
import dateutil
 

from rec import CourseRecord

class ScheduleReport:
    """Schedule Report class. Output graphs for scheduler...

    The ScheduleReport Class

    Attributes:
        tbd
    """

    def __init__(self, yr, sem, data, x_label, y_label):
        """ScheduleReport  initialization method.

        """

        self.day = {"M": "Monday", "T": "Tuesday", "W": "Wednesday",
                    "R": "Thursday", "F": "Friday", "S": "Saturday"}
        self.path = "../reports/"
        self.year = yr
        self.semester = sem
        self.course_times = self.set_course_times()
        self.x_label = x_label
        self.y_label = y_label
        self.data = data

    def set_course_times(self):
        course_times = []
        for i in range(7, 20):
            for j in range(0,60,60):
                hr = str(i)
                if j < 10:
                    mn = "0" + str(j)
                else:
                    mn = str(j)
                time = dparser.parse(hr+":"+mn)
                time = time.strftime('%H:%M')
                course_times.append(time)
        return course_times

    def get_course_times(self):
        return self.course_times

    def fill_timeline(self,time_line):
        for time in self.course_times:
            time = str(time)
            if time not in time_line:
                time_line[time] = 0
        return time_line

    def build_path(self,yr, sem, location):
        old_dir = os.getcwd()

        if not os.path.exists(self.path):
            os.mkdir(self.path)
        os.chdir(self.path)
        if not os.path.exists(yr):
            os.mkdir(yr)
        os.chdir(yr)
        if not os.path.exists(sem):
            os.mkdir(sem)
        os.chdir(sem)
        if not os.path.exists(location):
            os.mkdir(location)
        os.chdir(old_dir)

    def generate_plot_seat_percentage(self,course_list,day):
        plot_data = {}

        for course, score in course_list:
            time = course.rec["START_TIME"]
            end  = course.rec["END_TIME"]
            percent = score.percentage_score
            if time in plot_data:
                plot_data[time] += percent
            else:
                plot_data[time] = percent
            # if end in plot_data:
            #     plot_data[end] += percent
            # else:
            #     plot_data[end] = percent                
        for key in plot_data:
            plot_data[key] *= 100.00
        # sort the plot by time
        plot_data = self.fill_timeline(plot_data)
        plot_data = collections.OrderedDict(sorted(plot_data.items()))
        #print(plot_data.values())
        return plot_data


    def generate_plot_seat_labels(self,eval_data,location,times):
        labels = []
        for time in times:
            course = eval_data.find_record(location, time)
            if course != None:
                lbl =  course.get_rec("SUBJECT") + " " + str(course.get_rec("COURSE_NUM"))
            else:
                lbl = ""
            labels.append( lbl )
        return labels


    def plot_seat_percentage(self,location,weekday,capacity,counter):
        #print(plot)
        room_title = "Room Usage Statistics for "
        room_title = room_title + location + " on " + self.day[weekday] + "s"
        room_title = room_title + " - " + self.semester + " " + self.year
        plt.figure(figsize=(20,10))

        plt.title(room_title)
        plt.xlabel('Time')
        y_lab = 'Room Utilization (in percent)'
        plt.ylabel(y_lab)
        # Text places anywhere within the Axis

        #print("HELLOOOOOOOO")

        ax=plt.gca()
        self.data.print_records(True,True)
        plot = self.generate_plot_seat_percentage(self.data.get_records(),weekday)
        plt.text(0.6, 90, location + " capacity is " + str(capacity),
        horizontalalignment='right', backgroundcolor='pink')
        ax.grid(zorder=0)
        plt.bar(range(len(plot)), plot.values(), align='center',zorder=3)
        plt.xticks(range(len(plot)), list(plot.keys()))
        plt.axis(ymin = 0, ymax= 120)
        plt.xticks(rotation=70)

        rects = ax.patches
        labels = self.generate_plot_seat_labels(self.data,location,list(plot.keys()))
        print(labels)
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')
        # datestrings = ['2012-02-21 11:28:17.980000', '2012-02-21 12:15:32.453000', '2012-02-21 23:26:23.734000', '2012-02-26 17:42:15.804000']
        # dates = [dateutil.parser.parse(s) for s in datestrings]

        # plt_data = list(plot.values())
        # plt.subplots_adjust(bottom=0.2)
        # plt.xticks( rotation=25 )

        # ax=plt.gca()
        # lst = list(plot.keys())
        
        # ftr = [100,1]
        # for i in range(0,len(lst)):
        #     lst[i] = sum([a*b for a,b in zip(ftr, map(int,lst[i].split(':')))])

        # print(plt_data)
        # print(lst)
        # #xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        # #ax.xaxis.set_major_formatter(xfmt)
        # ax.set_xticks(lst)

        # #xfmt = md.DateFormatter('%H:%M')
        # #ax.xaxis.set_major_formatter(xfmt)
        # plt.plot( lst,plt_data, "o-")

        #plt.show()

        self.build_path(self.year, self.semester, location.replace(" ","_"))
        plt_file =  self.path  + self.year + "/" + self.semester  
        plt_file += "/" + location.replace(" ","_")  + "/" 
        plt_file += str(counter) + "_" + self.day[weekday] + "_" + location.replace(" ", "_") 
        #print(plt_file)
        plt.savefig(plt_file, format='pdf', bbox_inches='tight')
        plt.clf()        
        plt.close() 