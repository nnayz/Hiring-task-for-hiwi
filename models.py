from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Threads(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    comments = relationship('Comments', back_populates='thread', cascade='all, delete-orphan')

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    # Create a link between the data in two tables. points to the id column in the threads table
    thread_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
    thread = relationship("Threads", back_populates="comments")