from sqladmin import ModelView
from app.models import User

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id]
    form_columns = [User.username, User.email, User.is_active]
    icon = "fa-solid fa-user"
