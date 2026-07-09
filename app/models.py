from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Auth and user tables
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from starlette.requests import Request
from starlette_login.mixins import UserMixin


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password = Column(String(128))
    title_name = Column(String(150))
    is_bot = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_editor = Column(Boolean, default=False)

    @property
    def identity(self):
        return self.id

    @property
    def display_name(self) -> str:
        return self.title_name

    def set_password(self, password: str):
        self.password = pbkdf2_sha256.hash(password)

    def check_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    async def get_user_by_id(cls, request: Request, user_id: int):
        db = request.state.db
        return await db.get(User, user_id)

    @classmethod
    async def get_user_by_username(cls, db: AsyncSession, username: str):
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        if result is None:
            return None
        else:
            return result.scalars().first()

    @classmethod
    async def create_user(
        cls, db: AsyncSession,
        username: str,
        usertitle: str,
        password: str,
        is_admin: bool = False,
        is_editor: bool = False,
        is_bot: bool = False
    ):
        user = cls(
            username=username,
            title_name = usertitle,
            password=password,
            is_admin=is_admin,
            is_editor=is_editor,
            is_bot = is_bot,
        )
        user.set_password(password)
        db.add(user)
        await db.commit()
        return user

# Data tables
# individual quiz
CONST_QUEST_QUIZ = 0
# common (public) treasure quest
CONST_QUEST_TREASURE_QUEST = 1

# Quest and quiz
class Quest(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    # quest_type
    # CONST_QUEST_QUIZ for quiz with CONST_QUESTION_TYPE_TEXT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER
    # CONST_QUEST_TREASURE_QUEST for treasure quest over map
    quest_type = Column(Integer, nullable=False, default = CONST_QUEST_QUIZ )

    user_creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    user_creator = relationship( "User" )
    # difficulty coefficient
    difficulty_coefficient = Column(Integer, nullable=False, default=1)

    @property
    def is_treasure_quest(self) -> str:
        return self.quest_type == CONST_QUEST_TREASURE_QUEST


# question types const
# 0 is for simple quiz with text variants
CONST_QUESTION_TYPE_TEXT_AND_TEXT_VARS = 0
# 1 is for map description for questions, center on X,Y,ZOOM, answers is simple text variant
CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS = 1
# 2 is for map description for questions, center on X,Y,ZOOM, answers is user placed dot
CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER = 2

# permissible distance deviation for answer X,Y from true X,Y
CONST_PERMISSIBLE_DISTANCE_DEVIATION = 0.5

class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_title = Column(Text, nullable=True)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

    # question_type
    question_type = Column(Integer, nullable=False, default = CONST_QUESTION_TYPE_TEXT_AND_TEXT_VARS )

    # if question_type is [CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER ],
    # then X, Y, ZOOM is visible position of map in question description
    # this is not an answer or targed dot, this is a map start position only
    question_map_X = Column(Float, nullable = True )
    question_map_Y = Column(Float, nullable = True )
    question_map_ZOOM = Column(Integer, nullable = True )

class AnswerVar(Base):
    id = Column(Integer, primary_key=True, index=True)
    answer_title = Column(String, nullable=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

    right_message = Column(String, nullable=True)
    is_true_answer = Column(Boolean, default=False, nullable=False )
    wrong_message = Column(String, nullable=True)

    # if question.question_type is [CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER ],
    # then true_map_data contain geojson for answer true target dot
    true_answer_map_X = Column( Float )
    true_answer_map_Y = Column( Float )

# quiz played by player
class Player_Quest(Base):

    # one quest per user constaint
    __table_args__ = (
        UniqueConstraint("quest_id", "user_id", name="uq_user_quest"), )

    id = Column(Integer, primary_key=True, index=True)

    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    user = relationship( "User" )

    quest_began = Column( DateTime(timezone=True), nullable=False )
    quest_end = Column( DateTime(timezone=True) )

    questions_count = Column(Integer, nullable=False, default=0 )
    answered_count = Column(Integer, nullable=False, default=0 )
    answered_right_count = Column(Integer, nullable=False, default=0 )
    answered_wrong_count = Column(Integer, nullable=False, default=0 )
    final_score = Column(Integer, nullable=False, default=0 )

# treasure quest played public play, for CONST_QUEST_TREASURE_QUEST
class Public_Treasure_Quest(Base):
    id = Column(Integer, primary_key=True, index=True)

    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=False )
    quest = relationship( "Quest" )

    quest_began = Column( DateTime(timezone=True), nullable=False )
    quest_end = Column( DateTime(timezone=True) )

    started_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    started_user = relationship( "User", foreign_keys=[started_user_id] )

    ended_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True )
    ended_user = relationship( "User", foreign_keys=[ended_user_id] )

# treasure quest played by player
class Public_Treasure_Quest_User_Try(Base):

    id = Column(Integer, primary_key=True, index=True)

    public_treasure_quest_id: Mapped[int] = mapped_column(ForeignKey("public_treasure_quest.id"), nullable=False )
    public_treasurequest = relationship( "Public_Treasure_Quest" )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    user = relationship( "User" )

    saved_dt = Column( DateTime(timezone=True), nullable=False )
    try_map_X = Column( Float, nullable=False )
    try_map_Y = Column( Float, nullable=False )


# quest played by player
class Player_Quest_Answers(Base):

    # one quest per user constaint
    __table_args__ = (
        UniqueConstraint("player_quest_id", "question_id", "answervar_id", name="uq_user_quest_answer"), )

    id = Column(Integer, primary_key=True, index=True)
    player_quest_id: Mapped[int] = mapped_column(ForeignKey("player_quest.id"), nullable=False )
    player_quest = relationship( "Player_Quest" )
    answered_dt = Column( DateTime(timezone=True) )

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False )
    question = relationship( "Question" )

    answervar_id: Mapped[int] = mapped_column(ForeignKey("answervar.id"), nullable=False )
    answervar = relationship( "AnswerVar" )

    is_right_answer = Column(Boolean, nullable=False )
    # for map dot quiz CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER
    answer_map_X = Column( Float )
    answer_map_Y = Column( Float )
    answer_distance = Column( Float )


# News feed
class News_Feed(Base):
    id = Column(Integer, primary_key=True, index=True)
    published_dt = Column( DateTime(timezone=True) )
    title = Column(String(250))
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    user_creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False )
    user_creator = relationship( "User" )

    # may be it's just a text announce, without links
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), nullable=True )
    quest = relationship( "Quest" )

#