import os

class DefaultConfig(object):

    PROJECT = "Hello Shopify"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True
    TESTING = False

    IP = os.getenv('IP', '0.0.0.0')
    PORT = int( os.getenv('PORT', 8080))
    # app.run(port=port,host=host)
    
    SECRET_KEY = 'secret key'

    #SERVER_NAME =  os.getenv('IP', '0.0.0.0') + ":8082"
    PREFERRED_URL_SCHEME = 'https'

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/helloshopify.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    SHOPIFY_API_KEY = 'API_KEY_HERE'
    SHOPIFY_SHARED_SECRET = 'SHARED_SECRET'