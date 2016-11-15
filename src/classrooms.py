import datetime as dt
import dateutil.parser as dparser

code = {}

# dict containing all the classrooms by code
code["MPL"]  = "Paleontology Laboratories"
code["RCUC"] =  "Rapid City University Center"
code["MMC"]  = "Music Center"
code["MKC"] = "King Center"
code["MC"] = "Chem-Chem Engr Building"
code["MIER"] = "Industrial Engineering Researc"
code["MEP"] = "Electrical Engr-Physics"
code["MMI"] = "Mineral Industries Buildi"
code["MCB"] = "Classroom Building"
code["COFC"] = "Off Campus"
code["MOG"] = "Music Center"
code["MCBC"] = "Chemical-Bio-Chemistry"
code["MCM"] = "Civil-Mechanical-Engr-Bldg"
code["MM"] = "Mc Laury Building"
code["MNG"] = "Physical Education Center"
code["MC1"] = "CBEC"
#code["MC1"] = "CBEC"

# add more here.

#main_rooms = {k: code[k] for k in ('l', 'm', 'n')}
main_rooms = {r: code[r] for r in ('MM', 'MCB', 'MCBC', 'MC', 'MEP', 'MMI')}

#big_rooms = {k: code[k] for k in ('MEP', 'MCB', 'COFC')}

day = {"M" : "Monday", "T" : "Tuesday", "W" : "Wednesday", "R" : "Thursday", "F" : "Friday", "S" : "Saturday"}

course_times = []
for i in range(7, 20):
	time = dparser.parse(str(i)+":00")
	time = time.strftime('%H:%M')
	course_times.append(time)


