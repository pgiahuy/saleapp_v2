import math

from flask import render_template, request
from werkzeug.utils import redirect

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

@app.route("/login",methods=['get','post'])
def login():
    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        if username=="user" and password=="123":
            return redirect('/')
        else:
            err_msg ="Username hoac password khong dung!!!"


    return render_template('login.html',err_msg=err_msg)


if __name__ == "__main__":
    app.run(debug=True)
