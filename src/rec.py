from index import SpreadsheetIndex
from openpyxl import Workbook
from openpyxl import load_workbook

class CourseRecord:
    """Course Records data struct 

    The CourseRecord Class

    Attributes:
        tbd
    """

    def __init__(self):
        """CourseRecord class initialization method.

        

        """
        self.keys                   = []
        self.rec = {}
        self.i   = SpreadsheetIndex()
        self.subject_key            = ["SUBJECT", self.i.subject]
        self.course_number_key      = ["COURSE_NUM", self.i.course_number]
        self.status_key             = ["COURSE_STATUS", self.i.status]
        self.days_of_week_key       = ["DAYS_OF_WEEK", self.i.days_of_week]
        self.start_time_key         = ["START_TIME" , self.i.start_time]
        self.end_time_key           = ["END_TIME", self.i.end_time]
        self.room_capacity_key      = ["ROOM_CAPACITY", self.i.room_capacity]
        self.section_capacity_key   = ["SECTION_CAPACITY", self.i.section_capacity]
        self.building_key           = ["BUILDING", self.i.building]
        self.room_key               = ["ROOM", self.i.room]
        self.course_key             = ["COURSE", self.i.course]
        self.student_count_key      = ["STUDENT_COUNT", self.i.student_count]

        self.init_keys(self.keys)
        self.init_rec(self.rec, self.keys)

    def init_keys(self, keyring):
        keyring.append(self.course_key)             
        keyring.append(self.subject_key)
        keyring.append(self.course_number_key)      
        keyring.append(self.status_key)             
        keyring.append(self.days_of_week_key)       
        keyring.append(self.start_time_key)
        keyring.append(self.end_time_key) 
        keyring.append(self.room_capacity_key)   
        keyring.append(self.section_capacity_key) 
        keyring.append(self.building_key) 
        keyring.append(self.room_key)               
        keyring.append(self.student_count_key)    

    def __repr__(self):
        return self.rec

    def __str__(self):
        msg = ""
        for key, index in self.keys:
            msg = msg + key + ": " + str(self.rec[key]) + "\n"
        return msg

    def init_rec(self, record, keyring): 
        for key, index in keyring:
            record[key] = None

    def set_rec(self, key, value):
        self.rec[key] = value

    def get_rec(self, key):
        return self.rec[key]

    def read_rec(self, worksheet, row):
        """Read all relevant info for a given record
        """
        for key, index in self.keys:
            i = index + str(row)
            self.rec[key] = worksheet[i].value




