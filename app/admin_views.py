from sqladmin import ModelView
from .models import User, Quest, Question, AnswerVar
from starlette.requests import Request

class UserAdmin(ModelView, model=User):
    column_list = [
        User.id, User.username,
        User.is_admin,
        User.is_editor
    ]
    form_excluded_columns = [User.password]

    def is_accessible(self, request: Request) -> bool:
        """Restrict access only by admin"""
        user = request.user
        return user and user.is_authenticated and user.is_admin

class QuestAdmin(ModelView, model=Quest):
    column_list = [Quest.id, Quest.name, Quest.is_active, Quest.quest_type]
    column_searchable_list = [Quest.name, Quest.quest_type]
    column_sortable_list = [Quest.id, Quest.quest_type]
    form_columns = [Quest.name, Quest.description, Quest.is_active, Quest.quest_type, Quest.difficulty_coefficient, Quest.user_creator ]
    icon = "fa-solid fa-box"

class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.question_title]
    column_searchable_list = [Question.question_title]
    column_sortable_list = [Question.id]
    form_columns = [Question.question_title]
    icon = "fa-solid fa-box"

class AnswerVarAdmin(ModelView, model=AnswerVar):
    column_list = [AnswerVar.id, AnswerVar.answer_title, AnswerVar.question]
    column_searchable_list = [AnswerVar.answer_title]
    column_sortable_list = [AnswerVar.id]
    #form_columns = [AnswerVar.answer_title]
    icon = "fa-solid fa-box"
    
