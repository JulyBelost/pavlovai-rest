from sqlalchemy import Column, Integer, String, Float, Sequence
from db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence("seq1"), primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    def __init__(self, name, price):
        self.name = name
        self.price = price
