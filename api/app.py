#import greplin.scales.flaskhandler as statserver

from finance import app

#TODO change this to push to stats server once setup
#statserver.serveInBackground(8765, serverName='finance')

app.run(debug=True)