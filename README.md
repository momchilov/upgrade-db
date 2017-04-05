A simple database upgrade script.

This script does the following:
* A database upgrade requires the execution of numbered scripts stored in a folder. E.g. 045.createtable.sql
* There may be holes in the numbering and there isn't always a . after the number.
* The database upgrade works by looking up the current version in the database. It then compares this number to the scripts.
* If the version number from the db matches the highest number from the script then nothing is executed.
* If the number from the db is lower than the highest number from the scripts, then all scripts that contain a higher number than the db will be executed against the database.
* In addition the database version table is updated after the install with the latest number.

# Pre-requisites
Install Python's MySQL adapter on your system:  `sudo pip install pymysql`
