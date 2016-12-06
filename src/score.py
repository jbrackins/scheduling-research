from rec import CourseRecord

#MODIFIABLE ATTRIBUTES: TWEAK THESE TO GET DIFFERENT RESULTS

# ROOM TIERS: MAKE SURE LARGE_ROOM_TIER IS GREATER THAN MEDIUM_ROOM_TIER
LARGE_ROOM_TIER  = 60
MEDIUM_ROOM_TIER = 40


class RoomScore:
    """RoomScore, calculation tasks and weight determination for room evaluation

    The RoomScore Class

    Attributes:
        tbd
    """

    def __init__(self):
        """RoomScore class initialization method.

        

        """
        
        #things to evaluate based on:

        # percentage of room filled
        
        # room size tier (s,m,l)
        # l = 60 or more
        # m = 30 - 60
        # s = 30 or less
        
        # number of hours room is used
        # with additional weight given to important times

        self.percentage_score      = 0    # 0% - 100% room usage
        self.room_size_tier        = 'S'  # S / M / L
        self.section_size_tier     = 'S'  # S / M / L
        self.hourly_score          = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}   # how many hours room is used
        self.size_tier_score       = 0    # does the room size make sense
        self.calculated            = False
        self.weighted_score        = 0    # weighted final score

    def __str__(self):
        msg = ""
        msg = msg + "Room Size    Tier: " + str(self.room_size_tier)     + "\n"
        msg = msg + "Section Size Tier: " + str(self.section_size_tier)  + "\n"

        msg = msg + "% Usage     Score: " + str(self.percentage_score)   + "\n"
        msg = msg + "Hourly      Score: " + str(self.hourly_score)       + "\n"
        msg = msg + "Size Tier   Score: " + str(self.size_tier_score)    + "\n"

        msg = msg + "Weighted    Score: " + str(self.weighted_score)     + "\n"
        return msg

    def foo(self):
        print("")

    def get_room_size_tier(self,course):
        size = course.rec["ROOM_CAPACITY"]
        if size > 60:
            self.room_size_tier = "L" # Large room
        elif size > 40:
            self.room_size_tier = "M" # Medium Room
        else:
            self.room_size_tier = "S" # Small Room
        return self.room_size_tier

    def get_section_size_tier(self,course):
        size = course.rec["SECTION_CAPACITY"]
        if size == None:
            size = course.rec["STUDENT_COUNT"]
        if size > LARGE_ROOM_TIER:
            self.section_size_tier = "L" # Large student count
        elif size > MEDIUM_ROOM_TIER:
            self.section_size_tier = "M" # Medium student count
        else:
            self.section_size_tier = "S" # Small student count

    def get_size_tier_score(self,course):
        self.size_tier_score = self.check_size_tier(course)

    def get_percentage_score(self,course):
        """Percent utilization of room
        """
        student_count = course.rec["STUDENT_COUNT"]
        room_capacity = course.rec["ROOM_CAPACITY"]

        if room_capacity > 0:
            percentage = float(student_count) / float(room_capacity)
            percentage = percentage
        else:
            percentage = 0

        
        if percentage < 0:
            percentage = 0

        self.percentage_score = percentage

    def normalize(self,minimum,maximum,value):
        value -= minimum
        value /= ( maximum - minimum )
        return value

    def get_hourly_score(self,course,hourly_counts,hourly_total,minimum,maximum):
        course_days = course.rec["DAYS_OF_WEEK"]
        time        = course.rec["START_TIME"]
        score = 0
        for day in ["M", "T", "W", "R", "F", "S"]:
            if day in course_days:
                score = hourly_counts[day][time]
                printval = score
                #normalize the hourly score
                score = self.normalize(minimum[day],maximum[day],score)
                #self.hourly_score = str(score) + " " + str(printval)
                self.hourly_score[day] = score


    def get_weighted_score(self, course=None):
        """ Some logic for weighing the scores:

            Classes with BOTH section size tier and room size tier "L" get high scores.
                Reasoning:
                    These courses HAVE to be in the large rooms, no matter what.

            Classes with section size tier "S" or "M" in room size tier "L" rooms get bad scores.
                Reasoning:
                    These courses don't have to be in large rooms. The higher the 
                    hourly score for this course, the worse their weighed score is.
                    This is because, since this is a busy time, other courses 
                    should be considered for this classroom. 

                    The hourly score will influence how bad their score is, because 
                    if this happens to be a course time where there aren't a whole lot 
                    of classes going on, being in too large of a room isn't that big of a deal.
        """
        if not self.calculated:
            score = 1.00                 # 100 is perfect
            hourly = score
            section_size = self.section_size_tier
            room_size    = self.room_size_tier
            tier_max     = 1.00
            course_days = course.rec["DAYS_OF_WEEK"]
            # adjust worth of percentage
            percentage = self.percentage_score
            if room_size == "L" and section_size == "L":
                # percentage of room filled shouldn't be factored in, a large room HAS to be used.
                percentage += (tier_max-percentage) * 0.99 # 99% Boost
            elif percentage > 100 and self.tier_to_value(section_size) > self.tier_to_value(room_size):
                # room should be penalized for being too small
                percentage -= (tier_max-percentage) * 0.20 # 20% Reduction
            elif room_size == section_size:
                # If room size and section size are identical (not Large), then bump up percentage a bit
                percentage += (tier_max-percentage) * 0.75 # 80% Boost
            else:
                # Bump up the percentage regardless, since room percentage can be way lower than other stats
                percentage += (tier_max-percentage) * 0.50 # 50% Boost

            # compile the hourly scores
            for day in ["M", "T", "W", "R", "F", "S"]:
                if day in course_days:
                    hourly *= self.hourly_score[day]
            score = self.size_tier_score * 1 * percentage
            self.weighted_score = score
            self.calculated = True
        return self.weighted_score

    def check_size_tier(self,course):
        """ Check to see if the size of the 

        """
        LARGE  = 3
        MEDIUM = 2
        SMALL  = 1

        section = self.tier_to_value(self.section_size_tier)
        room    = self.tier_to_value(self.room_size_tier)

        # If room and section are identical tiers, perfect score
        score = 1.00
        if  room < section:
            # Room is too small
            for i in range(room,section):
                score = score * ( i / pow( section,1.5) )
        else:
            # Room is too large
            for i in range(section,room):
                score = score * ( i / pow(room,1) )
        return score


    def tier_to_value(self,tier):
        """ Convert

        """
        value = 0
        if tier == "S":
            value = 1
        elif tier == "M":
            value = 2
        elif tier == "L":
            value = 3
        return value

    
