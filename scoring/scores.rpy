'''
HTTP resource for getting the current scores for the competing teams.
'''

# NB: This is not a regular Python file.
# It used is by twisted to provide a URL resource.
# http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html

from twisted.web import resource
import server
import glob

class CurrentScores(resource.Resource):
    '''
    URL resource to get the current scores.
    '''    
    def render_GET(self, request):
        '''
	Get the current scores as JSON.
        
        This is called when the url to this file is requested
        via a http GET request.
        '''
        # Each team's score is at `logs/TEAM/current-score'
        scores = glob.glob("logs/*/current-score")
        if not scores:
            return None
        # Read the scores and convert to JSON
        teamsjs = []        
        for s in scores:
            teamsjs.append(open(s).read())
        return '[' + ','.join(teamsjs) + ']'

resource = CurrentScores()
