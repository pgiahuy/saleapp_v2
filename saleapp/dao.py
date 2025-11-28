import hashlib
import json

from saleapp import app,db
from saleapp.models import Product, Category, User


def load_categories():
    return Category.query.all()


def load_products(cate_id=None,kw=None, page=None):
    query = Product.query
    if cate_id:
        query = query.filter(Product.cate_id == cate_id)
    if kw:
        query = query.filter(Product.name.contains(kw))
    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page)-1)*size
        query = query.slice(start,start+size)

    return query.all()

def get_product_byId(id):
    return Product.query.get(id)

def count_products():
    return Product.query.count()

def auth_user(username,password):
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def add_user(name, username, password, avatar):

    password=hashlib.md5(password.encode("utf-8")).hexdigest()

    u = User(name=name,username=username,password=password,avatar=avatar)
    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)

