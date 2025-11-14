import json

from sqlalchemy.orm import backref, relationship

from saleapp import db, app


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

class Category(Base):
    products = db.relationship("Product", backref="category", lazy=True)


class Product(Base):
    price = db.Column(db.Float, default=0.0)
    image = db.Column(db.String(300),default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    cate_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)


# if __name__=="__main__":
#     with app.app_context():
#         #db.create_all()
#         with open("data/category.json", encoding="utf-8") as f:
#             cates = json.load(f)
#             for c in cates:
#                 db.session.add(Category(**c))
#             db.session.commit()
#         with open("data/product.json", encoding="utf-8") as f:
#             products = json.load(f)
#             for p in products:
#                 db.session.add(Product(**p))
#             db.session.commit()


