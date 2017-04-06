#!/usr/bin/python
import pymysql.cursors
import re
import sys
import os
from os import walk

def main():

    connection = pymysql.connect(host='localhost',                         
                                  user='root',
                                  password='',
                                  db='tdb',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)

    db_version = ''

    try:
        with connection.cursor() as cursor:
            sql = "select version from ecs order by version desc limit 1;"
            cursor.execute(sql)
            db_version = cursor.fetchone().get("version")
    except:
        connection.close()
        sys.exit()

    files = []
    for (dirpath, dirnames, filenames) in walk('./upgrades'):
        files.extend(filenames)
        break

    files.sort()

    for file in files:
        match = re.search('^(\d(?:\.\d+)+)(\.|\ )+?\w+\.sql$', file)

        found = match.group(1) if match else None
        print("Found is " + found)
        print("db_version is " + str(db_version))
        if found is None:
            continue
        if found < db_version:
            continue
        if found > db_version:
            new_db_version = found
            try:
                with connection.cursor() as cursor:
                    sql = open('./upgrades/' + file, 'r').read()
                    cursor.execute(sql)
                    sql = "update ecs set version=%s"
                    cursor.execute(sql, new_db_version)
            except:
                connection.rollback()
                connection.close()
                raise
            finally:
                connection.close()

        if found == db_version:
            print("I have made all of the upgrades to the current version. Exitting.");
            sys.exit()

if __name__ == '__main__':
	main()
