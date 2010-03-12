#!/bin/bash

# Start the scoring server in the background
python server.py &

# Start the web server (does not run in background)
twistd -ny twistd.tac

# After web server stops, kill the scoring server
kill `cat server.pid` && rm server.pid
