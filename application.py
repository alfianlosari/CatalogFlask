#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/')
def showMain():
    catalogs = session.query(Catalog).all()
    items = session.query(CatalogItem).all()
    return render_template('root.html', catalogs=catalogs, items=items, login_session=login_session)


@app.route('/googleLogin', methods=['POST'])
def googleLogin():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".format(access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode())
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error ')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's Client ID does not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url,params=params)
    data = answer.json()

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 300px; height:300px;border-radius:150px;">'
    flash("You are now logged in as {}".format(login_session['username']))
    return output


@app.route('/googleLogout')
def googleLogout():
    access_token = login_session.get('access_token')
    if access_token is None:
        return redirect(url_for('showMain'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    if result['status'] == '200':
        return redirect(url_for('showMain'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/<string:id>/items/')
def showCatalogItems(id):
    catalogs = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(id=id).one()
    items = session.query(CatalogItem).filter_by(catalog_id=catalog.id).all()
    return render_template('catalogItems.html', catalogs=catalogs, catalog=catalog, items=items, login_session=login_session)


@app.route('/catalog/<string:catalog_id>/item/<string:item_id>/')
def showCatalogItem(catalog_id, item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return render_template('item.html', item=item, login_session=login_session)


@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def newCatalogItem():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        id = request.form['name']
        description = request.form['description']
        catalog_id = request.form['catalog']
        catalog = session.query(Catalog).filter_by(id=catalog_id).one()
        newItem = CatalogItem(id=id, description=description, catalog=catalog)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalogItems', id=catalog_id))
    else:
        catalogs = session.query(Catalog).all()
        return render_template('newCatalogItem.html', catalogs=catalogs, login_session=login_session)


@app.route('/catalog/<string:catalog_id>/item/<string:item_id>/edit/', methods=['GET', 'POST'])
def editCatalogItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.id = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['catalog']:
            catalog = session.query(Catalog).filter_by(id=request.form['catalog']).one()
            item.catalog = catalog
        session.add(item)
        session.commit()
        return redirect(url_for('showCatalogItems', id=item.catalog.id))
    else:
        catalogs = session.query(Catalog).all()
        return render_template('editCatalogItem.html', item=item, catalogs=catalogs, login_session=login_session)


@app.route('/catalog/<string:catalog_id>/item/<string:item_id>/delete/', methods=['GET', 'POST'])
def deleteCatalogItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')

    item = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showCatalogItems', id=catalog_id))
    else:
        return render_template('deleteCatalogItem.html', item=item, login_session=login_session)


@app.route('/catalogs/JSON')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(categories=[c.serialize for c in catalogs])


@app.route('/catalog/<string:catalog_id>/item/<string:item_id>/JSON')
def catalogItemJSON(catalog_id, item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
