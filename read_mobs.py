import re
import fileinput
import random
import argparse


# struct char_data *read_mobile(int nr, int type)


# db.c

def fread_string(fl):
    ret = ""
    while True:
        line = fl.readline()
        m = re.search(r'^([^~]*)(~)?', line)
        if m.group(2):
            if len(m.group(1)):  #todo why is the trailing newline still there?
                 ret = ret + m.group(1).rstrip("\n\r")
            break
        else:
            ret = ret + m.group(0)

    return ret


def dice(n, d):
    ret = 0
    for x in range(0, n):
        ret += random.randint(1,d)
    return ret

def main():
    default_mob_file = "dm-dist/lib/tinyworld.mob"
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mobs",
                        help=f"*.mob file containing mob definitions (default {default_mob_file})",
                        default=default_mob_file)
    args = parser.parse_args()

    fl = fileinput.input(args.mobs)
    
    while True:
        mob = {
            'id': None,
            'name': None,
            'short_descr': None,
            'long_descr': None,
            'description': None,
            'title': 0,
            'act': None,
            'affected_by': None,
            'alignment': None,
            'mobtype': None,
        }
        
        line = fl.readline().rstrip("\n\r")

        # Mob number
        m = re.search(r'^(#\w+)$', line)
        if m is None:
            print(f"ERROR: line {fl.lineno():d}: Couldn't read a mob number out of '{line}'")
            break
        else:
            mob['id'] = m.group(1)
        
        rname = fread_string(fl)

        if rname == "$":
            break

        mob['name'] = rname
        mob['short_descr'] = fread_string(fl)
        mob['long_descr'] = fread_string(fl)
        mob['description'] = fread_string(fl)

        # act affected_by alignment
        line = fl.readline()
        m = re.search(r'^([\d-]+)\s+([\d-]+)\s+([\d+-]+)\s+([A-Z])', line)

        if m == None:
            print("ERROR: line %d: Couldn't read the mob flags line from '%s'" % (fl.lineno(), line))
            break
        else:
            mob['act'] = m.group(1)
            mob['affected_by'] = m.group(2)
            mob['alignment'] = m.group(3)
            mob['mobtype'] = m.group(4)
        
        if mob['mobtype'] == "S":
            line = fl.readline()
            m = re.search(r'^([\d-]+)\s+([\d-]+)\s+([\d-]+)\s+(\d+)d(\d+)\+(\d+)\s+(\d+)d(\d+)\+(\d+)', line)

            if m == None:
                print("ERROR: line %d: Couldn't read the mob flags line from '%s'" % (fl.lineno(), line))
                break
            
            mob['level'] = m.group(1)
            mob['hitroll'] = m.group(2)
            mob['armor'] = m.group(3)
            mob['max_hit'] = dice( int(m.group(4)), int(m.group(5)) ) + int(m.group(6))
            mob['damnodice'] = m.group(7)
            mob['damsizedice'] = m.group(8)
            mob['damroll'] = m.group(9)

            mob['mana'] = 10
            mob['max_mana'] = 10
            mob['move'] = 50
            mob['max_move'] = 50

            line = fl.readline()
            m = re.search(r'^([\d-]+)\s+([\d-]+)', line)
            if m is None:
                print("ERROR: line %d: Couldn't read the mob gold/exp line from '%s'" % (fl.lineno(), line))
                break
            
            mob['gold'] = m.group(1)
            mob['exp_value'] = m.group(2)

            line = fl.readline()
            m = re.search(r'^([\d-]+)\s+([\d-]+)\s+([\d-]+)', line)
            if m is None:
                print("ERROR: line %d: Couldn't read the position/gender line from '%s'" % (fl.lineno(), line))
                break

            mob['position'] = m.group(1)
            mob['default_pos'] = m.group(2)
            mob['sex'] = m.group(3)

            mob['class'] = 0
            mob['weight'] = 200
            mob['height'] = 198
            mob['GET_COND'] = [ -1, -1, -1 ]
            mob['apply_saving_throw'] = max(20 - int(mob['level']), 2)
        
        else:
            print(f"ERROR: line {fl.lineno():d}: Can't yet handle non-S types")
        
        print("Finished reading a mob: %s" % mob['id'])
        #import pprint
        #pprint.pprint(mob)
        #break



        # S
        #   GET_LEVEL = %d
        #   hitroll = 20 - %d
        #   armor = 10 * %d
        #   %Dd%D+%D -> hit = max_hit = dice(tmp, tmp2)+tmp3
        #   %Dd%D+%D -> (damnodice, damsizedice, damroll)
        #   mana = 10
        #   max_mana = 10
        #   move = 50
        #   max_move = 50
        #   gold = %d
        #   GET_EXP = %d
        #   position = %d
        #   default_pos = %d
        #   sex = %d
        #   class = 0
        #   weight = 200
        #   height = 198
        #   GET_COND = (-1, -1, -1)
        #   apply_saving_throw[0..4] = MAX(20-GET_LEVEL(mob), 2)
        


main()
