from score import RoomScore

if __name__ == "__main__":

	a = RoomScore()

	print("Perfect Scores:")
	print("-------------------------------------------")
	a.room_size_tier    = "L"
	a.section_size_tier = "L"
	print("Test A Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))
	
	print("-------------------------------------------")
	a.room_size_tier    = "M"
	a.section_size_tier = "M"
	print("Test D Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))
	
	print("-------------------------------------------")
	a.room_size_tier    = "S"
	a.section_size_tier = "S"
	print("Test G Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))
	
	print("\n\n")

	print("Room Too Large:")
	print("-------------------------------------------")
	a.room_size_tier    = "L"
	a.section_size_tier = "M"
	print("Test B Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))

	print("-------------------------------------------")
	a.room_size_tier    = "M"
	a.section_size_tier = "S"
	print("Test F Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))

	print("-------------------------------------------")
	a.room_size_tier    = "L"
	a.section_size_tier = "S"
	print("Test C Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))


		


	print("\n\n")

	print("Section Too Large:")
	print("-------------------------------------------")
	a.room_size_tier    = "S"
	a.section_size_tier = "M"
	print("Test I Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))

	print("-------------------------------------------")
	a.room_size_tier    = "M"
	a.section_size_tier = "L"
	print("Test E Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))

	print("-------------------------------------------")
	a.room_size_tier    = "S"
	a.section_size_tier = "L"
	print("Test H Score for Room:", a.room_size_tier,"Section:", a.section_size_tier, ": ", a.check_size_tier(a))
	

	
