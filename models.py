from sqlalchemy import Column, Integer, String
from database import Base

class TrackedItem(Base):
    __tablename__ = "tracked_items" 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    status = Column(String)
    notes = Column(String, nullable=True)