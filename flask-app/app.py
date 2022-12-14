###
# Main application interface
###

# import the create app function 
# that lives in src/__init__.py
from src import create_app
from session import session

# create the app object
app = create_app()

if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    session["buyerID"] = 1
    session["sellerID"] = 7

    #Since no login screen, hardcoded replacement values for session info
    session["adminID"] = 1
    app.run(debug = True, host = '0.0.0.0', port = 4000)