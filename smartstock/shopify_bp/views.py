import pprint

import shopify
from flask import (
    Blueprint, render_template, current_app, request, redirect, session,
    url_for)

from .models import Shop
from .decorators import shopify_auth_required
from ..extensions import db

import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)




shopify_bp = Blueprint('shopify_bp', __name__, url_prefix='/shopify')

@shopify_bp.route('/')
@shopify_auth_required
def index():
    """ Render the index page of our application.

    """
   
    if request.args.get('shop'):
        session['shop_url'] = request.args.get('shop')
        # And then redirect the user to the main page
       # logging.debug(session['shop'])
       
    else:
        logging.debug("no shop url")
        
    
    logging.debug('index requested')
    ss = shopify.Session(session['shopify_url'], session['shopify_token'] )
    shopify.ShopifyResource.activate_session(ss)
    """
    # Create a new product
    new_product = shopify.Product()
    new_product.title = "Burton Custom Freestyle 151"
    new_product.product_type = "Snowboard"
    new_product.vendor = "Burton"
    success = new_product.save() #returns false if the record is invalid
    """
    
    products = shopify.Product.find()
    """
    for item in products:
        logging.debug(item.title)
        item.title = 'Tom a'
        success = item.save()
        break
        
        if not success:
            logging.debug("item did not save")
    """    
    shop = shopify.Shop.current
    
    
    names=(o.title for o in products)
 
 
    return render_template('shopify_bp/debug.html', name = names)

@shopify_bp.route('/install')
def install():
    """ Redirect user to permission authorization page.

    """
    shop_url = "no-url-here-tc"
    
    if request.args.get('shop'):
        logging.debug("shop in args add to session")
       
        shop_url = request.args.get('shop')
    
    if request.args.get('shop_url'):
        logging.debug("shop_url in args add to session")
       
        shop_url = request.args.get('shopify_url')
        
    
    logging.debug('install called x')

    
#    Shop.query.filter_by(shop= shop_url).delete()
    logging.debug("installing url" + shop_url)
    
    """ There is an issue here. Shop can be None as not in session,
        This is not checked by the decorators.py function
    
    
    """
    
    #logging.debug('shop_url ' +  shop_url)
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])

    session = shopify.Session(shop_url)

    scope=[
        "write_products", "read_products", "read_script_tags", 
        "write_script_tags"]
    permission_url = session.create_permission_url(
        scope, url_for("shopify_bp.finalize", _external=True, _scheme='https'))

    logging.debug("generated permission url:" + permission_url)
    return render_template(
        'shopify_bp/install.html', permission_url=permission_url)

    
@shopify_bp.route('/finalize')
def finalize():
    """ Generate shop token and store the shop information.
    
    """
    
    logging.debug("finalising shop install")
    
    shop_url = request.args.get("shop")
    
    print("This is the shop url found:" + shop_url)
    
    shopify.Session.setup(
        api_key=current_app.config['SHOPIFY_API_KEY'], 
        secret=current_app.config['SHOPIFY_SHARED_SECRET'])
    shopify_session = shopify.Session(shop_url)

    token = shopify_session.request_token(request.args)
    logging.debug("adding shop")
    
    shop = Shop(shop=shop_url, token=token)
    
    
    db.session.add(shop)
    db.session.commit()
    logging.debug("commit shop")
    session['shopify_url'] = shop_url
    session['shopify_token'] = token
    session['shopify_id'] = shop.id

    logging.debug("going to redirext to 99888>>>> :" + url_for('shopify_bp.index'))

    #return redirect(url_for('shopify_bp.index', _external=True,_scheme='https'))
    return redirect(url_for('shopify_bp.index'))