# sharding-blackout

```
usage: simulate.py [-h] [-n SERVER_COUNT] [-c COPIES] [-r RECORDS]
                   [-k RECORDS] [--random] [--mirror]

Simulates a failure on a distributed database.

optional arguments:
  -h, --help       show help message and exit
  -n SERVER_COUNT  number of servers to simulate
  -c COPIES        specifies how many copies of one record are stored at once
  -r RECORDS       specifies how many records will be written in the database
  -k RECORDS       specifies the amount of servers to be killed
  --random         this flag forces the database to allocate records in random
                   order
  --mirror         this flag forces the database to allocate records in a
                   mirrored order (this is the default action)
```
