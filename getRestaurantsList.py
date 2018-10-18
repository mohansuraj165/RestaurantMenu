from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItems

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurantList = session.query(Restaurant).all()
for restaurant in restaurantList:
	print(restaurant.name, restaurant.id)
	items = session.query(MenuItems).filter_by(id=restaurant.id)
	for item in items:
		print(item.name)
		
	print("  ")
	
