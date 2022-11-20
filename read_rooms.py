# TODO escape single quotes in descript; add description to batchcode

# ^#define \([A-Z_]+\)[ \t]+\([0-9]+\)
#     \2 : '\1',


import re
import fileinput
import argparse

class DikuRoom:

    #structs.h
    room_flags = {
        1 : 'DARK',
        2 : 'DEATH',
        4 : 'NO_MOB',
        8 : 'INDOORS',
        16 : 'LAWFULL',
        32 : 'NEUTRAL',
        64 : 'CHAOTIC',
        128 : 'NO_MAGIC',
        256 : 'TUNNEL',
        512 : 'PRIVATE',
    }


    dir_options = {
        '0' : {'def' : 'north', 'dir' : 'n', 'rev_dir' : 's'},
        '1' : {'def' : 'east',  'dir' : 'e', 'rev_dir' : 'w'},
        '2' : {'def' : 'south', 'dir' : 's', 'rev_dir' : 'n'},
        '3' : {'def' : 'west',  'dir' : 'w', 'rev_dir' : 'e'},
        '4' : {'def' : 'up',    'dir' : 'u', 'rev_dir' : 'd'},
        '5' : {'def' : 'down',  'dir' : 'd', 'rev_dir' : 'u'},

    }


    door_flags = {
        1 : 'EX_ISDOOR',
        2 : 'EX_CLOSED',
        4 : 'EX_LOCKED',
        8 : 'EX_RSCLOSED',
        16 : 'EX_RSLOCKED',
        32 : 'EX_PICKPROOF',
    }

    sector_types = {
        0 : 'SECT_INSIDE',
        1 : 'SECT_CITY',
        2 : 'SECT_FIELD',
        3 : 'SECT_FOREST',
        4 : 'SECT_HILLS',
        5 : 'SECT_MOUNTAIN',
        6 : 'SECT_WATER_SWIM',
        7 : 'SECT_WATER_NOSWIM',
    }

    def __init__(self):
        self.id = None
        self.name = None
        self.desc = None
        self.zone = None
        self.room_bits = None
        self.sector_type = None
        self.extra_desc: list = []
        self.directions: dict = {}
        self._seen = False
        self._reachable = False

    def getZonePlusId(self):
        return self.zone + self.id
    
    def __repr__(self):
        return "{%s, %s, %s}" % (self.id, self.name, self._seen)


# db.c

def fread_string(fl):
    ret = ""
    while True:
        line = fl.readline()
        m = re.search(r'^([^~]*)(~)?', line)
        if m.group(2):
            if len(m.group(1)):  #todo why is the trailing newline still there?
                 ret = ret + m.group(1)
            break
        else:
            ret = ret + m.group(0)

    return ret


def parse_into_zone(filename, zone_prefix):
    fl = fileinput.input(filename)

    rooms = {}
    room_list = []

    while True:
        room = DikuRoom()
        #id = None
        #name = None
        #desc = None
        #zone = None
        #room_bits = None
        #sector_type = None
        #extra_desc = []
        #directions = {}
        
        line = fl.readline().rstrip("\n\r")

        # Room number
        m = re.search(r'^(#\w+)$', line)
        if m is None:
            print("#ERROR: line %d: Couldn't read a room number out of '%s' -- exiting" % (fl.lineno(), line))
            break
        else:
            room.id = m.group(1)

        # Room Name
        room.name = fread_string(fl).replace("'", "\\'")

        if re.search(r';', room.name):
            print(f"#WARNING: line {fl.lineno():d}: Room name for room {room.id} ({room.name}) contains a semicolon, could be bad in a @batchcommand line")
            room.name = room.name.replace(";", "<semicolon>")

        if room.name == "$":
            #print("Found EOF marker -- exiting")
            break
        
        # Description
        room.desc = fread_string(fl)



        
        # Zone flags sector
        line = fl.readline()
        m = re.search(r'^([\d-]+)\s([\d-]+)\s([\d-]+)', line)
        if m == None:
            print("#ERROR: line %d: Couldn't read the zone/flag/sector line from '%s'" % (fl.lineno(), line))
            break
        else:
            room.zone = zone_prefix + m.group(1)
            room.room_bits = m.group(2)
            room.sector_type = m.group(3)
        
        # Directions or extra descriptions        
        while True:
            line = fl.readline()
            if line.startswith("S"):
                break
            elif line.startswith("D"):
                m = re.search(r'^D(\d+)\s', line)
                if m is None:
                    print("#ERROR: line %d: Can't match a direction for '%s'" % (fl.lineno(), line))
                    break
                tmp_dir = m.group(1)
                tmp_key = fread_string(fl)
                tmp_desc = fread_string(fl)
                line = fl.readline().rstrip("\n\r")
                (tmp_unk, tmp_doortype, tmp_target) = re.split(" ", line, 2)
                #tmp_flags = fread_string(fl)
                room.directions[tmp_dir] = { 'key' : tmp_key , 'desc' : tmp_desc, 'unk' : tmp_unk, 'flags' : tmp_doortype, 'target' : tmp_target  }
            elif re.search("^E", line):
                tmp_key = fread_string(fl)
                tmp_desc = fread_string(fl)
                room.extra_desc.append( { tmp_key : tmp_desc } )
            else:
                print("#ERROR: line %d: Expecting D|E|S, not '%s'" % (fl.lineno(), line))

                
                # there shouldn't blank lines, but if there are, ignore them
                if re.search(r'^\W*$', line):
                    print("#   ... but quietly ignoring this blank line")
                else:
                    break

        #print("Finished reading a room: %s" % room.id)
        #print room.toBatchCommand()
        #rooms[ room.id ] = room
        room_list.append(room)
        
        #import pprint    
        #pprint.pprint(room)
        #break
    #for room in room_list:
    #    print "Found a room: " + room.id
    return room_list    
        

