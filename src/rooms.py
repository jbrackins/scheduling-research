class Classrooms:
    """Classrooms that matter...

    The Classroom Class

    Attributes:
        tbd
    """

    def __init__(self, rooms="all"):
        """Classroom list  initialization method.

        """
        self.room_list = self.populate_list(rooms.upper())

    def get_rooms(self):
        return self.room_list

    def populate_list(self, rooms):
        lst = []
        if rooms == "ALL":
            # Every Other Room
            lst.append("MM 205")
            lst.append("MM 304")
            lst.append("MM 306")
            lst.append("MM 310")
            lst.append("MM 313")

            lst.append("MCB 106")
            lst.append("MCB 107")
            lst.append("MCB 110")
            lst.append("MCB 116")
            lst.append("MCB 118")
            lst.append("MCB 205E")
            lst.append("MCB 205W")
            lst.append("MCB 206E")
            lst.append("MCB 206W")
            lst.append("MCB 309")
            lst.append("MCB 327")
            lst.append("MCB 328")
            lst.append("MCB 329")
            lst.append("MCB 330")
            
            lst.append("MCBC 113")
            lst.append("MCBC 3304")
            lst.append("MC 304")
            lst.append("MCBC 3305")
            lst.append("MC 303")
            
            lst.append("MEP 208")
            lst.append("MEP 255")

            lst.append("MMI 220")
            lst.append("MMI 320")
        if rooms == "LARGE" or rooms == "ALL":
            # The big rooms
            lst.append("MCB 204E")
            lst.append("MCB 204W")
            lst.append("MCB 203")
            
            lst.append("MEP 252")
            lst.append("MEP 253")
            lst.append("MEP 254")
            
            lst.append("MCBC 2228")
            
            lst.append("MC 228")
            
            lst.append("MMI 222")
        return lst