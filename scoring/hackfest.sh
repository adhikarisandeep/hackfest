#!/bin/bash

# Start the scoring server
python server.py &

# Start the web server
twistd -ny twistd.tac
