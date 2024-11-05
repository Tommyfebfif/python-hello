from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import psycopg2

def home_view(request):
    engine = create_engine("postgresql://testu:testp@testhost:5432/testd")
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.execute("SELECT * FROM your_table")
    rows = result.fetchall()

    html = "<html><body>"
    for row in rows:
        html += f"<p>{row}</p>"
    html += "</body></html>"
    return Response(html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(home_view, route_name='home')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
