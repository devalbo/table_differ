table_differ
============

What it is
----------
Compare tables, grids, 2D arrays of data side by side in your web browser

Installation
------------
Windows

* Install Python 2.7 from http://www.python.org

* Get git working (git hub has Git for Windows at http://msysgit.github.io/)

* Make a fork of the table_differ repository in github

* Git clone the fork

* Get VirtualEnv running... this will help keep development environment clean and reproducible
http://www.slideshare.net/sivasubramaniam3/installing-python-setup-tools-virtual-env-in-windows

* Create a virtual environment to develop with
> virtualenv venv-table_differ

* Activate the virtual environment

* Download the dependencies into the virtual environment using pip
> pip install -r requirements.txt

* Run the server
> python new_server.py