def room_batch_commands(rooms, room):
        if room._seen:
            #print "#seen: room %s" % room.id
            return

        #print room.printBatchCommand(rooms)
        zid = room.getZonePlusId()
        print(f"@tel {zid}")
        print("#")
        print(f"@desc {zid} = {room.desc}")
        print("#")

        for (dir, ex) in room.directions.items():
        
            k = "#" + ex['target']
            dir = DikuRoom.dir_options[dir]['dir']
            if k in rooms.keys():
                # assume the exit is to the same zone, since it's ambiguous otherwise
                print(f"@tunnel/oneway {dir} = {rooms[k].name};{rooms[k].zone}#{ex['target']}")
                print("#")
            else:
                print (f"#ERROR: (ROOM DOES NOT EXIST) @tunnel/oneway {dir} = {room.zone}#{ex['target']}")

        room._seen = True
        for (dir, ex) in room.directions.items():

            k = "#" + ex['target']
            if k in rooms.keys():
                room_batch_commands(rooms, rooms[k])
            else:
                print (f"#ERROR: Room {room.id} refers to exit to {k} which does not exist")

def room_batch_code(rooms, room):
        if room._seen:
            print (f"#ERROR: Already output room {room.id}")
            return
        else:
            key = room.getZonePlusId()
            print (f"rooms['{key}'] = create_object(typeclasses.rooms.Room, key='{room.name}', aliases=['{key}',])")
            room._seen = True

def room_batch_code_exits(rooms, room):
        if not room._seen:
            print (f"#ERROR: Printing exits for room {room.id} which hasn't been created yet")
            return
        else:
            for (dir, ex) in room.directions.items():
                tmp = "#" + ex['target']
                if tmp in rooms.keys():
                    room2 = rooms[tmp]
                    if room2._seen:
                        #todo custom aliases
                        print (f"new_exit = create_object(typeclasses.exits.Exit, key='{DikuRoom.dir_options[dir]['def']}', aliases=['{DikuRoom.dir_options[dir]['dir']}'], location=rooms['{room.getZonePlusId()}'], destination=rooms['{room2.getZonePlusId()}'])")
                        room2._reachable = True
                    else:
                        print (f"#ERROR: Room {room.id} has an exit to room {room2.id}, which hasn't been output")
                else:
                    print (f"#ERROR: Room {room.id} refers to exit to {tmp} which does not exist")

def create_batch_output(room_list, output_type):
    if output_type not in ('batchcommand', 'batchcode'):
        print (f"#ERROR creating output, unknown output type '{output_type}'")
        return

    rooms = {}
    for room in room_list:
        rooms[room.id] = room

    if output_type == 'batchcommand':
        # Just need the first room, and it will do a breadth-first walk through anything connected
        room_batch_commands(rooms, room_list[0])

        #for room in room_list:
        #    if not room._seen:
        #        print "#WARNING: Room not linked: %s - %s" % (room.id, room.name)
        for room in [ r for r in room_list if not r._seen ]:
            print (f"#WARNING: Room {room.id} ({room.name}) is unreachable from any path starting from {room_list[0].id}")

    elif output_type == 'batchcode':

        print ("from evennia import create_object\n" \
            "import typeclasses.rooms\n" \
            "import typeclasses.exits\n" \
            "\n" \
            "rooms = {}\n")

        # Create all the rooms in order
        ct = 0
        for room in room_list:
            room_batch_code(rooms, room)
            ct += 1
            if ct % 100 == 0:
                print (f'print "Rooms created: {ct:d}"')

        print (f'print "Rooms created: {ct:d}"')

        # Now create all the exists in order
        print ("\n# -- Exits --")
        ct = 1
        for room in room_list:
            room_batch_code_exits(rooms, room)
            ct += 1
            if ct % 100 == 0:
                print (f'print "Rooms with exits: {ct:d}"')

        print (f'print "Rooms with exits: {ct:d}"')
        
        for room in [ r for r in room_list if not r._reachable ]:
            print (f"#WARNING: Room {room.id} ({room.name}) is unreachable from any other room")
        
    



def create_batch_commands(room_list, start, direction):
    print ("@tel {start}")
    print ("#")
    print (f"@tunnel/oneway {direction} = {room_list[0].name};{room_list[0].getZonePlusId()}")
    print ("#")
    create_batch_output(room_list, 'batchcommand')


def create_batch_code(room_list):
    create_batch_output(room_list, 'batchcode')


default_world_file = "dm-dist/lib/tinyworld.wld"
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rooms",
                    help=f"*.wld file containing room definitions (default {default_world_file})",
                    default=default_world_file)
args = parser.parse_args()

room_list = parse_into_zone(args.rooms, "tinyworld")

#create_batch_commands(room_list, "Limbo", "e")

create_batch_code(room_list)
