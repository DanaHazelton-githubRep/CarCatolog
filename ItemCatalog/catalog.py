# Import objects
from flask import (Flask,
    render_template,
    request,
    redirect,
    jsonify,
    url_for,
    flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_dbsu import Base, Category, Items, User
from flask import session as login_session
import datetime
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Flask Instance
app = Flask(__name__)

# Google Client_ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "PartyBarge Car Catalog Application"


# Connect to Databasecreate database session
engine = create_engine('sqlite:///catalog_dbsu.db')
Base.metadata.bind = engine
# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# OAUTH LOGIN
# Create anti-forgery state token:


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token:
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
            ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token#check
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
        print user_id
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("%s you are now logged in." % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    print h
    result = h.request(url, 'GET')[0]
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps
            ('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showCatalog'))
        flash("You are now logged out.")
        return response
    else:
        response = make_response(json.dumps
            ('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON query's for Catalog information:

@app.route('/catalog/<path:category_name>/item/JSON')
def categorieMenuJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(
        category=category).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Catalog Home:
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(Category.name.asc())
    items = session.query(Items).order_by(Items.date.desc())
    return render_template('catalog.html', categories=categories,
                           items=items)
 

# Show a category menu:
@app.route('/catalog/<path:category_name>/')
@app.route('/catalog/<path:category_name>/item/')
def showItem(category_name):
    categories = session.query(Category).order_by(Category.name.asc())
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category).all()
    if 'username' not in login_session :
        return render_template('publicitem.html', items=items,
            category=category, categories=categories)
    else:
        return render_template('item.html',
            items=items, category=category, 
            categories=categories)


# Create a new item:
@app.route('/catalog/<path:category_name>/item/new/',
    methods=['GET', 'POST'])
def newItem(category_name):
    # Check if User is logged in:
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(Category.name.asc())
    category = session.query(Category).filter_by(name=category_name).one()
    # Handle authorized user:
    if request.method == 'POST':
            newItem = Items(
                category= category,
                name=request.form['name'],
                date=datetime.datetime.now(),
                description=request.form['description'],
                user_id=login_session['user_id'])
            if request.form['name'] and request.form['description']:
                session.add(newItem)
                session.commit()
                flash('New %s Item Successfully Created' % (newItem.name))
                return redirect(url_for('showItem',
                    category_name=category_name,categories=categories))
            else:
                flash('Need both Year/Model and a Description.')
                return render_template('newItem.html',
                    category_name=category_name,categories=categories)
    else:
        return render_template('newItem.html', category_name=category_name,
            categories=categories)

# Item Description:
@app.route('/catalog/<path:category_name>/item/<path:item_name>/description/',
    methods=['GET', 'POST'])
def descItem(category_name,item_name):
    categories = session.query(Category).order_by(Category.name.asc())
    description= session.query(Items).filter_by(name=item_name).one()
    return render_template('description.html', item=description,
        categories=categories, category_name=category_name)       

# Edit a Catalog item:
@app.route('/catalog/<path:category_name>/item/<path:item_name>/edit',
    methods=['GET', 'POST'])
def editItem(category_name, item_name):
    # Check if User is logged in:
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(Category.name.asc()) 
    editedItem = session.query(Items).filter_by(name=item_name).one()
    category = session.query(Category).all()
    # Compare Item creator with logged in User:
    creator = getUserInfo(editedItem.user_id)
    user = getUserInfo(login_session['user_id'])
    #Handle Logged in user if not Item creator:
    if creator.id != login_session['user_id']:
        flash('This Item was created by %s you can not Edit the Item!'
            % creator.name)
        return redirect(url_for('showCatalog'))
    # Handle authorized user:
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('You have edited your Item')
        return redirect(url_for('showItem', category_name=category_name,
            categories=categories))
    else:
        return render_template('editItem.html', category_name=category_name,
            item_name=item_name, item=editedItem, categories=categories)


# Delete a item
@app.route('/catalog/<path:category_name>/item/<path:item_name>/delete',
    methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    # Check if User is logged in:
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(Category.name.asc())
    category = session.query(Category).all
    itemToDelete = session.query(Items).filter_by(name=item_name).one()

    # Compare Item creator with logged in User:
    creator = getUserInfo(itemToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    # Handle Logged in user if not Item creator:
    if creator.id != login_session['user_id']:
        flash('This Item was created by %s you can not Delete the Item!'
            % creator.name)
        return redirect(url_for('showCatalog'))
    # Handle authorized user:
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item has been Successfully Deleted')
        return redirect(url_for('showItem',
            category_name=category_name, categories=categories))
    else:
        return render_template('deleteItem.html',
            item=itemToDelete, categories=categories)

# Code must be placed at the end of every Flask File:
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)