from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from catalog_dbsu import Category, Base, Items, User
 
engine = create_engine('sqlite:///catalog_dbsu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Steve McQueen", email="Bullit@haulin.com",
             picture='https://steveMcQuenn.com/profile_images/1234567890/19ebdyrtlitn_200x200.png')
session.add(User1)
session.commit()

User2 = User(name="Dale Jr", email="dj@budwieser.net",
             picture='https://dj@budwieser.net/profile_images/2671170543/iamfasterthanyou123_400x400.png')
session.add(User2)
session.commit()


#categories
cat1 = Category(name = "Ford")

session.add(cat1)
session.commit()

cat2 = Category(name = "Chevy")

session.add(cat2)
session.commit()

cat3 = Category(name = "Dodge")

session.add(cat3)
session.commit()

cat4 = Category(name = "Pontiac")

session.add(cat4)
session.commit()

cat5 = Category(name = "Oldsmobile")

session.add(cat5)
session.commit()

cat6 = Category(name = "Jeep")

session.add(cat6)
session.commit()

cat7 = Category(name = "Plymouth")

session.add(cat7)
session.commit()

cat8 = Category(name = "Mercury")

session.add(cat8)
session.commit()

cat9 = Category(name = "AMC")

session.add(cat9)
session.commit()

cat10 = Category(name = "Buick")

session.add(cat10)
session.commit()

Item2 = Items(name = "1969 Cheverlet Camaro",
			  description = "The 1969 Camaro carried over the previous year's drivetrain and major mechanical components," 
			  "but all-new sheetmetal, except the hood and trunk lid, gave the car a substantially sportier look."
			  "The grille was redesigned with a heavy V cant and deeply inset headlights. New door skins, rear quarter panels,"
			  "and rear valance panel also gave the car a much lower, wider, more aggressive look. This styling would serve for the"
			  "1969 model year only. Collectors often debate the merits of smooth, rounded lines of 1967 and 1968 model versus the"
			  "heavily creased and sportier looks of the 1969.",
			  category_id = 2,
			  date = datetime.datetime.now(),
			  user_id = 2)

session.add(Item2)
session.commit


Item1 = Items(name = "1964 Mustang",
			  description = "Since it was introduced four months before the normal start of the 1965 production year and manufactured"
			  "alongside 1964 Ford Falcons and 1964 Mercury Comets, the earliest Mustangs are widely referred to as the 1964 and a half model.[19]"
			  "Nevertheless, all 1964 and a half cars were given 1965 U.S. standard VINs at the time of production, and - with limited exception "
			  "to the earliest of promotional materials[20] - were marketed by Ford as 1965 models.[21] The low-end model hardtop used" 
			  "a U-code 170 cu in (2.8 L) straight-6 engine[22] borrowed from the Falcon, as well as a three-speed manual transmission "
			  "and retailed for US$2,368. Standard equipment for the early 1965 Mustangs included black front seat belts, a glove box "
			  "light, and a padded dash board.[23] Production began in March 1964 and official introduction following on April 17 at the"
			  "1964 World's Fair. V8 models got a badge on the front fender that spelled out the engine's cubic inch displacement "
			  "(260 or 289) over a wide V. This emblem was identical to the one on the 1964 Fairlane.",
			  category_id = 1,
			  date = datetime.datetime.now(),
			  user_id = 1)

session.add(Item1)
session.commit()



print "added items!"