=====
roper
=====

A CLI refactoring tool using the `rope <https://github.com/python-rope/rope>`_ library.

Install
=======
To install for the current user, do::

    $ pip install --user roper

Develop
=======
This currently use https://python-poetry.org/ for package handling and more. To install from a
checked out repo, do::

    $ pip install --user poetry
    $ poetry install

in the project directory. Enter the virtualenv by running::

    $ poetry shell

Other tasks are handled by `sykel`. To install, do::

    $ pip install --user sykel

To preapre a release, do::

    $ sykel version.bump
    $ sykel package.clean package.build
    $ sykel package.publish


Alternatives
============

IDEs
----
* PyCharm - https://www.jetbrains.com/help/pycharm/refactoring-source-code.html

Editor plugins
--------------
* vim - https://github.com/python-rope/ropevim
* emacs - https://github.com/python-rope/ropemacs

Libraries
---------
* bowler - https://pybowler.io/
* libcst - https://libcst.readthedocs.io/en/latest/
* undebt - https://github.com/Yelp/undebt
* redbaron - http://redbaron.pycqa.org/en/latest/

Resources
=========
* https://github.com/python-rope/rope
* https://realpython.com/python-refactoring/
