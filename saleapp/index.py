import math

from flask import render_template, request
from saleapp import app
import saleapp.dao as dao

@app.route("/")
def index():
    cate_id = request.args.get('cate_id')
    kw = request.args.get('kw')
    page = request.args.get('page')
    pages = math.ceil(dao.count_products()/app.config['PAGE_SIZE'])
    products = dao.load_products(cate_id=cate_id,kw=kw ,page=page)
    return render_template('index.html', products=products,pages=pages)

@app.route("/products/<int:id>")
def product_details(id):
    p = dao.get_product_byId(id)
    return render_template('product-details.html', p=p)

@app.context_processor
def common_adtributes():
    return {
        'cates': dao.load_categories()
    }

@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
