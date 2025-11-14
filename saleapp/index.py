import math
from flask import render_template, request
from werkzeug.utils import redirect
from flask_login import current_user,login_user,logout_user
from saleapp import app,login,admin
import dao
from saleapp.models import UserRole


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
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")
    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user =  dao.auth_user(username, password)

        if user:
            login_user(user)
            if user.user_role == UserRole.ADMIN:

                return redirect("/admin")
            else:
                return redirect("/")
        else:
            err_msg ="Username hoac password khong dung!!!"

    return render_template('login.html',err_msg=err_msg)

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
