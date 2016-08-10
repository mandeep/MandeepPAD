============
MandeepPAD
============

MandeepPAD is a rich and plain text editor built with Python and the PyQt5 library. The application
was created as a way to learn PyQt in addition to continuing a project I started in Visual Basic 6
at the ripe old age of 12.

-------------------
|travis| |coverage|
-------------------

.. image:: mpad/images/screen.png

************
Installation
************

The text editor is dependent on the PyQt5 library. If the user's system Python is 3.5 or greater, setup.py will attempt to install PyQt5, otherwise the user is responsible for installing the PyQt5 package. Once PyQt5 is installed in the working environment, MandeepPAD can be installed by invoking the following commands::

    git clone https://github.com/mandeepbhutani/MandeepPAD.git
    cd MandeepPAD
    pip install .

When the package is finished installing, the following command will run the application::

    MandeepPAD

.. |travis| image:: https://travis-ci.org/mandeepbhutani/MandeepPAD.svg?branch=master
    :target: https://travis-ci.org/mandeepbhutani/MandeepPAD
.. |coverage| image:: https://coveralls.io/repos/github/mandeepbhutani/MandeepPAD/badge.svg?branch=master
    :target: https://coveralls.io/github/mandeepbhutani/MandeepPAD?branch=master