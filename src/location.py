from rec import CourseRecord
from score import RoomScore
from evaluation import ScheduleEvaluation

FULL_HOURS    = 8 # 8:00AM - 4:00PM utilization
PARTIAL_HOURS = FULL_HOURS * 0.75 #75%
HALF_HOURS    = FULL_HOURS * 0.50 #50%
SPARSE_HOURS  = FULL_HOURS * 0.25 #25%

class LocationScore:


    def __init__(self, evals=None):

        self.evals   = evals
        self.courses = None
        self.location  = None

        self.daily_weights  = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}
        self.daily_totals   = {"M": {}, "T": {}, "W": {}, "R": {}, "F": {} ,"S": {}}
        self.final_weighted = 0
        self.weight_rank    = 0 # 0 = worst, 1 = best
        if evals != None:
            self.courses = self.evals.get_records()
            self.location    = self.find_location()
            self.final_weighted = self.calculate_final_weighted_score()

    def reset_daily_weights(self):
        for day in ["M", "T", "W", "R", "F", "S"]:
            self.daily_weights[day] = 0
            self.daily_totals[day]  = 0

    def get_daily_weight(self,day_of_week):
        return self.daily_weights[day_of_week]

    def normalize_final_weighted_score(self,minimum,maximum):
        value = self.final_weighted
        value -= minimum
        if maximum - minimum > 0:
            value /= ( maximum - minimum )
        else:
            value = 0
        self.weight_rank = "{0:.2f}".format(value * 10)

    def calculate_final_weighted_score(self):
        score_sum   = 0.00
        score_total = 0.00

        #reset daily stuff
        self.reset_daily_weights()

        for course, score in self.courses:
            days = course.rec["DAYS_OF_WEEK"]
            #score_sum   += score.get_weighted_score(course)
            score_total += 1.00
            for day in ["M", "T", "W", "R", "F", "S"]:
                if day in days:
                    self.daily_weights[day] += score.get_weighted_score(course)
                    self.daily_totals[day]  += 1

        for day in ["M", "T", "W", "R", "F", "S"]:
            if self.daily_totals[day] > 0:
                self.daily_weights[day] /= self.daily_totals[day]
                self.daily_weights[day] = self.adjust_utilization(self.daily_weights[day],self.daily_totals[day])
                score_sum += self.daily_weights[day]
            else:
                self.daily_weights[day] = 0
        return score_sum / score_total

    def adjust_utilization(self,weights,totals):
        max_score = 1.00
        if totals >= FULL_HOURS: # 8 Hours or more, give slight boost to score
            weights *= 1.15 # 15% Boost
        elif totals >= PARTIAL_HOURS:   # Small Penalty
            weights *= (PARTIAL_HOURS/FULL_HOURS) 
        elif totals >= HALF_HOURS:      # Medium Penalty
            weights *= (HALF_HOURS/FULL_HOURS) 
        elif totals >  SPARSE_HOURS:    # Large Penalty
            weights *= (SPARSE_HOURS/FULL_HOURS) 
        else:                           # Very Large Penalty
            weights *= (1.00/FULL_HOURS)
        return weights

    def get_location(self):
        return self.location

    def find_location(self):
        for course, score in self.courses:
            location = str( course.rec["BUILDING"] )+ " " + str( course.rec["ROOM"] )
            # just need to find the first one, so break after this happens
            break   
        return location

    def get_final_weighted_score(self):
        return self.final_weighted

    def get_score_rank(self):
        return self.weight_rank

    def get_evals(self):
        return self.evals
