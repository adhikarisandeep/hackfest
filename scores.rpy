'''
HTTP resource for getting the current scores for the competing teams.

This is not a regular Python file.  It is by twisted to provide a 
URL resource. More information can be found at
http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html
'''

from twisted.web import resource
import hackfest

class CurrentScores(resource.Resource):
    '''
    URL resource to get the current scores.
    '''
    def __init__(self, teams):
        self.teams = teams

    def render_GET(self, request):
        '''
        Get the current scores as JSON.
        
        This is called when the url to this file is requested
        via a http GET request.
        '''
        teamsjs = []
        for t in teams.teams:
            teamsjs.append(t.json() + '\n')
        s = '[' + ', '.join(teamsjs) + ']'
        return s

hackfest.start_hackfest()
resource = CurrentScores(hackfest.teams)
