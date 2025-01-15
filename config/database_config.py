from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity.cadastro_entity import Base

from utils.common_imports import *


engine = create_engine('sqlite:///cadastros.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
