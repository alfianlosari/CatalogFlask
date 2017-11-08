from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Catalog, Base, CatalogItem

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(
    name='Alfian Lo',
    email='alfian@losari.org',
    picture='',
)
session.add(user1)
session.commit()

Soccer = Catalog(id="Soccer")
session.add(Soccer)
session.commit()

soccerItem = CatalogItem(
    id="Two shinguards",
    description="A Protector",
    catalog=Soccer,
    user_id=user1.id
)
session.add(soccerItem)
session.commit()

Basketball = Catalog(id="Basketball")
session.add(Basketball)
session.commit()

basketballItem = CatalogItem(
    id="Air Jordan XXIII",
    description="A Protector",
    catalog=Basketball,
    user_id=user1.id
)
session.add(basketballItem)
session.commit()

Baseball = Catalog(id="Baseball")
session.add(Baseball)
session.commit()

baseballItem = CatalogItem(
    id="Bat",
    description="A Protector",
    catalog=Baseball,
    user_id=user1.id
)
session.add(baseballItem)
session.commit()

Frisbee = Catalog(id="Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Catalog(id="Snowboarding")
session.add(Snowboarding)
session.commit()

snowboardingItem = CatalogItem(
    id="Snowboard",
    description="A Protector",
    catalog=Snowboarding,
    user_id=user1.id
)
session.add(soccerItem)
session.commit()

RockClimbing = Catalog(id="Rock Climbing")
session.add(RockClimbing)
session.commit()

Foosball = Catalog(id="Foosball")
session.add(Foosball)
session.commit()

Skating = Catalog(id="Skating")
session.add(Skating)
session.commit()

Hockey = Catalog(id="Hockey")
session.add(Hockey)
session.commit()

hockeyItem = CatalogItem(
    id="Stick",
    description="A Protector",
    catalog=Hockey,
    user_id=user1.id
)
session.add(hockeyItem)
session.commit()
