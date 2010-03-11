'''
teams.py
========

This is the 
'''

import sys
import json
import random
import time
from datetime import datetime

from twisted.web import client

RANDOMIZE = True
EVENT_LOGFILE = open('events.log', 'w')

def logEvent(event):
    '''Log the given event.
    '''
    print >>EVENT_LOGFILE, event
    EVENT_LOGFILE.flush()

class Service(object):
    '''Represents a network service that teams should implement.
    '''
    def status(self):
        '''Get the current status of service.'''
        if RANDOMIZE:
            return random.choice((True, False))
        return self._status()
        
class URL(Service):
    '''A service that checks the owner of a URL.
    '''
    def __init__(self, teamname, url, points=1):
        '''Create a new URL service.
        
        Args:
         * 'teamname': Owner of 'url'
         * 'url': The URL to check.
         * 'points': The number of points this service is worth.
         '''
        self.teamname = teamname
        self.url = url
        self.points = points

    def _status(self):
        '''Get the current status of this service.
        
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
    '''A service that checks whether an 'ssh' connection can be established.
    '''
    def __init__(self, user, host, points=2):
        '''Create a new SSH service.
        '''
        self.user = user
        self.host = host
        self.points = points
        
    def _status(self):
        # TODO: Implement
        return True

class Team(object):
    '''Hackfest competitor.
    '''
    def __init__(self, name, services):
        '''Create a new team named 'name'.
        
        'services' indicate the services that should be checked for this team.
        '''
        self.name = name
        self.score = 0
        self.services = dict.fromkeys(services, False)
        self.time = None
        
    def update(self):
        '''
        Update the team's score by checking the status of its 'services'.
        '''
        for s in self.services:
            self.services[s] = s.status()
            self.time = str(datetime.now())
            if self.services[s]:
                self.score += s.points
        logEvent(self.json())

    def json(self):
        '''Get a JSON representation of the team.
        
        The returned form is useful for passing data to Javascript 
        via HTTP requests.
        '''
        servs = {}
        for s in self.services:
            servs[s.__class__.__name__] = self.services[s]
        team = vars(self).copy()
        team['services'] = servs
        return json.dumps(team)
