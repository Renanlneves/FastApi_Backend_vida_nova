from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Blog(Base):
  id = Column(Integer, primary_key= True, index= True)
  title = Column(String)
  body = Column(String)