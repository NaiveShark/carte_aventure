from sqladmin import ModelView
from app.models import User, Quest

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id]
    form_columns = [User.username, User.email, User.is_active]
    icon = "fa-solid fa-user"

class QuestAdmin(ModelView, model=Quest):
    column_list = [Quest.id, Quest.name, Quest.is_active]
    column_searchable_list = [Quest.name]
    column_sortable_list = [Quest.id]
    form_columns = [Quest.name, Quest.description, Quest.is_active]
    icon = "fa-solid fa-box"
    
    