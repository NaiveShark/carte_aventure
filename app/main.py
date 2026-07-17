import logging

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from sqladmin import Admin

from starlette_login.backends import SessionAuthBackend
from starlette_login.login_manager import LoginManager
from starlette_login.middleware import AuthenticationMiddleware

from contextlib import asynccontextmanager

from .admin_views import UserAdmin, QuestAdmin, QuestionAdmin, AnswerVarAdmin
from .models import Base, User
from .view import login_page, logout_page, reg_new_user, home_page, view_user_profile, view_quiz_top, quizzes_page, quests_page, view_quest, play_quest, in_play_quest, handle_qqa, in_play_it_next, get_treasure_quest_dots, post_treasure_quest_dot, start_public_treasure_quest
from .pop import pop_data, BOT_USER_NAME, BOT_USER_TITLE

import mimetypes
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')

SECRET_KEY = 'our_webapp_secret_key'

# Check if running on Vercel, otherwise use local path
if os.environ.get("VERCEL"):
    DB_URL = "sqlite+aiosqlite:////tmp/mq.db"  # Note the 4 slashes for absolute path
else:
    DB_URL = 'sqlite+aiosqlite:///./mq.db'

logger = logging.getLogger('uvicorn.error')
db_engine = create_async_engine(DB_URL, connect_args={"check_same_thread": False}, ) # Required for SQLite in multi-threaded environments

# Create a session factory for generating database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Helper function to enable Write-Ahead Logging (WAL) for better concurrency
async def init_db():
    async with db_engine.begin() as conn:
        # Enable WAL mode
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        # Create tables if they do not exist
        await conn.run_sync(Base.metadata.create_all)

    # create start users and populate data
    async with get_db() as db:
        if not await User.get_user_by_username(db, 'admin'):
            await User.create_user(
            db, 'admin', 'Admin', 'password', is_admin=True
        )

        if not await User.get_user_by_username(db, 'u'):
            await User.create_user(
                db, 'u', 'u user', 'u'
            )

        if not await User.get_user_by_username(db, BOT_USER_NAME ):
            await User.create_user(
                db,
                BOT_USER_NAME, BOT_USER_TITLE,
                'password',
                is_bot=True
            )

        await pop_data( db )


# 1. Lifespan handler manages startup and shutdown events
@asynccontextmanager
async def lifespan(app: Starlette):
    # Setup: Initialize database and tables
    await init_db()
    yield
    # Shutdown: Clean up resources if necessary

# 2. Context manager to ensure database sessions close cleanly
@asynccontextmanager
async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Открываем сессию для каждого запроса
        async with get_db() as db:
            request.state.db = db
            response = await call_next(request)
            return response

login_manager = LoginManager(
    redirect_to='/login', secret_key=SECRET_KEY
)
login_manager.set_user_loader(User.get_user_by_id)

middleware = [
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
    Middleware(DatabaseMiddleware),
    Middleware(
        AuthenticationMiddleware,
        backend=SessionAuthBackend(login_manager),
        login_manager=login_manager,
        excluded_dirs=['/statics']
    )
]


app = Starlette(
    middleware=middleware,
    lifespan=lifespan,
    routes=[
        Route('/', home_page, name='home'),
        Route('/quizzes', quizzes_page, name='quizzes_page'),
        Route('/quests', quests_page, name='quests_page'),
        Route('/view_quiz_top', view_quiz_top, name='view_quiz_top'),

        Route("/view/quest/{quest_id}", view_quest, name='view_quest'),
        Route("/quest/play_it/{quest_id}", play_quest, name='play_quest'),
        Route("/quest/in_play_it/{player_quest_id}", in_play_quest, name='in_play_quest'),
        Route("/quest/in_play_it_next/{player_quest_id}", in_play_it_next, name='in_play_it_next'),
        Route("/quest/submit_form-qqa/{player_quest_id}/{current_question_id}", handle_qqa, methods=["POST"]),
        Route("/quest/start_public_treasure_quest/{quest_id}", start_public_treasure_quest ),
        Route("/quest/get_treasure_quest_dots/{ptq_id}", get_treasure_quest_dots ),
        Route("/quest/post_treasure_quest_dot/{ptq_id}", post_treasure_quest_dot, methods=["POST"] ),

        Route('/profile', view_user_profile, name='view_user_profile'),
        Route('/reg_new_user', reg_new_user, methods=['GET', 'POST'], name='reg_new_user'),
        Route('/login', login_page, methods=['GET', 'POST'], name='login'),
        Route('/logout', logout_page, name='logout'),

        Mount("/statics", StaticFiles(directory="statics"), name="statics"),

    ]
)
app.state.login_manager = login_manager

# Use `SessionMiddleware` and `AuthenticationMiddleware`
# to secure admin pages
admin = Admin(app, db_engine, middlewares=middleware)
admin.add_view(UserAdmin)
admin.add_view(QuestAdmin )
admin.add_view(QuestionAdmin )
admin.add_view(AnswerVarAdmin )

#