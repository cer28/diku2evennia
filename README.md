# diku2evennia
This project contains a few basic scripts to convert original DikMUD DB files from their native format into
Evennia-style batchcode. The resulting  batchcode files can then be imported into an Evennia world to create rooms.
exits, mobs, objects, and shops.

## Installation
DikuMUD DB files have not been included with this project. The original Tinyworld object files may be downloaded from
various places, such as:

- [DikuMUD Alfa version](https://github.com/Seifert69/DikuMUD) essentially the "official" release (see https://dikumud.com/download/), re-licensed under LGPL 2.1
- [alternative source on GitHub 1](https://github.com/sneezymud/dikumud)
- [tinyworld DB files in a different GitHub project](https://github.com/tpolecat/mud/tree/master/data)
- [diku-linux.tar.gz 1](http://ftp.lip6.fr/pub/linux/sunsite/games/muds/diku-linux.tar.gz) (1992-12-02 290K)
- [diku-linux.tar.gz 2](http://ftp.gwdg.de/pub/linux/funet/xtra/games/muds/diku-linux.tar.gz) (01-Dec-1992 22:00 296375 bytes)

There are slight differences in the data between the distributions. For example, "Luxan the Shopkeeper" and "The
Hierophant" appears in some versions but not others. Either version should work with these scripts.

From the distribution, copy the files dm-dist/lib/tinyworld.* into this project's dm-dist/lib folder.

```
dm-dist/lib/tinyworld.mob
dm-dist/lib/tinyworld.wld

# These are not yet being read
dm-dist/lib/tinyworld.obj
dm-dist/lib/tinyworld.shp
dm-dist/lib/tinyworld.zon
```

Additional [sample areas](./Caw-archive/Files/) have been included here from the CAW (Curious Areas Workshop) project.
The original files are  no longer available online, but have been obtained from [the archive.org snapshot](https://web.archive.org/web/20040604021951/http://qsilver.queensu.ca/~fletchra/Caw/).
Please note the [LICENSE](Caw-archive/Files/LICENSE.md) associated with the files. Also note that the files are named
verbatim from the original ending in "*.tar.gz"; however, the files are actually tar files and not gzipped.

## Usage

There are a few places in the original files where non-standard formatting causes issues with parsing. To fix these, run
the patch file:

```
patch -u -b -i dm-dist/lib/diku_tinyworld.patch
```

Once fixed, the scripts can be run:

```
python2 read_rooms.py > output/batchcode.py
python2 read_mobs.py >> output/batchcode.py
```

The output will be batchcode that can be executed in an Evennia world. Currently, rooms and exits are functional,
and the process detects rooms that are not connected by an exit from any other room. The zones have not been
fully implemented, but at this point they are crudely implemented via appending the original zone into the room
aliases. For example, tinyworld room #3001 in zone 30 will have the Evennia alias `tinyworld30#3001` set for it.

Example output (Rooms)
```
from evennia import create_object
import typeclasses.rooms
import typeclasses.exits

rooms = {}

rooms['tinyworld0#0'] = create_object(typeclasses.rooms.Room, key='The Void', aliases=['tinyworld0#0',])
rooms['tinyworld0#1'] = create_object(typeclasses.rooms.Room, key='The Void', aliases=['tinyworld0#1',])
rooms['tinyworld0#2'] = create_object(typeclasses.rooms.Room, key='Limbo', aliases=['tinyworld0#2',])
...
print "Rooms created: 657"

# -- Exits --
new_exit = create_object(typeclasses.exits.Exit, key='up', aliases=['u'], location=rooms['tinyworld0#0'], destination=rooms['tinyworld30#3001'])
new_exit = create_object(typeclasses.exits.Exit, key='north', aliases=['n'], location=rooms['tinyworld30#3001'], destination=rooms['tinyworld30#3054'])
...
print "Rooms with exits: 658"
#WARNING: Room #0 (The Void) is unreachable from any other room
#WARNING: Room #1 (The Void) is unreachable from any other room
#WARNING: Room #2 (Limbo) is unreachable from any other room
#WARNING: Room #1200 (The Chat Room) is unreachable from any other room
#WARNING: Room #1201 (Moses\' Hangout) is unreachable from any other room
#WARNING: Room #1202 (The centre of the universe.) is unreachable from any other room
#WARNING: Room #3031 (The Pet Shop) is unreachable from any other room
#WARNING: Room #3032 (Pet Shop Store) is unreachable from any other room
#WARNING: Room #3055 (Odin\'s Store) is unreachable from any other room
#WARNING: Room #4058 (The maze) is unreachable from any other room
#WARNING: Room #5577 (Ravan\'s hideout) is unreachable from any other room
#WARNING: Room #7130 (The sewer pipe.) is unreachable from any other room
#WARNING: Room #7301 (The Entrance to the Realm of silence) is unreachable from any other room
#WARNING: Room #7903 (The Artifact room of Naris) is unreachable from any other room
#WARNING: Room #8999 (The fog) is unreachable from any other room
```

Example output (Mobs)

TODO

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Debugging

This code is currently alpha status and in early development. To check the status of your imported world, count in the
evennia database:

```
After creating rooms

select count(*), db_typeclass_path from objects_objectdb where id > 2 group by db_typeclass_path

count(*)        db_typeclass_path
1493    typeclasses.exits.Exit
657     typeclasses.rooms.Room
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

