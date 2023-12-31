__version__='1.0.8'
__author__='Ioannis Tsakmakis'
__date_created__='2023-10-20'
__last_updated__='2023-11-30'

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os, json, logging

local_directory = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(local_directory, 'mysql_config.json')

with open(config_path,'r') as f:
    config = json.load(f)

# sqlalchemy logging path
logging_path = config['sqlalchemy_logging_path']

# Creating sqlalchemy engine
engine = create_engine(url=f'{config["DBAPI"]}://{config["username"]}:{config['password']}@{config["host-ip"]}/{config["database"]}',
                         pool_size=30, max_overflow=5, pool_recycle=7200)


SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
