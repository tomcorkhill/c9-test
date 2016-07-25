from functools import wraps

import shopify
from flask import session, redirect, url_for, request, current_app

from .models import Shop
from ..extensions import db

import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)



def shopify_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging.debug("auth required decorator start")
        if "shopify_token" not in session:
            shop_url = request.args.get('shop')
            shopify.Session.setup(
                api_key=current_app.config['SHOPIFY_API_KEY'], 
                secret=current_app.config['SHOPIFY_SHARED_SECRET'])
            try:
                logging.debug("auth required decorator 1")
                shopify_session = shopify.Session.validate_params(request.args)
                    
                #logging.debug("*****found session:" + request.args)
            except Exception as ex:
                #logging.debug("exception: redirect to install" + str(ex))
                
                logging.debug("redirect to install as no session")
                return redirect(url_for('shopify_bp.install',_external=True, _scheme = 'https', **request.args))
            
            try:
                logging.debug("auth required decorator 2")
                shop = Shop.query.filter_by(shop=shop_url).one()
            except Exception as ex:
                
                logging.debug("error with finding shop" + str(ex))
                return redirect(url_for('shopify_bp.install', **request.args))

            session['shopify_token'] = shop.token
            session['shopify_url'] = shop_url
            session['shopify_id'] = shop.id

        else:
            logging.debug("shop in session")
           
            try:
                logging.debug("auth required decorator 3")
               
                ''' Shop.query.filter_by(shop= session['shopify_url']).delete()
                '''
                
                logging.debug("dec 3.1")
                
                ''' TODO: There is an issue whereby multiple shops get
                added to the database, so this returns more than one record
                which triggers an exception and redirects to intallation
                shop = Shop.query.filter_by(shop=session['shopify_url']).one()
                
                termporily changed to just get the first record.
                '''
                
                shop = Shop.query.filter_by(shop=session['shopify_url']).one()
                
               
            except Exception as ex:
                logging.debug("auth required decorator 4")
                logging.debug((str(ex)))
                
                logging.debug(session['shopify_url'])
               
                shop = session['shopify_url']
                
                session.pop("shopify_token")
                session.pop("shopify_url")
                session.pop("shopify_id")
                
                """
                    need to get shopify shop name if url is none
                """
                #logging.debug(str(**request.args))
                #logging.debug(session.pop["shopify_url"])
                
                #return redirect(url_for('shopify_bp.install', _external=True, _scheme = 'https',**request.args))
                return redirect(url_for('shopify_bp.install',**request.args))

        return f(*args, **kwargs)
    
    return decorated_function