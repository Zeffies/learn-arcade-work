class Room:
    """
    A room has a name, a description, and one to 10 exits.
    """

    def __init__(self, name, description='', north=0, west=0, east=0, south=0, northwest=0, southwest=0, northeast=0,
                 southeast=0, up=0, down=0):
        self.name = name
        self.description = description
        self.north = north
        self.west = west
        self.east = east
        self.south = south
        self.northwest = northwest
        self.southwest = southwest
        self.northeast = northeast
        self.southeast = southeast
        self.up = up
        self.down = down


def main():
    # initiate variables and lists
    room_list = []
    current_room = 0
    done = False
    # set up all of the rooms
    room = Room('central chamber',
                '\tYou are in the central chamber. It is a circular room that has walls lined with doors.\nIt is lit '
                'with a mana-stone powered ornate chandelier that gives off a mystical blue glow. \n\tThe room gives '
                'off an ostentatious vibe, as every door is more regal than the last. \nLooking at them makes you dizzy'
                ' thinking of how much this room alone would cost to have built. '
                '\n\nThere are rooms in all 8 directions.',
                north=3, northeast=2, northwest=1, west=4, southeast=9, southwest=5, south=8, east=11, up=None,
                down=None)
    room_list.append(room)
    room = Room('northwest balcony',
                'This is the northwest balcony. There are some comfortable looking rocking '
                'chairs next to a table. The table has a pitcher that refills itself magically \n'
                'with a refreshing drink. In the distance there is a forest that goes on for as \n'
                'far as the eye can see. A bird rests on the balcony railing.'
                '\nThere is a door to your southeast.',
                southeast=0, northeast=None, northwest=None, north=None, southwest=None, south=None, west=None,
                east=None, up=None, down=None)
    room_list.append(room)
    room = Room('northeast balcony',
                '\tThis is the northeast balcony. There is a bizarre, small domesticated animal sitting in the far \n'
                'corner of the balcony. Its form seems to shift, never quite allowing you to figure out what it is. \n'
                'The only thing you know is, it is impossibly cute and has more than two ears.\n'
                '\tIn the distance you can see the eastern edge of a forest, which rests atop a steep cliff that \n'
                'leads to a large body of water. The water shimmers with the brilliance of a perfect emerald, \n'
                'and is coloured as such.\n'
                '\nThere is a door to your southwest.',
                southwest=0, southeast=None, northeast=None, northwest=None, north=None, south=None, west=None,
                east=None, up=None, down=None
                )
    room_list.append(room)
    room = Room('throne room',
                "\tYou've entered the throne room. Opposite the door, at the end of the room is a staircase in the \n"
                "shape of a hill upon which rests a large wooden chair, embroidered with a glossy thread.\nIn the "
                "upper corners of the chair's back rests two gemstones, each glowing softly. \nYou get the feeling that"
                " sitting in the chair without having the proper credentials would be a poor decision.\n\tIn front of "
                "the "
                " throne lays a carpet runner that leads from the throne to the door you're standing infront of. \nOn "
                "each side of the room, past the carpet, rest several benches--pews, really.\n\tThe left and right "
                "walls "
                "have large stained glass windows,\nand the back wall has a normal circular window that is surrounded "
                "by runes in a language you recognize to be magic script. \nYou feel a stagnant air, and smell "
                "something metallic.\n"
                "\nThere is a door to your south.",
                south=0, southeast=None, northeast=None, northwest=None, north=None, southwest=None, west=None,
                east=None, up=None, down=None)
    room_list.append(room)
    room = Room('kitchen',
                "\tYou've entered the kitchen. You're immediately hit with a delightful aroma that you can't quite put "
                "your finger on. \nStrewn across the room are various workstations covered in appliances and tools "
                "required for cooking. \n\tIn one corner of the room, there is a large set of stoves. One of the "
                "burners has a large pot that has steam coming out of it. \n\tThe room is lit very brightly by "
                "skylights lined with glow-stones.\n"
                "\nThere is a door to the east.",
                east=0, southeast=None, northeast=None, northwest=None, north=None, southwest=None, south=None,
                west=None, up=None, down=None)
    room_list.append(room)
    room = Room('bedroom',
                "\tYou've entered a bedroom. The room has a carpet that looks like you'd sink into completely if "
                "you'd let it. \nThe room smells of fresh fruit, and looking at the nightstand you can see why; a "
                "bowl of ripe, cut fruit rests atop it. \n\tNext to the nightstand is a large bed, nearly twice the "
                "size of a normal king-sized bed that has a canopy above it.\nThe bed's sheets are blue, "
                "and its frame is golden with purple gems littered throughout.\nThe bed has a magic shield around it "
                "that shimmers. You recall seeing such a shield before in a high-ranking military officer's "
                "room--\ntouching it without having proper permission would be a shock to be sure.\n\tYou get the "
                "feeling you're not supposed to be in here, but there doesn't seem to be anyone around to stop you.\n "
                "\nThere are doors to your northeast, west, and northwest.",
                northeast=0, west=7, northwest=6, southeast=None, north=None, southwest=None, south=None,
                east=None, up=None, down=None)
    room_list.append(room)
    room = Room('bathroom',
                "You've entered a bathroom. The room is pristine and smells of citrus. There is a statue of an animal "
                "butler next to the toilet that is carrying a try with toilet paper on it. It seems out of place, "
                "given the rest of the bathroom being so posh. "
                "\nThere is a door to the southeast.",
                southeast=5, northeast=None, northwest=None, north=None, southwest=None, south=None, west=None,
                east=None, up=None, down=None)
    room_list.append(room)
    room = Room('closet',
                "You've entered a closet. It is strangely empty, aside from a single shirt stained with a blue "
                "liquid.\nThe shirt smells sickeningly sweet.\n\nThere is a door to your east.",
                east=5, southeast=None, northeast=None, northwest=None, north=None, southwest=None, south=None,
                west=None, up=None, down=None)
    room_list.append(room)
    room = Room('banquet hall',
                "You're in the banquet hall",
                north=0, southeast=None, northeast=None, northwest=None, southwest=None, south=None, west=None,
                east=None, up=None, down=None)
    room_list.append(room)
    room = Room('staircase',
                "Staircase",
                northwest=0, up=10, southeast=None, northeast=None, north=None, southwest=None, south=None, west=None,
                east=None, down=None)
    room_list.append(room)
    room = Room('chapel',
                "chapel",
                down=9, southeast=None, northeast=None, northwest=None, north=None, southwest=None, south=None,
                west=None,
                east=None, up=None)
    room_list.append(room)
    room = Room('exit',
                'exit',
                west=0, southeast=None, northeast=None, northwest=None, north=None, southwest=None, south=None,
                east=None, up=None, down=None)
    room_list.append(room)
    while not done:
        next_room = None
        # blank line to separate each room you navigate. may replace with a more robust clear screen function
        # (maybe with some ascii pictures? could be cool)
        print()
        print(room_list[current_room].description)
        user_choice = input("\nWhere do you want to go?: ")
        # Handle every possible direction
        if ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'n' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'north':
            next_room = room_list[current_room].north
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 's' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'south':
            next_room = room_list[current_room].south
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'sw' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'southwest':
            next_room = room_list[current_room].southwest
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'w' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'west':
            next_room = room_list[current_room].west
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'ne' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'northeast':
            next_room = room_list[current_room].northeast
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'e' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'east':
            next_room = room_list[current_room].east
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'se' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'southeast':
            next_room = room_list[current_room].southeast
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'nw' or (
                (user_choice.lower()).replace(' ', '')).replace('-', '') == 'northwest':
            next_room = room_list[current_room].northwest
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'up':
            next_room = room_list[current_room].up
        elif ((user_choice.lower()).replace(' ', '')).replace('-', '') == 'down':
            next_room = room_list[current_room].down
        elif user_choice.lower() == 'quit' or user_choice.lower() == 'q':
            print('Thanks for playing!')
            break
        # debug stuff (make it so you can turn this on at any time?)
        # print('current room: ', current_room, 'next room: ', next_room, 'user_choice: ', user_choice)
        # print(room_list[0].south)

        if next_room is None:
            print("You can't go that way.")
        else:
            current_room = next_room


if __name__ == '__main__':
    main()
