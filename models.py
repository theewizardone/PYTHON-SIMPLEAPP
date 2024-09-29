"""
This module contains the database models for the customer and orders system.
It defines the ORM models using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    number = Column(String)

    

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    item = Column(String, index=True)
    amount = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")

Customer.orders = relationship("Order", back_populates="customer")

