from sqlalchemy import Column, Integer, String, Text
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String)
    result = Column(Text)