import os

class DefaultConfig(object):

    PROJECT = "Hello Shopify"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True
    TESTING = False

    IP = os.getenv('IP', '127.0.0.1')
    PORT = int( os.getenv('PORT', 8000))
    # app.run(port=port,host=host)
    
    SECRET_KEY = 'secret key'

    #SERVER_NAME =  os.getenv('IP', '0.0.0.0') + ":8082"
    PREFERRED_URL_SCHEME = 'https'

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/helloshopify.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    SHOPIFY_API_KEY = 'd07123086349e90cbf615cb52da784cc'
    SHOPIFY_SHARED_SECRET = '9ba2a3d8d8b082ce4c5575677ca00f12'