#!/usr/bin/env bash

# given a database and a mysql general log file, list the tables that were touched during the log session

import os
import MySQLdb
import argparse
import re
from sys import platform
from collections import namedtuple
from sh import netstat, awk, bash

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # some defaults
    ddatabase = 'moonpie'
    duser = 'root'
    dpasswd= 'thangs'

    # not always necessary, this works around an oddity I found one day:
    #    _mysql_exceptions.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)")
    # if you see that error, go uncomment socket-related things below

    #if platform == "linux" or platform == "linux2":
    #    dsocket= str(awk(netstat('-ln'), '/mysql(.*)?\.sock/ { print $9 }')).strip()
    #elif platform == "darwin":
    #    dsocket= str(awk(netstat('-an'), '/mysql(.*)?\.sock/ { print $5 }')).strip()
    #else:
    #    print("please specify the mysql socket explicitly")
    #    dsocket=""

    parser.add_argument('-d', '--database', default=ddatabase, help='the name of the database whose tables we want')
    parser.add_argument('-u', '--user', default=duser, help='the mysql username')
    parser.add_argument('-p', '--password', default=dpasswd, help='the mysql password')
    #parser.add_argument('-s', '--socket', default=dsocket, help='the Unix socket for the mysql daemon')
    parser.add_argument('file', type=str)

    return parser.parse_args()

# preprocess the file to reduce its size
# (I expect the utilities below are faster than I can manage with python,
#  and easier than I can manage with anything else)
def get_candidates(in_file):

    with open(in_file, 'r') as log:

        # this is slow
        #      uniq(
        #          sort(
        #              egrep(
        #                  tr(
        #                      tr(
        #                          cat(in_file),
        #                          ['-s', '[:space:]', r'\n']),            # spaces -> newlines
        #                      ['-c', '-d', '[a-zA-Z0-9][:space:][_\-]']), # strip non-table-name characters
        #                  ['-v', '[0-9]'])                                # ignore id's
        #              )                                                   # sort
        #          )                                                       # ignore duplicates
        #      ).split()                                                   # as a list of words

        # this is faster
        command = '''cat {} | tr -s [:space:] '\n' | tr -c -d '[a-zA-Z0-9][:space:][_\-]' | egrep -v '[0-9]' | sort | uniq'''.format(in_file)
        return str(bash(['-c', command])).split() # as a list of words

def main(args):

    # connect to the database
    db=MySQLdb.connect(
            host='localhost',
            user=args.user,
            passwd=args.password,
            database=args.database)
            # unix_socket=args.socket)

    c = db.cursor()
    c.execute("show tables;")

    # get the set of table names
    tables = set()
    row = c.fetchone()
    while row is not None:
        tables.add(row[0])
        row = c.fetchone()

    # get the set of words in the log file
    log_words = set(get_candidates(args.file))

    # print their intersection
    for table in list(tables.intersection(log_words)):
        print(table)

if __name__ == '__main__':
    args = parse_args()
    main(args)
