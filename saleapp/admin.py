from flask import redirect, render_template
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import logout_user, current_user
from markupsafe import Markup
from saleapp import app, db
from saleapp.models import Category, Product, UserRole


class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class AdminAuthenticated(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render("admin/index.html")


class ProductAdmin(AuthenticatedView):
    column_list = ['name','price','category','created_date','image']
    column_formatters = {
        'price': lambda v, c, m, p: "{:,.0f} ₫".format(m.price).replace(",", "."),
        'image': lambda v, c, m, p: Markup(f'<img src="{m.image}" width="80">'),
    }

class CategoryAdmin(AuthenticatedView):
    column_list = ['name','products']



class MyAdminLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated


class StatsView(AdminAuthenticated):
    @expose('/')
    def index(self):
        return self.render("admin/stats.html")


admin = Admin(app=app,name="E-CORMMERCE", theme=Bootstrap4Theme(),index_view=MyIndexView())

admin.add_view(ProductAdmin(Product,db.session))
admin.add_view(CategoryAdmin(Category,db.session))
admin.add_view(StatsView("Thống kê"))
admin.add_view(MyAdminLogoutView("Đăng xuất"))