#!/bin/bash

# If aditional arg exists, use it as the port number of the login page
authPort="$1";
if [ $# -eq 0 ]
  then
    echo "startAuth.sh: No port numbers given, using defaults..."
    authPort="1025";
fi

# Start flask in new terminal window
export FLASK_APP="auth/auth.py";
gnome-terminal -- python3 auth/auth.py $authPort;

# Start SpotiGUI
javac SpotiGUI/*.java;
java SpotiGUI/SpotiGUI;