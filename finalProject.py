from flask import Flask, render_template, request, redirect, url_for, flash, jsonify


# Import the following code to so that I am able to connect to the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create a database session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


################
#API END POINTS#
################

@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurant=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menuItemJSON(restaurant_id):
    
    targetItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in targetItems])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item>/JSON')
def specificMenuItemJSON(restaurant_id, menu_item):
    
    targetItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_item).one()
    return jsonify(MenuItem=[targetItems.serialize])



@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    #return "This page will show all of my restaurants"
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def createRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        print(newRestaurant)
        session.add(newRestaurant)
        session.commit()
        # Add flash message later
        #flash("New Menu Item Created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('createRestaurant.html')
    

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # Pull the object that I need straight out of the database
    restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
    
    if request.method == 'POST':
        if request.form['newname']:
            restaurantToEdit.name = request.form['newname']
            session.add(restaurantToEdit)
            session.commit()
        return redirect(url_for('showRestaurants'))
    #return "This page is for editing menu item {} for restaurant {}".format(menu_id, restaurant_id)
    else:
        #return "This page will allow me to edit the restaurant %s" % restaurant_id
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurantToEdit = restaurantToEdit)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))

    #return "This page will allow me to delete restaurant %s" % restaurant_id
    else:
        return render_template('deleteRestaurant.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    #return "This page is the menu for restaurant %s" % restaurant_id
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant_id = restaurant_id, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    print("HERE HERE HERE HERE")
    if request.method == 'POST':
        newMenuItem = MenuItem(name = request.form['name'], 
                                description = request.form['description'],
                                price = request.form['price'],
                                restaurant_id = restaurant_id)
        session.add(newMenuItem)
        session.commit()
        # Add flash message later
        #flash("New Menu Item Created")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        #return "This page is for creating a new menu item for restaurant %s" % restaurant_id
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menuItemToEdit.name = request.form['name']
        if request.form['description']:
            menuItemToEdit.description = request.form['description']
        if request.form['price']:
            menuItemToEdit.price = request.form['price']
        session.add(menuItemToEdit)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    #return "This page is for editing menu item {} for restaurant {}".format(menu_id, restaurant_id)
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, menuItemToEdit = menuItemToEdit)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    menuItemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(menuItemToDelete)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    #return "This page will allow me to delete restaurant %s" % restaurant_id
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id)
    

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)