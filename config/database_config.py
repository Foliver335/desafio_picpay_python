from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity.cadastro_entity import Base

engine = create_engine('postgresql://postgres:root@localhost/crud_aws', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
