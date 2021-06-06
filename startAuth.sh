#!/bin/bash
port="$1";
port2="$2";
if [ $# -eq 0 ]
  then
    echo "startAuth.sh: No port numbers given, using defaults..."
    port="1024";
    port2="1025";
fi

# Starting flask
export FLASK_APP="auth/auth.py";
gnome-terminal -- flask run --host=0.0.0.0 --port=$port2;

# Starting java
javac SpotiGUI/*.java;
java SpotiGUI/SpotiGUI $port;