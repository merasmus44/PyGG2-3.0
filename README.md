PyGG2-3.0 - What is it?
====================

PyGG2-3.0 is a Python3 port of  [PyGG2](https://github.com/PyGG2/PyGG2), which is a python2 port of [Gang Garrison 2](http://ganggarrison.com/).

HELP NEEDED
------------
I need help porting the python C extension files (in mask_extension) to the newest version of cython. It will take a while to do this on my own, because I don't know C very well. If you think you could help with this, go ahead and edit the file, then make a pull request with your fix.

Why is this not working?
------------
This is alot of work, specifically porting pySFML to pygame. Also I am currently unable to build for windows because I don't know how to link python properly to gcc 

Dependencies
------------

PyGG2-3.0 requires the following dependencies, in addition to Python 3.x:

* [pygame ](https://pypi.org/project/pygame)
* [pySFML ](https://pypi.org/project/sfml/) (optional)
* [Python Imaging Library](https://pypi.org/project/Pillow/)
* PyGG2-3.0 bitmask extension (compile with `python make.py build`, with `gcc` in path)

License
-------
(Same as the licence for PyGG2)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
