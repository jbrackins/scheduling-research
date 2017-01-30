import matplotlib.pyplot as plt
import os
import datetime as dt
import dateutil.parser as dparser
import collections
import matplotlib.dates as md
import dateutil

from rec import CourseRecord

LARGE_ROOM_TIER  = 60
MEDIUM_ROOM_TIER = 40

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

    def get_size_tier(self,size):
        tier = None
        if size > LARGE_ROOM_TIER:
            tier = "L" # Large room
        elif size > MEDIUM_ROOM_TIER:
            tier = "M" # Medium Room
        else:
            tier = "S" # Small Room
        return tier

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

    def fill_timeline(self,time_line,time_label):
        for time in self.course_times:
            time = str(time)
            if time not in time_line:
                time_label[time] = ""
                time_line[time] = 0
        return time_line,time_label

    def build_path(self,yr, sem, location, classrooms):
        old_dir = os.getcwd()

        sem += "_" + classrooms + "_classrooms"
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

    def valid_label(self,label):
        if label == None:
            return 0
        else:
            return int(label)

    def get_label(self,subject,course_num,count,capacity):
        count    = self.valid_label(count)
        capacity = self.valid_label(capacity)
        
        label  = str(subject) + " "
        label += str(course_num) + "\n"
        label += "[[" + str(count) + " / "
        label += str(capacity) + "]]"
        return label

    def update_label(self,old_label,subject,course_num,count,capacity):
        # Get rid of excess characters in string
        #print(old_label)
        old_label = old_label.split("[[")[1].replace("]]","").replace(" ","").split("/")
        #print(old_label[1])
        
        # validate labels to make sure they aren't crap
        old_count    = self.valid_label(old_label[0])
        old_capacity = self.valid_label(old_label[1])
        count    = self.valid_label(count)
        capacity = self.valid_label(capacity)

        count    += old_count
        capacity += old_capacity

        return self.get_label(subject,course_num,count,capacity)


    def generate_plot_seat_percentage(self,course_list,day):
        # Generate plot data, as well as labels, etc

        plot_data  = {}
        plot_label = {}
        for course, score in course_list:
            time     = course.rec["START_TIME"]
            end      = course.rec["END_TIME"]

            subject  = course.rec["SUBJECT"]
            number   = course.rec["COURSE_NUM"]
            count    = course.rec["STUDENT_COUNT"] 
            capacity = course.rec["SECTION_CAPACITY"]
            percent = score.percentage_score
            if time in plot_data:
                plot_data[time] += percent
                # update label
                plot_label[time] = self.update_label(plot_label[time],subject,number,count,capacity)
            else:
                plot_data[time] = percent
                #plot_data[time] += percent
                # new label
                plot_label[time] = self.get_label(subject,number,count,capacity)
            # if end in plot_data:
            #     plot_data[end] += percent
            # else:
            #     plot_data[end] = percent                
        for key in plot_data:
            plot_data[key] *= 100.00
            if plot_data[key] > 110.00:
                plot_data[key] = 110.00
        # sort the plot by time
        plot_data,plot_label = self.fill_timeline(plot_data,plot_label)
        plot_data = collections.OrderedDict(sorted(plot_data.items()))
        plot_label = collections.OrderedDict(sorted(plot_label.items()))
        #print(list(plot_label.values()))
        #print(plot_data.values())
        return plot_data, list(plot_label.values())


    def generate_plot_seat_labels(self,eval_data,location,times):
        labels = []
        for time in times:
            course = eval_data.find_course(location, time)
            if course != None:
                lbl  =  course.get_rec("SUBJECT") + " " 
                lbl += str(course.get_rec("COURSE_NUM")) + "\n"
                lbl += "(" + str(course.get_rec("STUDENT_COUNT")) + " / " 
                lbl += str(course.get_rec("SECTION_CAPACITY")) + ")"
            else:
                # Pass a blank label so we have a correct total
                lbl = ""
            labels.append( lbl )
        return labels


    def plot_seat_percentage(self,location,weekday,capacity,score_ind, score_tot,rank,counter,classrooms):

        # Plot Title
        room_title = "Room Usage Statistics for "
        room_title += location + " on " + self.day[weekday] + "s"
        room_title += " - " + self.semester + " " + self.year
        plt.figure(figsize=(20,10))

        # Set up title and axes
        plt.title(room_title)
        plt.xlabel('Course Time')
        y_lab = 'Room Utilization (in percent)'
        plt.ylabel(y_lab)

        # Prepare plot data
        ax=plt.gca()
        plot, labels = self.generate_plot_seat_percentage(self.data.get_records(),weekday)
        
        # Prepare message displayed in plot
        message  = location + " student capacity is " + str(capacity) + " (" + self.get_size_tier(capacity) + " Room)\n"
        message += self.day[weekday]  + " weighted score for " + location + " is " + str(score_ind) + "\n"
        message += "Total weighted score for " + location + " is " + str(score_tot) + "\n"
        message += location + "'s Rank is " + str(rank) + " / 10.00"
        plt.text(3, 130, message ,
        horizontalalignment='right', backgroundcolor='pink')
        
        # Set up the bar graph
        ax.grid(zorder=0)
        plt.bar(range(len(plot)), plot.values(), align='center',zorder=3)
        plt.xticks(range(len(plot)), list(plot.keys()))
        plt.axis(ymin = 0, ymax= 150)
        plt.xticks(rotation=70)

        # Set labels on each bar
        rects = ax.patches
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

        # Write plot to file
        self.build_path(self.year, self.semester, location.replace(" ","_"), classrooms)
        plt_file =  self.path  + self.year + "/" + self.semester + "_" + classrooms + "_classrooms"
        plt_file += "/" + location.replace(" ","_")  + "/" 
        plt_file += str(counter) + "_" + self.day[weekday] + "_" + location.replace(" ", "_") 
        #print(plt_file)
        plt.savefig(plt_file, format='pdf', bbox_inches='tight')
        plt.clf()        
        plt.close() 

    def generate_report(self,good,bad,classrooms,middle):
        report_file = self.path  + self.year + "/" + self.semester + "_" + classrooms + "_classrooms"
        report_file += "/" + "report.txt"

        file = open(report_file, 'w')

        good_list = sorted(list(good.keys()), key=lambda x: (good[x]['rank'], good[x]['score']))
        good_list.reverse()

        bad_list = sorted(list(bad.keys()), key=lambda x: (bad[x]['rank'], bad[x]['score']))
        bad_list.reverse()

        msg = "\n---SCHEDULE EVALUATION REPORT:-------------------------\n"
        if classrooms == "large":
            msg += "Evaluation of all large rooms on campus\n"
        elif classrooms == "all":
            msg += "Evaluation of all interest rooms on campus\n"
        msg += "Rooms with a ranking >= " + str(middle) + ":\n"
        for room in good_list:
            msg += "{:12s}".format(room) + " " + "SCORE: "
            msg += "{0:.2f}".format(good[room]["score"]) + "    " + "RANK: "
            msg += "{0:.2f}".format(good[room]["rank"] ) + "\n"
        msg += "\n-------------------------------------------------------\n\n"
        msg += "Rooms with a ranking < " + str(middle) + ":\n"
        for room in bad_list:
            msg += "{:12s}".format(room) + " " + "SCORE: "
            msg += "{0:.2f}".format(bad[room]["score"]) + "    " + "RANK: "
            msg += "{0:.2f}".format(bad[room]["rank"] ) + "\n"
        msg += "\n-------------------------------------------------------\n\n"

        best  = good_list[0]
        worst = bad_list[-1]
        msg += "Best  Room Based on Ranking: " + best  + "\n"
        msg += "Worst Room Based on Ranking: " + worst + "\n"
        
        # write the message to the file and close it. You're done!
        file.write(msg)
        file.close()




