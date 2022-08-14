# diku2evennia
This project contains a few basic scripts to convert original DikMUD DB files from their native format into Evennia-style batchcode. The resulting
batchcode files can then be imported into an Evennia world to create rooms. exits, mobs, objects, and shops.

## Installation
DikuMUD DB files have not been included with this project. The original Tinyworld object files be downloaded from various places, such as:

- [DikuMUD Alfa version](https://github.com/Seifert69/DikuMUD) essentially the "official" release (see https://dikumud.com/download/), re-licensed under LGPL 2.1
- [alternative source on GitHub 1](https://github.com/sneezymud/dikumud)
- [tinyworld DB files in a different GitHub project](https://github.com/tpolecat/mud/tree/master/data)
- [diku-linux.tar.gz 1](http://ftp.lip6.fr/pub/linux/sunsite/games/muds/diku-linux.tar.gz) (1992-12-02 290K)
- [diku-linux.tar.gz 2](http://ftp.gwdg.de/pub/linux/funet/xtra/games/muds/diku-linux.tar.gz) (01-Dec-1992 22:00 296375 bytes)

There are slight differences in the data between the distributions. For example, "Luxan the Shopkeeper" and "The Hierophant" appears in some versions
but not others. Either version should work with these scripts.

From the distribution, copy the files dm-dist/lib/tinyworld.* into this project's dm-dist/lib folder.

```
dm-dist/lib/diku_tinyworld.wld
dm-dist/lib/diku_tinyworld.wld.ORIG
dm-dist/lib/tinyworld.mob
dm-dist/lib/tinyworld.mob.ORIG
dm-dist/lib/tinyworld.obj
dm-dist/lib/tinyworld.shp
dm-dist/lib/tinyworld.zon
```

## Usage
```
python2 read_rooms.py > output/batchcode.py
python2 read_mobs.py >> output/batchcode.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Debugging

This code is currently alpha status and in early development. To check the status of your imported world, count in the evennia database:

```
After creating rooms

select count(*), db_typeclass_path from objects_objectdb where id > 2 group by db_typeclass_path

count(*)        db_typeclass_path
1493    typeclasses.exits.Exit
657     typeclasses.rooms.Room
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

