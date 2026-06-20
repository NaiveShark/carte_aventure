from sqladmin import ModelView
from app.models import User, Product

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id]
    form_columns = [User.username, User.email, User.is_active]
    icon = "fa-solid fa-user"

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.in_stock]
    column_searchable_list = [Product.name]
    column_sortable_list = [Product.id, Product.price]
    form_columns = [Product.name, Product.description, Product.price, Product.in_stock]
    icon = "fa-solid fa-box"
    
    