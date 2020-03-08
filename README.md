# stopeight editor

Python2 branch of stopeight. stopeight versions 3 and above do not work with version 2 of the Python interpreter anymore.

This build has been tested on Ubuntu 18.04.

1. PyQt5 has been removed from PyPI/pip2. It is required for the editor. It is available from the Universe repository.
+
```shell
$ sudo apt-get install python-pyqt5
```

2. Install the following minimal requirements from the main repository.
+
```shell
$ sudo apt-get install python python-pip
```

3. Clone the Python2 branch of the Github repository recursively.
+
```shell
$ git clone --recurse-submodules https://github.com/specpose/stopeight.git
$ git checkout Python2
```

4. If you want to run the tests for the legacy algorithm, install Qt5.
+
```shell
$ sudo apt-get install qtbase5-dev
```

5. Build in the stopeight directory.
+
```shell
$ cd stopeight
$ python setup.py install --user
```

6. Launch the editor.
+
```shell
$ python -m stopeight.util.editor.dispatch
```

# stopeight SOAP/XMLRPC server

The server is discontinued in version 3 of the Python interpreter because of missing ZSI in PyPI/pip3.

The server is only available in the git repository.
+
```shell
$ cd /path/to/where/stopeight
```

It relies on SOAP for client/server communication, therefore ZSI is needed.

Python 3: ZSI 2.0 release candidates don't work. Also ConfigParser is missing in Python3. Status Not working.

ZSI 2.1a2 is a version that does not require PyXML anymore. Install ZSI.
+
```shell
$ sudo apt-get install subversion
$ cd /path/to/temp/dir
$ svn checkout svn://svn.code.sf.net/p/pywebsvcs/code/trunk pywebsvcs-code
```

Download and run in subdirectory zsi.
+
```shell
$ cd /path/to/temp/dir/pywebsvcs-code/zsi
$ python setup.py install --user
```

## Storage Setups

### File Storage

For running against a file storage, you need ZODB.
+
```shell
$ pip install ZODB3
```

Tested working with version:
+
ZODB3-3.10.5.tar.gz

Run zodbTools to make a Data.fs file.
+
```python
from ZODB.FileStorage import FileStorage
from stopeight.server import server_include
FileStorage(server_include.zodb_filename)
```

Run configuration.
+
```python
$ python -m stopeight.server.zodbTools
```

### Database

For running against a rails2.3 style db instead, you need elixir, SQLAlchemy, mysqlclient.
+
```shell
$ pip install mysqlclient Elixir SQLAlchemy==0.7.8
```

Tested working with versions:
+
Elixir-0.7.1.tar.gz
SQLAlchemy-0.7.8.tar.gz

You need to modify 3 lines of code in the server module. Change occurences of:
+
```
"from zodbTools import DBLine"
```

to:
+
```
"from elixirTools import DBLine"
```

And setting the database connection in stopeight.server.server_include according to your database installation. I have successfully tested MySQL. The elixir code follows the rails ActiveRecord convention.

## stopeight Server: Starting the server

To launch the server do the following from the same directory.
+
```python
from stopeight.server import server_soap
server_soap.run(8888)
```

## stopeight Server: Testing it

I have provided example-scripts for all of the SOAP commands.
+
```shell
$ cd /path/to/where/stopeight
```

To save your first line on the server, run:
+
```shell
from stopeight.server import client_saveLine_test
client_saveLine_test.run()
```

This should produce output containing the id of your newly created line.
Store this id.

To check whether an input line matches any of the reference lines, do the following:
+
```shell
    >>> from stopeight.server import client_matchLine_test
    >>> client_matchLine_test.run()
```

This will return both the data and the id's that have matched your input.

If you want to just retrieve the data of a reference line, you can do so by submitting the id.
+
```shell
from stopeight.server import client_getLine_test
client_getLine_test.run()
```

This will return the data associated to the reference line on record.

And finally, if you want to delete a reference line in the database, send the id
+
```shell
from stopeight.server import client_deleteLine_test
client_deleteLine_test.run()
```

Please refer to the code-samples for further information on how to use this from within your code.
