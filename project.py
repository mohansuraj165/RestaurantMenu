#flask imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

#sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItems, Base
from sqlalchemy.pool import StaticPool

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool, echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Home page: List of restaurants
@app.route('/')
@app.route('/restaurant/')
def RestaurantHome():
    restaurantList = session.query(Restaurant)
    return render_template('restaurantHome.html', restaurantList = restaurantList)

#Restaurant menu: Displays menu items for a restaurant
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menuItems = session.query(MenuItems).filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html',restaurant=restaurant, items=menuItems)

#API for menu items in JSON
@app.route('/restaurant/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menuItems = session.query(MenuItems).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in menuItems])

#Create new restaurant
@app.route('/restaurant/new/',
           methods=['GET', 'POST'])
def addRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New restaurant created")
        return redirect(url_for('RestaurantHome'))
    else:
        return render_template('newRestaurant.html')


#Create new menu item
@app.route('/restaurant/<int:restaurant_id>/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
        if request.method == 'POST':
                newItem = MenuItems(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
                session.add(newItem)
                session.commit()
                flash("new menu item created!")
                return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
                return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItems).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Item has been edited")
                return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItems).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)


if __name__ == '__main__':
        app.secret_key = 'super_secret_key'
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
