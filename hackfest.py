from twisted.internet import task
from twisted.internet import reactor

# The hackfest competitors
TEAMS = [
    Team('red', (
            URL('red', 'localhost'),
            SSH('whitey', 'localhost'),
            )),
    Team('blue', (
            URL('blue', 'localhost'),
            SSH('whitey', 'localhost'),
            )),
    ]


WAIT_TIME = 3.0               # Wait time between updating scores

def startHackfest():
    '''
    Start the competition.
    '''
    def updateTeams():
        for t in TEAMS:
            t.update()
    l = task.LoopingCall(updateTeams)
    l.start(UPDATE_TIME)
