from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)

class Quest(Base):
    __tablename__ = "quest"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question_description = Column(String, nullable=True)

class QuestQuestion(Base):
    __tablename__ = "questquestion"
    id = Column(Integer, primary_key=True, index=True)
    
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

class AnswerVar(Base):
    __tablename__ = "answervar"
    id = Column(Integer, primary_key=True, index=True)
    answer_title = Column(String, nullable=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

    wrong_message = Column(String, nullable=True)
    right_message = Column(String, nullable=True)
    is_true_answer = Column(Boolean, default=True)
