from rec import CourseRecord
import datetime as dt
import dateutil.parser as dparser
import collections

class ScheduleEvaluation:
    """Schedule Evaluation methods

    The ScheduleEvaluation Class

    Attributes:
        tbd
    """

    def __init__(self, rec_list):
        """ScheduleEvaluation class initialization method.

        

        """
        self.records    = rec_list
        self.rooms      = {}  
        self.buildings  = {}
        self.hourly_counts = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}
        self.hourly_counts = collections.OrderedDict(self.hourly_counts)

        self.hourly_total = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}

        self.hourly_min   = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}
        self.hourly_min = collections.OrderedDict(self.hourly_min)

        self.hourly_max   = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}
        self.hourly_max = collections.OrderedDict(self.hourly_max)

        self.set_min_max()
        self.room_total   = 0

    def set_min_max(self):
        for day in ["M", "T", "W", "R", "F", "S"]:
            self.hourly_total    =  0
            self.hourly_min[day] =  10000
            self.hourly_max[day] = -10000

    def valid(self, course):
        """Validate course to determine if we care about it.

            We do not care about courses in this criteria:
            1) courses that do not meet at a specific time
            2) courses not labeled "active"
            3) courses that do not meet in a specific room
            4) <More Criteria can be added by checking record keys>

        """

        if course.rec["START_TIME"] == None:
            return False
        elif course.rec["COURSE_STATUS"] == "C":
            return False
        elif course.rec["ROOM"] == None:
            return False
        elif course.rec["ROOM_CAPACITY"] == None:
            return False

        # If all above record values check out, it's a valid rec
        return True

    def in_location(self,course,location):
        """Validate course to determine if we care about it.

            We care about courses in this criteria:
            1) In a specific room
        """
        course_location = self.get_course_location(course)
        if course_location == location:
            return True
        return False

    def in_location_list(self,course,loc_list):
        """Validate course to determine if we care about it.

            We care about courses in this criteria:
            1) In a specific room
        """
        course_location = self.get_course_location(course)
        if course_location in loc_list:
            return True
        return False

    def in_room_size(self,course,score,size):
        """Validate course to determine if we care about it.

            We care about courses in this criteria:
            1) In a specific room size tier (S,M,L)
        """
        course_size = score.get_room_size_tier(course)
        if course_size == size:
            return True
        return False

    def on_date(self,course,date):
        """Validate course to determine if we care about it.

            We care about courses in this criteria:
            1) On a specific date
        """

        # Fix date just in case
        date = date.upper()
        if date == "MONDAY":
            date = "M"
        elif date == "TUESDAY":
            date == "T"        
        elif date == "WEDNESDAY":
            date == "W"        
        elif date == "THURSDAY":
            date == "R"        
        elif date == "FRIDAY":
            date == "F"        
        elif date == "SATURDAY":
            date == "S"

        course_dates = course.rec["DAYS_OF_WEEK"]
        if date in course_dates:
            return True
        return False

    def get_course_location(self,course):
        return str( course.rec["BUILDING"] ) + " " + str( course.rec["ROOM"] )

    def find_course(self, location, time):
        for course,score in self.records:
            loc = self.get_course_location(course)
            hr  = course.rec["START_TIME"]
            if location == loc and time == hr:
                return course
        return None

    def calc_data(self):
        """Perform evaluation calcs
        """
        for course, score in self.records:

            #clean days of the week - M T W R F S represent days of week now
            course.rec["DAYS_OF_WEEK"] = course.rec["DAYS_OF_WEEK"].replace("Th", "R")

            # clean time stamps. Use miitary time so we don't fuss with AM / PM
            course.rec["START_TIME"]   = self.get_military_time(course.rec["START_TIME"])
            course.rec["END_TIME"]     = self.get_military_time(course.rec["END_TIME"])

            # Tally Room Usage
            location = self.get_course_location(course)
            self.count_rooms(location)

            # Tally Hourly Usage
            self.count_hourly_usage(course)
        self.get_buildings()
        self.count_buildings()

    def count_hourly_usage(self, course):
        course_days = course.rec["DAYS_OF_WEEK"]
        start_time  = course.rec["START_TIME"]


        for day in ["M", "T", "W", "R", "F", "S"]:
            if day in course_days:
                # Course occurs on given day, add it's course time to our record
                if start_time in self.hourly_counts[day]:
                    self.hourly_counts[day][start_time] += 1
                else:
                    self.hourly_counts[day][start_time] = 1
                #self.hourly_total[day] += 1
                value = self.hourly_counts[day][start_time]

                # update min and max for this day if need be
                self.hourly_min[day], self.hourly_max[day] = self.check_min_max(self.hourly_min[day], self.hourly_max[day],value)
                
    def count_rooms(self, location):
        """Build Room Dictionary
        """

        # Make a tally of how many times a given room is used.
        if location in self.rooms:
            self.rooms[location] = self.rooms[location] + 1
        else:
            self.rooms[location] = 1
        self.room_total = self.room_total + 1

    def count_buildings(self):

        # Get all of the locations first
        for location in sorted(self.rooms):

            location_building = location.split(" ")[0]
            if location_building not in self.buildings:
                self.buildings[location_building] = 0

        specific_total = {}

        # Count how many courses happen in a given building.
        for specific_building in self.buildings:
            specific_total[specific_building] = 0

            for location in sorted(self.rooms):
                location_building = location.split(" ")[0]
                if specific_building == location_building:
                    count = self.rooms[location]
                    specific_total[specific_building] = specific_total[specific_building] + count
            self.buildings[specific_building] = specific_total[specific_building]

    def get_buildings(self):
        return self.buildings

    def print_buildings(self):
        total = 0
        for building in self.buildings:
            print(building, ":", str(self.buildings[building]))
            total = total + self.buildings[building]
        print(total, "Courses Total, just calculated")
        print(self.room_total, "Courses Total, class variable")
        if total == self.room_total:
            print("Totals match, math checks out")
        else:
            print("Totals do NOT match...")

    def print_hourly_usage(self):
        for day in ["M", "T", "W", "R", "F", "S"]:
            print(day,":")
            for time in sorted(self.hourly_counts[day]):
                print("\t",time, ":", self.hourly_counts[day][time], "courses")


    def print_rooms(self,specific_building=None):
        specific_total = 0
        for location in sorted(self.rooms):
            if specific_building == None:
                print(location, ":", str(self.rooms[location]) )
            else:
                location_building = location.split(" ")[0]
                if specific_building == location_building:
                    print(location, ":", str(self.rooms[location]) )
                    specific_total = specific_total + self.rooms[location]
        print(self.room_total, "Courses Total")
        if specific_building != None:
            percent = str(( specific_total / self.room_total ) * 100 ) + "%"
            print(specific_total, "Courses Total for", specific_building, "(", percent ,")")

    def print_records(self, print_course=True,print_score=True):
        for course,score in self.records:
            if print_course:
                print(course)
            if print_score:
                print(score)

    def prune_records(self):
        self.records = [ [course, score] for course, score in self.records if self.valid(course)]

    def get_courses_in_location(self, location):
        return [ [course, score] for course, score in self.records if self.in_location(course, location)]
 
    def get_courses_in_location_list(self, loc_list):
        return [ [course, score] for course, score in self.records if self.in_location_list(course, loc_list)]

    def get_courses_on_date(self, date):
        return [ [course, score] for course, score in self.records if self.on_date(course, date)]

    def get_courses_in_room_size(self, size):
        size = size.upper()
        if size == "LARGE":
            size = "L"
        elif size == "MEDIUM":
            size = "M"
        elif size == "SMALL":
            size = "S"
        return [ [course, score] for course, score in self.records if self.in_room_size(course, score, size)]

    def count_records(self):
        return len(self.records)

    def get_records(self):
        return self.records

    def score_records(self):
        for rec,score in self.records:
            score.get_room_stats(rec)
            score.get_room_size_tier(rec)
            score.get_section_size_tier(rec)
            score.get_student_count_tier(rec)

            score.get_percentage_score(rec)
            #score.get_hourly_score(rec,self.hourly_counts,self.hourly_total, self.hourly_min, self.hourly_max)
            score.get_size_tier_score(rec)
            score.get_weighted_score(rec)

    def check_min_max(self,current_min,current_max,value):

        #check min
        if current_min > value:
            current_min = value
        #check max
        if current_max < value:
            current_max = value

        return current_min, current_max

    def find_min_max(self,course_list):
        # get first value to set as minimum
        for course in course_list:
            #minimum = course.
            break

        for course in course_list:
            break

        return minimum, maximum
    def get_military_time(self,time):
        """get correct time format
        """
        if time:
            time = time[::-1].replace(":", ""[::-1], 1)[::-1]
            date=dparser.parse(time)
            return date.strftime('%H:%M')
        else:
            return None