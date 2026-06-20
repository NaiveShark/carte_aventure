from sqladmin import ModelView
from app.models import User, Quest, Question, AnswerVar, QuestQuestion

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

class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.question_description]
    column_searchable_list = [Question.question_description]
    column_sortable_list = [Question.id]
    form_columns = [Question.question_description]
    icon = "fa-solid fa-box"

class AnswerVarAdmin(ModelView, model=AnswerVar):
    column_list = [AnswerVar.id, AnswerVar.answer_title, AnswerVar.question]
    column_searchable_list = [AnswerVar.answer_title]
    column_sortable_list = [AnswerVar.id]
    #form_columns = [AnswerVar.answer_title]
    icon = "fa-solid fa-box"
    
class QuestQuestionAdmin(ModelView, model=QuestQuestion):
    column_list = [QuestQuestion.id, QuestQuestion.quest, AnswerVar.question]
    #column_searchable_list = [QuestQuestion.question]
    column_sortable_list = [QuestQuestion.id]
    #form_columns = [AnswerVar.answer_title]
    icon = "fa-solid fa-box"
