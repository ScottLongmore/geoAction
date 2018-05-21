"""
run.py - run geoAction/polyAction Flask service
"""
from geoAction import app

app.run(debug=True, port=5000)  # Run app in debug mode on port 5000
