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

        self.percentage_score     = 0    # 0% - 100% room usage
        self.room_size_tier            = 'S'  # S / M / L
        self.section_size_tier            = 'S'  # S / M / L
        self.hourly_score         = 0    # how many hours room is used

        self.calculated           = False
        self.weighted_score       = 0    # weighted final score

    def __str__(self):
        msg = ""
        msg = msg + "Room Size    Tier: " + str(self.room_size_tier) + "\n"
        msg = msg + "Section Size Tier: " + str(self.section_size_tier) + "\n"

        msg = msg + "% Usage     Score: " + str(self.percentage_score) + "\n"
        msg = msg + "Hourly      Score: " + str(self.hourly_score) + "\n"
        msg = msg + "Weighted    Score: " + str(self.weighted_score) + "\n"
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

    def get_section_size_tier(self,course):
        size = course.rec["SECTION_CAPACITY"]
        if size > LARGE_ROOM_TIER:
            self.section_size_tier = "L" # Large student count
        elif size > MEDIUM_ROOM_TIER:
            self.section_size_tier = "M" # Medium student count
        else:
            self.section_size_tier = "S" # Small student count

    def get_percentage_score(self,course):
        """Percent utilization of room
        """
        student_count = course.rec["STUDENT_COUNT"]
        room_capacity = course.rec["ROOM_CAPACITY"]

        if room_capacity > 0:
            percentage = float(student_count) / float(room_capacity)
            percentage = percentage * 100
        else:
            percentage = 0

        
        if percentage < 0:
            percentage = 0

        self.percentage_score = percentage

    def get_hourly_score(self,course,hourly_counts):
        course_days = course.rec["DAYS_OF_WEEK"]
        time        = course.rec["START_TIME"]
        for day in ["M", "T", "W", "R", "F", "S"]:
            if day in course_days:
                self.hourly_score = hourly_counts[day][time]


    def get_weighted_score(self):
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
        return self.weighted_score


    
