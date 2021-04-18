from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgres://pckeozibdtravb:6a2c35bdabeb4d3e20f20597d120574030fb8825c170f0ba8e72f4e12f6ddbb3@ec2-54-167-152-185.compute-1.amazonaws.com:5432/d51b3qfecq92df"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
Base.metadata.schema = "GameZone"