table_differ
============

What it is
----------
Compare tables, grids, 2D arrays of data side by side in your web browser

Installation
------------
Windows

* Install Python 2.7 from http://www.python.org

* Get git working (git hub has Github for Windows at http://windows.github.com/)

* Make a fork of the table_differ repository in github, then > git clone the fork.
<https://help.github.com/articles/fork-a-repo> is a good link describing github's recommended process for forking
a repo.

* Make a fork of

* Git clone the fork

* Get Pip and VirtualEnv running... this will help keep development environment clean and reproducible
https://zignar.net/2012/06/17/install-python-on-windows/

* Create a virtual environment to develop with
> virtualenv venv-table_differ

* Activate the virtual environment

* Download the dependencies into the virtual environment using pip (do this from the same shell window
you activated the virtual environment from)
> pip install -r requirements.txt

* Initialize the ORM/sqlite database. This will create a file named "table_differ.db". Whenever you want a clean slate,
delete this file and run the command again.
> python db_init.py

* Run the server
> python new_server.py