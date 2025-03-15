import cherrypy
import sys
import os

# Add the Webapp directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from auth and db_queries
from auth import authenticate_and_generate_token
from model import db_queries
from model.db_queries import get_user_by_email

# Determine the root of the web application
WEB_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Helper function to check if the user is logged in
def has_logged():
    return "username" in cherrypy.session

class LoginController:

    @cherrypy.expose
    def index(self, code=None, scope=None, state=None):
        """
        Handle login and display the login page.
        If 'code', 'scope', or 'state' parameters are provided, process them.
        """
        if has_logged():
            raise cherrypy.HTTPRedirect("/home")
        
        oauth_success = cherrypy.session.pop("oauth_success", None)
        login_page = os.path.join(WEB_ROOT, 'template', 'login.html')
        
        # Read the login HTML file
        with open(login_page, 'r') as file:
            page_content = file.read()
        
        # If query string parameters exist, log them or handle OAuth response
        if code or scope or state:
            cherrypy.log(f"Received OAuth callback parameters: code={code}, scope={scope}, state={state}")
            # Additional logic to handle 'code' (e.g., exchange it for a token) can go here
        
        # Add a message if OAuth was successful
        if oauth_success:
            page_content += "<p>OAuth completed successfully. You can now log in.</p>"
        
        return page_content

    @cherrypy.expose
    def do_login(self, gmail=None):
        if has_logged():
            raise cherrypy.HTTPRedirect("/home")

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", gmail)

        # Authenticate the user
        user = db_queries.get_user_by_email(gmail)

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", user)
        if user:
            print(">>>", 1)
            cherrypy.session["username"] = gmail

            try:
                # Perform OAuth authentication
                oauth_status = authenticate_and_generate_token()
                print(">>>>>>>>>>>", 2)
                if not oauth_status:
                    return "Error during OAuth authentication. Please try again."
            except Exception as e:
                import traceback
                traceback.print_exc()
                return f"Error during authentication: {e} <a href='/'>Try again</a>"
            
            cherrypy.session["oauth_success"] = True
            # Redirect to the home page after successful login
            raise cherrypy.HTTPRedirect("/home")
        else:
            return "Login failed. Please try again. <a href='/'>Login here</a>"

    @cherrypy.expose
    def home(self):
        if not has_logged():
            raise cherrypy.HTTPRedirect("/")
        return """
        <h1>Login successful!</h1>
        <a href='/do_logout'>Logout</a>
        """

    @cherrypy.expose
    def do_logout(self):
        if not has_logged():
            raise cherrypy.HTTPRedirect("/")
        del cherrypy.session["username"]
        return "Logged out successfully!"

# CherryPy application configuration
if __name__ == "__main__":
    cherrypy.quickstart(LoginController(), '/', {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': WEB_ROOT
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    })

