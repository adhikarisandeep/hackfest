
Scoring Server
==============

This is the scoring server for the `hackfest` competition.

Requirements
------------

You will need the `twisted` web server for things to work::

    sudo aptitude install python-twisted

Running
-------

To run the program::

    ./hackfest.sh

This will start the scoring server and also start the `twistd` web
server which will serve the site at <http://localhost:8080/>.

After you get everything running, goto
<http://localhost:8080/view-scores.html> to watch the action.  This
page will display the scores of the opposing teams and should
automatically update itself.

Notes
-----

This program was tested using:

 * `Ubuntu-9.10 <http://www.ubuntu.com/GetUbuntu/download>`_
 * `Python-2.6 <http://www.python.org/download/>`_
 * `Twisted-8.2 <http://twistedmatrix.com/trac/>`_
