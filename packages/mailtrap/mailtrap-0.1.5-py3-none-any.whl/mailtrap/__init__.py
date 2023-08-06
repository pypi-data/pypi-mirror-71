import asyncore

import gevent
from gevent.event import Event
from logbook import Logger
from socketio.server import SocketIOServer

from mailtrap.db import connect, disconnect, create_tables
from mailtrap.smtp import smtp_handler, SMTPServer
from mailtrap.web import app


log = Logger(__name__)
stopper = Event()
socketio_server = None


def start(http_host, http_port, smtp_host, smtp_port, smtp_auth, db_path=None, debug=False):
    global socketio_server
    # Webserver
    log.notice('Starting web server on http://%s:%s' % (http_host, http_port))
    socketio_server = SocketIOServer((http_host, http_port), app,
                                     log='default' if app.debug else None)
    socketio_server.start()
    # SMTP server
    log.notice('Starting smtp server on %s:%s' % (smtp_host, smtp_port))
    if smtp_auth:
        log.notice('Enabled SMTP authorization with htpasswd file %s' % smtp_auth.path)
    SMTPServer((smtp_host, smtp_port), smtp_handler, smtp_auth, debug)
    gevent.spawn(asyncore.loop)
    # Database
    connect(db_path)
    create_tables()
    # Wait....
    try:
        stopper.wait()
    except KeyboardInterrupt:
        print()
    else:
        log.debug('Received stop signal')
    # Clean up
    disconnect()
    log.notice('Terminating')


def stop():
    stopper.set()
