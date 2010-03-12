'''
This the main component of the scoring server.  

It consists of a simple framework that awards the teams points based on 
the status of the network services they are providing.

Created: March 10, 2010
   
Contributors:
    Jon Waltman (jonathan.waltman@gmail.com)
'''
##############################################################################
# Commentary:
#
# To record the log of events and to allow other processes to check the current
# score, we simply write a JSON string representation of the team and its data
# to log files.

import sys
import os
import json
import random
import time
from datetime import datetime
from optparse import OptionParser
from twisted.web import client


##############################################################################
# Team

class Team(object):
    '''
    A hackfest competitor.
    '''
    def __init__(self, name, services):
        '''
        Create a new team named `name`.
        
        `services` indicate the services that should be checked for this team.
        '''
        self.name = name
        self.score = 0
        self.services = dict.fromkeys(services, False)
        self.time = None
        self.logdir = "logs/%s/" % name
        try: 
            os.makedirs(self.logdir)
        except:
            pass                # Already exists?
        
    def update(self):
        '''
        Update the team's score by checking the status of its `services`.
        '''
        for s in self.services:
            self.services[s] = s.status()
            self.time = str(datetime.now())
            if self.services[s]:
                self.score += s.points
        self.log()

    def log(self):
        '''
        Save self to appropriate log files as JSON.
        '''
        logfile = self.logdir + "%d" % time.time()
        scorefile = self.logdir + "current-score"
        with open(logfile, 'w') as log:
            with open(scorefile, 'w') as score:
                js = self.json()
                log.write(js)
                score.write(js)

    def json(self):
        '''
        Get a JSON representation of the team.
        
        The returned form is useful for passing data to Javascript 
        via HTTP requests.
        '''
        servs = {}
        for s in self.services:
            servs[s.__class__.__name__] = self.services[s]
        team = vars(self).copy()
        team['services'] = servs
        return json.dumps(team)


##############################################################################
# Services

class Service(object):
    '''
    Represents a network service whose status can be checked.
    '''
    def status(self):
        '''
        Get the current status of service.
        '''
        if OPTS.randomize:
            return random.choice((True, False))
        return self._status()
        
class URL(Service):
    '''
    A service to check the owner of a URL.
    '''
    def __init__(self, teamname, url, points=1):
        '''
        Create a new URL service. 
        '''
        self.teamname = teamname
        self.url = url
        self.points = points

    def _status(self):
        '''
        Get the current status of this service.
        
        Reads the specified `url` and searches for `teamname`.
        '''
        try: page = client.getPage(self.url)
        except: return False
        # Page should contain text like `NAME Team'
        regex = r'(\w+)\sTeam'
        match = re.search(regex, page, re.I)
        owner = match.group(1) if match else ''
        return self.teamname.upper() == owner.upper()
    
class SSH(Service):
    '''
    A service that checks whether an `ssh` connection can be established.
    '''
    def __init__(self, user, host, points=2):
        '''
        Create a new SSH service.
        '''
        self.user = user
        self.host = host
        self.points = points
        
    def _status(self):
        # TODO: Implement
        return True


##############################################################################

# The hackfest competitors
teams = [
    Team('red', (
            URL('red', 'localhost'),
            SSH('whitey', 'localhost'),
            )),
    Team('blue', (
            URL('blue', 'localhost'),
            SSH('whitey', 'localhost'),
            )),
    ]

def _setup_server():
    '''
    Preliminary setup for the server.
    '''
    # We only want one running instance of the server
    try:
        with open("server.pid") as f:
            p = f.read()
        try:
            os.kill(int(p), 9)
            print >>sys.stderr, "server: Killed previous instance"
        except Exception as e:
            print >>sys.stderr, "server: Failed to kill previous instance" \
                "[pid=%s]:" % p, e
    except:
        pass
    # Save our pid
    with open("server.pid", 'w') as f:
        f.write(str(os.getpid()))
    # Add hook to remove file on exit
    import atexit
    atexit.register(lambda: os.remove("server.pid"))
    

def main():
    '''
    Start the hackfest competition.
    '''
    # Command-line args
    parser = OptionParser()
    parser.add_option("--random", action='store_true', dest="randomize",
                      help="generate random scores [%default]", default=True)
    parser.add_option("--sleep", type=float, dest="sleep",
                      help="time to sleep between updates [%default]", 
                      metavar='secs', default=5)
    global OPTS, ARGS
    OPTS, ARGS = parser.parse_args()
    _setup_server()
    print >>sys.stderr, "server: Hackfest has started!"
    # Update the teams
    while 1:
        for t in teams:
            t.update()
        time.sleep(OPTS.sleep)

if __name__ == '__main__':
    main()
