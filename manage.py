import os
from flask_script import Manager, Server

from smartstock import create_app
from smartstock.extensions import db
from smartstock import config



manager = Manager(create_app)
host = os.getenv('IP', '0.0.0.0')
port = int( os.getenv('PORT', 8080))

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=host,
    port=port,
    ssl_context='adhoc'))


@manager.command
def run_debug():
    """run app in debug mode using adhoc ssl. 
    Make sure that in production you have valid certs.
    """
    host = os.getenv('IP', '127.0.0.1')
    port = int(os.getenv('PORT', 8000))

    app = create_app(config.DefaultConfig)
    app.run(debug=True, host=host,  port =port, ssl_context='adhoc')

    
    """ host = os.getenv('IP', '0.0.0.0')
    port = int( os.getenv('PORT', 8000))
    app = create_app(config.DefaultConfig)
    app.run(port=port,host=host)
    """
    
    
    
@manager.command
def initdb():
    """ Initialize database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    
    ''' for some reason need to put the port etc here when running in cloud9.for
    need to remove if wanting to run commands such as initidb from python terminal
    '''

    host = os.getenv('IP', '127.0.0.1')
    port = int( os.getenv('PORT', 8000))
    app = create_app(config.DefaultConfig)
   
    app.run(port=port,host=host)

    app.debug = True


    manager.run()
    
   