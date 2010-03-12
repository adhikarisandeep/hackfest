#!/bin/bash

# Start the scoring server in the background
python server.py &

# Start the web server
twistd -ny twistd.tac

cat <<EOF
The twisted server has stopped but the scoring server may still be running.
EOF
