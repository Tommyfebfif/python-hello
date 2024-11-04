from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import getLogger
import os

def connectingPG():
    try:
        PGengine = create_engine('postgresql://user:password@host:port/database')
        pgSession = sessionmaker(bind=PGengine)
        session = pgSession()
        fetresult = session.execute('SELECT * FROM your_table').fetchall()
        session.close()
    except Exception as e:
        logging.exception(e)

def hello_world(request):
    name = os.environ.get('NAME')
    if name == None or len(name) == 0:
        name = "world"
    message = "Hello, " + name + "!\n"

    connectingPG()
    
    return Response(message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
