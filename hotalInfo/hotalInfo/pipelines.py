# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from itemadapter import ItemAdapter


# load_dotenv()

# # Database setup
# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in the .env file")

# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
# session = Session()
# Base = declarative_base()

# class Hotel(Base):
#     __tablename__ = 'hotels'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     hotelId = Column(String)
#     hotelName = Column(String)
#     lat = Column(Float)
#     lon = Column(Float)
#     brief = Column(String)
#     imgUrl = Column(String)  
#     cityName = Column(String)
#     fullAddress = Column(String)
#     hotelFacilityList = Column(JSON)

# # Create the table
# Base.metadata.create_all(engine)

# class HotelPipeline:
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         hotel = Hotel(
#             hotelId=adapter.get('hotelId'),
#             hotelName=adapter.get('hotelName'),
#             lat=adapter.get('lat'),
#             lon=adapter.get('lon'),
#             brief=adapter.get('brief'),
#             imgUrl=adapter.get('imgUrl'),  # This is now the file path
#             cityName=adapter.get('cityName'),
#             fullAddress=adapter.get('fullAddress'),
#             hotelFacilityList=adapter.get('hotelFacilityList')
#         )
#         session.add(hotel)
#         session.commit()
#         return item


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from itemadapter import ItemAdapter
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotelId = Column(String, unique=True)
    hotelName = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    brief = Column(String)
    imgUrl = Column(String)
    cityName = Column(String)
    fullAddress = Column(String)
    hotelFacilityList = Column(JSON)

# Create the table
Base.metadata.create_all(engine)

class HotelPipeline:
    def __init__(self):
        self.session = None

    def open_spider(self, spider):
        self.session = SessionLocal()

    def close_spider(self, spider):
        if self.session:
            self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        try:
            hotel_id = str(adapter.get('hotelId'))  # Convert hotelId to string
            
            # Check if the hotel already exists in the database
            existing_hotel = self.session.query(Hotel).filter_by(hotelId=hotel_id).first()
            
            if existing_hotel is None:
                # If the hotel doesn't exist, add it to the database
                hotel = Hotel(
                    hotelId=hotel_id,
                    hotelName=adapter.get('hotelName'),
                    lat=adapter.get('lat'),
                    lon=adapter.get('lon'),
                    brief=adapter.get('brief'),
                    imgUrl=adapter.get('imgUrl'),
                    cityName=adapter.get('cityName'),
                    fullAddress=adapter.get('fullAddress'),
                    hotelFacilityList=adapter.get('hotelFacilityList')
                )
                self.session.add(hotel)
                self.session.commit()
                print(f"Added new hotel: {adapter.get('hotelName')}")
            else:
                print(f"Hotel already exists: {adapter.get('hotelName')}")
        
        except SQLAlchemyError as e:
            # If an error occurs, rollback the session
            self.session.rollback()
            print(f"Error processing hotel {adapter.get('hotelName')}: {str(e)}")
        
        return item

