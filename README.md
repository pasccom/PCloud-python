REPOSITORY DESCRIPTION
----------------------

This repository contains a partial implementation of PCloud API in Python.
It currently supports the following parts of PCloud API:
  - General
  - Folder
  - File
  - FileOps

USAGE
-----

The API can be accessed thanks to a context manager
```python
    with PCloud() as pClould:
        pCloud.username = 'username'
        pCloud.password = 'password'

        # Make an API request
        pCloud.userInfo()
```
Noctice that you can alse pass the username and password directly to the `PCloud` constructor.
The connection to the `PCloud` API server will be initiated only on the first API request
(`userInfo()` on the above example).

PCloud FileOps API is used as follows
```python
    with PCloud() as pClould:
        pCloud.username = 'username'
        pCloud.password = 'password'

        with pCloud.createFile(0, 'test.txt') as f:
            f.write('Hello world!')
```

More information is given in the documentation.

MAKING THE DOCUMENTATION
------------------------

The documentation of the utilities included in PythonUtils is provided as
Sphinx reStructuredText, which can be compiled into beatiful documentation
by [Sphinx](http://www.sphinx-doc.org).

To compile the documentation you have to install Sphinx, which can be done using
```
pip install -U sphinx
```
If you are using Unix, you will also need `make`, which is generally provided
by default.

Then `cd` into the `doc` subdirectory and run e.g.
```
make html
```
to generate HTML documentation. The documentation is output in `doc/_build` by default.

LICENSING INFORMATION
---------------------
These programs are free software: you can redistribute them and/or modify
them under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

These programs are distributed in the hope that they will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

