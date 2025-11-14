import json

from sqlalchemy import Boolean, Enum, String, Integer, Column, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from saleapp import db, app
from datetime import datetime
from enum import Enum as RoleEnum
from flask_login import UserMixin

class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime,default= datetime.now())

    def __str__(self):
        return self.name

class User(Base,UserMixin):
    username = Column(String(150), nullable=False ,unique=True)
    password = Column(String(150), nullable = False)
    avatar = Column(String(300), default="https://icons.iconarchive.com/icons/papirus-team/papirus-status/256/avatar-default-icon.png")
    user_role = Column(Enum(UserRole), default= UserRole.USER)

class Category(Base):
    products = relationship("Product", backref="category", lazy=True)


class Product(Base):
    price = Column(Float, default=0.0)
    image = Column(String(300),default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__=="__main__":
    with app.app_context():
        # db.create_all()
        # with open("data/category.json", encoding="utf-8") as f:
        #     cates = json.load(f)
        #     for c in cates:
        #         db.session.add(Category(**c))
        #     db.session.commit()
        # with open("data/product.json", encoding="utf-8") as f:
        #     products = json.load(f)
        #     for p in products:
        #         db.session.add(Product(**p))
        #     db.session.commit()
        with open("data/user.json", encoding="utf-8") as f:
            users = json.load(f)
            for u in users:
                db.session.add(User(**u))
            db.session.commit()


