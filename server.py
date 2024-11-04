from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

def connectingPG(request):
    try:
        PGengine = create_engine('postgresql://user:password@host:port/database')
        pgSession = sessionmaker(bind=PGengine)
        session = pgSession()
        fetresult = session.execute('SELECT * FROM your_table').fetchall()
        session.close()
        # return fetresult
        return Response("aaa")
    except Exception as e:
        logging.info("DB Error.")

def hello_world(request):
    name = os.environ.get('NAME')
    if name == None or len(name) == 0:
        name = "world"
    message = "Hello, " + name + "!\n"

    pgdata = connectingPG()
    logging.info(pgdata)
    
    return Response(message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        config.add_route('hellopg', '/pg')
        config.add_view(connectingPG, route_name='hellopg')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
