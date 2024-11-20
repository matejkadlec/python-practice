from sqlalchemy import ForeignKey, Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    # Table name
    __tablename__ = "user"

    # Table columns
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    # CheckConstraint could be added for this column, but it's not needed as it's checked elsewhere
    email = Column(String(100), unique=True)
    created_at = Column(TIMESTAMP)

    # Table relationships
    order = relationship("Order", back_populates="user")


class Product(Base):
    # Table name
    __tablename__ = "product"

    # Table columns
    id = Column(Integer, primary_key=True)
    name = Column(String(200), index=True)
    price = Column(DECIMAL(10, 2))
    description = Column(Text)
    created_at = Column(TIMESTAMP)

    # Table relationships
    order_product = relationship("OrderProduct", back_populates="product")


class Order(Base):
    # Table name
    __tablename__ = "order"

    # Table columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    total_amount = Column(DECIMAL(10, 2))
    order_date = Column(TIMESTAMP)
    # CheckConstraint could be added for this column, but it's not needed as it's checked elsewhere
    status = Column(String(10), default='CREATED', index=True)

    # Table relationships
    user = relationship("User", back_populates="order")
    order_product = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    # Table name
    __tablename__ = "order_product"

    # Table columns
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)

    # Table relationships
    order = relationship("Order", back_populates="order_product")
    product = relationship("Product", back_populates="order_product")
