#!/bin/bash
exec python -m gunicorn -b 0.0.0.0:5500 app:app
# exec will run as a new shell (guni becomes pid 1 - useful in a container)
# -b bind - means listen on all addresses and port 5500. 
# 0.0.0.0 important as localhost inside a container means not reachable from outside. 
# app:app == module:app-object so python file called app and runs a flask-app-object called app.
