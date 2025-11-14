
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from markupsafe import Markup
from saleapp import app, db
from saleapp.models import Category, Product


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render("admin/index.html")


admin = Admin(app=app,name="E-CORMMERCE", theme=Bootstrap4Theme(),index_view=MyIndexView())

class ProductAdmin(ModelView):
    column_list = ['name','price','category','created_date','image']
    column_formatters = {
        'price': lambda v, c, m, p: "{:,.0f} ₫".format(m.price).replace(",", "."),
        'image': lambda v, c, m, p: Markup(f'<img src="{m.image}" width="80">'),
    }

admin.add_view(ProductAdmin(Product,db.session))
admin.add_view(ModelView(Category,db.session))