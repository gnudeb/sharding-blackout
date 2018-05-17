#!/usr/bin/env python3
import argparse
from itertools import permutations
import random


class Server(set):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity
        self.is_running = True

    def is_full(self):
        return len(self) >= self.capacity

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False


class Database:
    """Represents a database that redundantly stores records on different servers."""
    def __init__(self, server_count=10, server_capacity=5):
        self.servers = [Server(server_capacity) for _ in range(server_count)]
        self.records = set()

    def __str__(self):
        return "Database({}, servers={})".format(len(self.servers), self.servers)

    def __repr__(self):
        return self.__str__()

    def push(self, record, times=2, at_random=False):
        """Inserts the `record` into several distinct `server`s `times` times."""
        self.records.add(record)
        available_servers = tuple(filter(lambda s: not s.is_full(), self.servers))

        if at_random:
            servers = random.sample(available_servers, times)
        else:
            servers = available_servers[:times]

        for server in servers:
            server.add(record)

    def check_integrity(self):
        """Returns `False` if at least one record is not present on running `server`s."""
        running_servers = filter(lambda s: s.is_running, self.servers)
        stored_data = set().union(*running_servers)
        return stored_data == self.records

    def restore(self):
        for server in self.servers:
            server.start()

    def blast(self, count=2):
        """
        Checks average durability of database by disabling every
        combination of `count` servers and checking integrity of the
        resulting database.

        Returns the probability in percents (0-100).
        """
        trials = 0
        failures = 0
        for unlucky_servers in permutations(self.servers, count):
            trials += 1
            self.restore()
            for server in unlucky_servers:
                server.stop()
            if not self.check_integrity():
                failures += 1
        self.restore()
        return round(100 * failures / trials)


class SimulatorArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description="Simulates a failure on a distributed database.")
        self.add_argument("-n", default=10, metavar="SERVER_COUNT", type=int,
                          help="number of servers to simulate")
        self.add_argument("-c", default=2, metavar="COPIES", type=int,
                          help="specifies how many copies of one record are stored at once")
        self.add_argument("-r", default=100, metavar="RECORDS", type=int,
                          help="specifies how many records will be written in the database")
        self.add_argument("-k", default=2, metavar="RECORDS", type=int,
                          help="specifies the amount of servers to be killed", )
        self.add_argument("--random", action="store_true",
                          help="this flag forces the database to allocate records in random order")
        self.add_argument("--mirror", action="store_true",
                          help=("this flag forces the database to allocate records in a "
                                "mirrored order (this is the default action)"))


if __name__ == "__main__":
    args = SimulatorArgumentParser().parse_args()

    server_count = args.n
    record_count = args.r
    redundancy = args.c
    # `+ 1` prevents an edge case where the last n free spaces happen
    # to be in one server
    server_capacity = server_count * redundancy + 1
    servers_to_kill = args.k

    db = Database(server_count=args.n, server_capacity=server_capacity)
    for record in range(record_count):
        db.push(record, at_random=args.random)

    print("Simulating {} servers with {} records, redundancy of {} and {} record storing".format(
        server_count, record_count, redundancy, "random" if args.random else "mirror"
    ))

    failure_probability = db.blast(count=servers_to_kill)

    print("Killing {} arbitrary servers results in data loss in {}% cases".format(
        servers_to_kill, failure_probability
    ))
