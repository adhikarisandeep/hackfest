Requirements
------------

Scoring Server
==============

The scoring server will provide live scoring during a competition. The
red and blue teams are required to maintain a set of services
online. So, the scoring server periodically checks if the
aforementioned services are online.

Depending on the services that are online or offline the concerned
team will be awarded or deducted points respectively. The scoring
server will also set up a log of all the scoring events so that these
events can be examined at a later time.

The scoring server will also need to allow Manual Adjustment of
scores. For earning extra points and for breaking the rules.

It should also be able to support some sort of messaging system.

The scoring server will reside in a rackmount along with the scoring
client.

Scoring Client
==============

The messaging data that is generated by the scoring server will be
captured by the scoring client, which it displays to everyone in a
graphical manner.

There should be support for participating teams greater or equal to
two.

Chat Mechanism
==============

It should be developed in such a way that Red and Blue in no way can
communicate with each other. It should only allow Red or Blue to
communicate with the White administrative team.

Since the blue team or the red team may use encryption methods while
sending messages. The chat mechanism must also have a feature that is
able to decrypt the cipher text.

Challenge Server
================

A Challenge Server will need to be implemented that will function as a
point of contact for the ongoing challenges and team submissions.

The Challenge Server will also alert teams of new challenges as they
become available and also it will be able to accept submissions from
both the teams.

It should also support wireless challenges. Wireless challenges will
get more difficult by the question and unlike other challenges once it
has been solved the opponent team cannot submit its version.

Capture the Flag
================

White team will have several captures the flag servers which will have
a number of services such as SSH HTTP FTP, and Red and Blue may decide
to capture the flag by logging in successfully and modifying a
variable to their name.

Here again points will be awarded to teams which capture the flag. So
the scoring server should check the capture the flag servers also at
regular intervals.
