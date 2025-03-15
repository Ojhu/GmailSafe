import cherrypy
from controller.login import LoginController
from controller.reg import RegController
import os

WEB_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'File',
        'tools.sessions.storage_path': os.path.join(WEB_ROOT, 'sessions'),
        'tools.sessions.timeout': 10
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(WEB_ROOT, 'static')
    },
    '/template': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(WEB_ROOT, 'template' ),
    }
}

if __name__ == '__main__':
    cherrypy.tree.mount(LoginController(), '/', config=conf)
    cherrypy.tree.mount(RegController(), '/register', config=conf)

    cherrypy.server.socket_port = 8088
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
