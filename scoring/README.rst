
Scoring Server
==============

This is the scoring server for the `hackfest` competition.

Requirements
------------

You will need the `Twisted` web server for things to work.

On Ubuntu::

    sudo aptitude install python-twisted

Running
-------

To run the program on a machine::

    ./hackfest.sh

This will start the scoring server and also the `twistd` web
server which will serve the site at <http://localhost:8080/>.

After you get everything running, goto
<http://localhost:8080/view-scores.html> to watch the action.  

This page will display the scores of the opposing teams and will
automatically update itself.

Notes
-----

This program was tested using:

 * Ubuntu-9.10  <http://www.ubuntu.com/GetUbuntu/download>
 * Python:      <http://www.python.org/download/>
 * Twisted-8.2: <http://twistedmatrix.com/trac/>
