# Which Tables Touched

This is a python script which will accept a mysql general log file and print out the names of the tables that were mentioned.

It does not parse the SQL.  Instead it connects to the database and finds the list of tables.  Then it finds which of those appear in the log file

## To use

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
