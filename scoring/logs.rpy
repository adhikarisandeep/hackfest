'''
HTTP resource for browsing the logs.
'''

# NB: This is not a regular Python file.
# It used is by twisted to provide a URL resource.
# http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html

from twisted.web import resource
import glob

class LogGetter(resource.Resource):
    '''
    URL resource to get the current logs.
    '''    
    def render_GET(self, request):
        '''
	Get the current log files for each team as JSON.
        
        This is called when the url to this file is requested
        via a http GET request.
        '''
        # Each team's log files are at `logs/TEAM/'
	logs = glob.glob("logs/*/*")
        logs.sort(key=lambda f: f.rsplit("/")[-1])
        # Read the logs and convert to JSON
        teamsjs = []
        for l in logs:
            teamsjs.append(open(l).read())
        js = '[' + ','.join(teamsjs) + ']'
        return js

resource = LogGetter()
