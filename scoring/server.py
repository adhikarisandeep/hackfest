'''
The scoring server for hackfest.
'''

import sys, os
import json
import random
import time
from datetime import datetime

from twisted.web import client


##############################################################################
# Team

class Team(object):
    '''
    A hackfest competitor.
    '''
    def __init__(self, name, services):
        '''
        Create a new team named 'name'.
        
        'services' indicate the services that should be checked for this team.
        '''
        self.name = name
        self.score = 0
        self.services = dict.fromkeys(services, False)
        self.time = None
        self.logdir = "logs/%s/" % name
        try:
            os.makedirs(self.logdir)
        except:
            pass
        
    def update(self):
        '''
        Update the team's score by checking the status of its 'services'.
        '''
        for s in self.services:
            self.services[s] = s.status()
            self.time = str(datetime.now())
            if self.services[s]:
                self.score += s.points
        self.log()

    def log(self):
        '''
        Save self to log.
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
    Represents a network service that teams should implement.
    '''
    def status(self):
        '''
        Get the current status of service.
        '''
        if RANDOMIZE:
            return random.choice((True, False))
        return self._status()
        
class URL(Service):
    '''
    A service that checks the owner of a URL.
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
        
        Reads the specified 'url' and searches for 'teamname'.
        '''
        try: page = client.getPage(self.url)
        except: return False
        # url should contain text like `NAME Team'
        regex = r'(\w+)\sTeam'
        match = re.search(regex, page, re.I)
        owner = match.group(1) if match else ''
        return self.teamname.upper() == owner.upper()
    
class SSH(Service):
    '''
    A service that checks whether an 'ssh' connection can be established.
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

# Wait time between updating scores
WAIT_TIME = 3.0

# Report random service status
RANDOMIZE = True

def main():
    '''
    Start the competition.
    '''
    # We only want one instance of the server
    try:
        with open("server.pid") as f:
            os.kill(int(f.read()), 9)
            print >>sys.stderr, "server: Killed previous instance"
    except Exception as e:
        print >>sys.stderr, "Warning: ", e
    with open("server.pid", 'w') as f:
        f.write(str(os.getpid()))

    # Update the teams
    while 1:
        for t in teams:
            t.update()
        time.sleep(WAIT_TIME)

if __name__ == '__main__':
    main()
