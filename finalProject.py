from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return "This page will show all of my restaurants"


@app.route('/restaurant/new')
def createRestaurant():
    return "This page will allow me to create a restaurant"



@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "This page will allow me to edit the restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "This page will allow me to delete restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "This page is the menu for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "This page is for creating a new menu item for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "This page is for editing menu item {} for restaurant {}".format(menu_id, restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "This page is for deleting menu item {} for restaurant {}".format(menu_id, restaurant_id)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)