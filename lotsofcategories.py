from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

Soccer = Catalog(id="Soccer")
session.add(Soccer)
session.commit()

soccerItem = CatalogItem(id="Two shinguards", description="A Protector", catalog=Soccer)
session.add(soccerItem)
session.commit()

Basketball = Catalog(id="Basketball")
session.add(Basketball)
session.commit()

basketballItem = CatalogItem(id="Air Jordan XXIII", description="A Protector", catalog=Basketball)
session.add(basketballItem)
session.commit()

Baseball = Catalog(id="Baseball")
session.add(Baseball)
session.commit()

baseballItem = CatalogItem(id="Bat", description="A Protector", catalog=Baseball)
session.add(baseballItem)
session.commit()

Frisbee = Catalog(id="Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Catalog(id="Snowboarding")
session.add(Snowboarding)
session.commit()

snowboardingItem = CatalogItem(id="Snowboard", description="A Protector", catalog=Snowboarding)
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

hockeyItem = CatalogItem(id="Stick", description="A Protector", catalog=Hockey)
session.add(hockeyItem)
session.commit()
