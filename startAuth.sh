#!/bin/bash
authPort="$1";
if [ $# -eq 0 ]
  then
    echo "startAuth.sh: No port numbers given, using defaults..."
    authPort="1025";
fi

# Starting flask
export FLASK_APP="auth/auth.py";
gnome-terminal -- flask run --host=0.0.0.0 --port=$authPort;

# Starting java
javac SpotiGUI/*.java;
java SpotiGUI/SpotiGUI;