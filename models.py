"""
from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cin = Column(Integer, index=True)
    username = Column(String, unique=True, index=True)
    lastname = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

class Vacation(Base):
    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(String)
    end_date = Column(String)
    reason = Column(String)

    user = relationship("User ", back_populates="vacations")

User.vacations = relationship("Vacation", back_populates="user")

"""

