from rec import CourseRecord
from score import RoomScore
from evaluation import ScheduleEvaluation
class LocationScore:


	def __init__(self, evals=None):

		self.evals   = evals
		self.courses = None
		self.location  = None

		self.final_weighted = 0
		if evals != None:
			self.courses = self.evals.get_records()
			self.location    = self.find_location()
			self.final_weighted = self.calculate_final_weighted_score()

	def calculate_final_weighted_score(self):
		score_sum   = 0.00
		score_total = 0.00

		for course, score in self.courses:
			score_sum   += score.get_weighted_score(course)
			score_total += 1.00
		return str(score_sum / score_total) + ", " + str(score_total) + " Records..."

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

	def get_evals(self):
		return self.evals
