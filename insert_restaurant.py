import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session=DBSession()
restaurantObj=Restaurant(name=str(sys.argv[1]))
session.add(restaurantObj)
session.commit()
session.query(Restaurant).all()
