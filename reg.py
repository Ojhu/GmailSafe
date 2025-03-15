import cherrypy
import os
from model import db_queries
from genshi.template import TemplateLoader
import re

WEB_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def has_logged():
    return "username" in cherrypy.session

class RegController:
    def __init__(self):
        self.loader = TemplateLoader(os.path.join(WEB_ROOT, 'template'), auto_reload=True)
        db_queries.create_table()
    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @cherrypy.expose
    def index(self):
        return open(os.path.join(WEB_ROOT, 'template'/ 'reg.html')).read()
       
    @cherrypy.expose
    def do_register(self, **params):
        user_details = {
            'Full_Name': params.get('full_name', 'N/A'),
            'Username': params.get('username', 'N/A'),
            'Email': params.get('email', 'N/A'),
            'Phone_Number': params.get('phone_number', 'N/A'),
            'Password': params.get('password', 'N/A'),
            'Gender': params.get('gender', 'N/A')
        }

        if not self.validate_password(user_details['Password']):
            return "Password must be at least 8 characters long, include one uppercase letter, one number, and one special character."

        db_queries.insert_user(user_details)
        tmpl = self.loader.load('result.html')
        stream = tmpl.generate(user=user_details)
        return stream.render('html', doctype='html')
