# Which Tables Touched

This is a python script which will accept a mysql general log file and print out the names of the tables that were mentioned.

It does not parse the SQL.  Instead it connects to the database and finds the list of tables.  Then it filters the log file based on what it found in the database.  If you have tables named `select`, expect them to show up as false-positives.

## Get the MYSQL general query log

### Tell mysql where to put the log file
Add this line to `my.cnf` (on some systems it will be `mysql.conf.d/mysqld.cnf`).

    general_log_file = /path/to/query.log```

### Enable the general log
    mysql> SET global general_log = 1;

(don't forget to turn this off, it can grow very quickly)

### Do the thing
All mysql queries will be added to `/path/to/query.log`

### Disable the general log
    mysql> SET global general_log = 0;

Warning: If you are working on an active database, the log file can grow very quickly.

## Extract table names

#### Have python 3.3 or higher installed

#### Create a virtual environment
Do this just once (it will create a directory)

`❯ ` `python3 -m venv which-venv`

#### Enter a virtual environment

`❯ ` `source which-venv/bin/activate`

#### Prepare environment
Do this just once

`which-venv ❯ ` `pip install --upgrade pip`

`which-venv ❯ ` `pip install -r requirements.txt`

#### Run it

`which-venv ❯ ` `python which_tables.py mysql_general.log --database meta --user root --password test`

#### Exit virtual environment

`which-venv ❯ ` `deactivate`

`❯ `

## For more, try --help

```
which-venv ❯ python which_tables.py --help

    usage: which_tables.py [-h] [-d DATABASE] [-u USER] [-p PASSWORD] file

    positional arguments:
      file

    optional arguments:
      -h, --help            show this help message and exit
      -d DATABASE, --database DATABASE
                            the name of the database whose tables we want
                            (default: moonpie)
      -u USER, --user USER  the mysql username (default: root)
      -p PASSWORD, --password PASSWORD
                            the mysql password (default: thangs)
```

## Oddities

If you need root permissions to view generalQuery.sql, but find that root permissions make your packages unavailable (i.e. it takes you out of your venv) you might consider running it like this:

```
sudo .venv/bin/python which_tables.py -d meta -u root -p test /var/tmp/generalQuery.log
```
