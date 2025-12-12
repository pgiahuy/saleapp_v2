import math

import cloudinary
import cloudinary.uploader
from flask import render_template, request, session, jsonify
from werkzeug.utils import redirect
from flask_login import current_user,login_user,logout_user
from saleapp import app, login, admin, db, utils
import dao
from saleapp.decorators import anonymous_required
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
        'cates': dao.load_categories(),
        'stats_cart': utils.count_cart(session.get('cart'))
    }

@app.route("/login",methods=['get','post'])
@anonymous_required
def login_my_user():
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

@app.route('/admin-login', methods=['post'])
def admin_login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username, password)

    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"


@app.route("/register",methods=['get','post'])
def register():
    err_msg=None
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password==confirm:
            username = request.form.get('username')
            name = request.form.get('name')
            avatar = request.files.get('avatar')
            file_path=None
            if avatar:
                upload_result = cloudinary.uploader.upload(avatar)
                file_path = upload_result["secure_url"]
            try:
                dao.add_user(name=name, username=username, password=password, avatar=file_path)
                return redirect("/login")
            except:
                db.session.rollback()
                err_msg = "Lỗi rồi khách ơi!"


        else:
            err_msg="Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/api/carts",methods=['POST'])
def add_to_cart():
    cart = session.get('cart')
    if not cart:
        cart ={}
    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['quantity']+=1
    else:
        cart[id]={
            "id":id,
            "name" :request.json.get('name'),
            "price" :request.json.get('price'),
            "quantity":1
        }
    session['cart']=cart

    print(session['cart'])

    return jsonify(utils.count_cart(cart=cart))

@app.route("/api/carts/<id>", methods=['put'])
def update_cart(id):
    cart = session.get('cart')

    if cart and  id in cart:
        cart[id]["quantity"] = int(request.json.get("quantity"))
        session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))

@app.route("/api/carts/<id>", methods=['delete'])
def delete_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart[id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))

if __name__ == "__main__":
    app.run(debug=True)
