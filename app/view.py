from urllib.parse import parse_qsl

from starlette.requests import Request
from starlette.responses import (
    HTMLResponse, PlainTextResponse, RedirectResponse
)
from starlette_login.decorator import login_required
from starlette_login.utils import login_user, logout_user
from datetime import datetime

from .models import User, Quest, Question, AnswerVar, Player_Quest, Player_Quest_Answers, CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS

from starlette.templating import Jinja2Templates
from starlette_login.login_manager import LoginManager

from sqlalchemy import select, func, exists
from sqlalchemy.orm import selectinload

import markdown

login_manager = LoginManager(redirect_to='login', secret_key='no_secret_here')
template = Jinja2Templates(directory='templates' )

# Register custom markdown filter
def render_markdown(text: str) -> str:
    if not text:
        return ""
    # 'fenced_code' allows ```python ... ``` blocks
    # 'tables' adds support for markdown tables
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])

template.env.filters["markdown"] = render_markdown


async def login_page(request: Request):
    db = request.state.db
    error = ''
    if request.method == 'POST':
        body = (await request.body()).decode()
        data = dict(parse_qsl(body))
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            error = "Invalid username or password"
        else:
            user = await User.get_user_by_username(db, username)
            if user:
                if user.check_password(password) is True:
                    await login_user(request, user)
                    return RedirectResponse('/', status_code=302)
                else:
                    error = "Invalid password"
            else:
                error = "User not found"

    return template.TemplateResponse(
    request,
        'login.html', context={ "error" : error  }
    )

async def logout_page(request: Request):
    if request.user.is_authenticated:
        content = 'Logged out'
        await logout_user(request)
        return RedirectResponse('/', status_code=303)
    else:
        content = 'You not logged in'
        return PlainTextResponse(content)

async def reg_new_user(request: Request):
    db = request.state.db
    error = ''
    if request.method == 'POST':
        body = (await request.body()).decode()
        data = dict(parse_qsl(body))
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            error = "Invalid username or password"
        else:
            user = await User.get_user_by_username(db, username)
            if user:
                error = "User name taken. Choose another name"
            else:
                await User.create_user( db, username, password, is_admin=False )

                user = await User.get_user_by_username(db, username)
                if user:
                    if user.check_password(password) is True:
                        await login_user(request, user)
                        return RedirectResponse('/', status_code=302)
                    else:
                        error = "Invalid password"

    return template.TemplateResponse(
    request,
        'reg.html', context={ "error" : error  }
    )

async def home_page(request: Request):
    return template.TemplateResponse(
    request,
        'home.html', context={ }
    )

async def map_tools(request: Request):
    return template.TemplateResponse(
    request,
        'map_tools.html', context={ }
    )

@login_required
async def view_user_profile(request: Request):
    # main.LocalDBSession
    db = request.state.db
    user = request.user
    if user is None:
        return None
    else:
        query_q = select(Player_Quest).where(Player_Quest.user_id == user.id ).options(selectinload(Player_Quest.quest))
        query_c = await db.execute(query_q)
        quests = query_c.scalars().all()

        return template.TemplateResponse(
                 request,
                'user_profile.html', context={ "quests" : quests, }
            )


@login_required
async def quests_page(request: Request):
    # main.LocalDBSession
    db = request.state.db

    query = select(Quest).where(Quest.is_active == True )
    result = await db.execute(query)
    if result is None:
        return None
    else:
        quests = result.scalars().all()
        return template.TemplateResponse(
                 request,
                'quests.html', context={ 'quests' : quests, }
            )

@login_required
async def view_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db
    user = request.user

    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id )

    if quest is None:
        return None
    else:

        # check - may be quest is already played by user
        pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )
        pq_e = await db.execute(pq_query)
        pq = pq_e.scalar_one_or_none()

        return template.TemplateResponse(
                 request,
                'play_quest.html', context={ 'quest' : quest, "pq" : pq }
            )

@login_required
async def play_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id )

    if quest is None:
        return None
    else:
        # check - may be quest is already played by user
        pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )
        pq_e = await db.execute(pq_query)
        pq = pq_e.scalar_one_or_none()
        if pq:
            print( 'ready' )
        else:
            pq = Player_Quest( quest_id = quest_id, user_id = user.id, quest_began = datetime.now() )

            # calc question count at start

            pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )

            question_count_q = ( select(func.count(Question.id)).where(Question.quest_id == quest_id ) )
            pq.questions_count = await db.scalar(question_count_q)

            db.add( pq )
            await db.commit()
            print( 'new' )

        return RedirectResponse(url='/quest/in_play_it/' + str( pq.id ) )

# User in process of playing for this quest
@login_required
async def in_play_quest(request: Request ):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    player_quest_id = request.path_params['player_quest_id']
    player_quest = await db.get(Player_Quest, player_quest_id )

    if player_quest is None:
        return None
    else:
        answer_variants = None
        current_question_id = request.query_params.get("current_question_id", default=None)

        quest_id = player_quest.quest_id
        quest = await db.get(Quest, quest_id )
        questions_q = select(Question).where( Question.quest_id == quest_id )
        current_question = None
        questions = await db.execute( questions_q )

        pqa = None
        question_need_map = False

        if current_question_id:
            current_question = await db.get(Question, current_question_id )
            question_need_map = ( current_question.question_type == CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS )

            av_query = select(AnswerVar).where( AnswerVar.question_id == current_question_id )
            answer_await = await db.execute(av_query)
            answer_variants = answer_await.scalars().all()
            # detect, may be already answered
            pqa_query = select(Player_Quest_Answers).where(Player_Quest_Answers.player_quest_id == player_quest_id, Player_Quest_Answers.question_id == current_question_id )
            pqa_e = await db.execute(pqa_query)
            pqa = pqa_e.scalar_one_or_none()

        return template.TemplateResponse(
                 request,
                'play_quest_stage.html', context={
                    "quest" : quest,
                    "player_quest_id" : player_quest_id,
                    "player_quest" : player_quest,
                    "questions" : questions.scalars().all(),
                    "current_question_id" : current_question_id,
                    "current_question" : current_question,
                    "question_need_map" : question_need_map,
                    "answer_variants" : answer_variants,
                    "pqa" : pqa,
                }
            )

# user answered the question
@login_required
async def handle_qqa(request: Request ):
    db = request.state.db

    user = request.user

    player_quest_id = request.path_params['player_quest_id']
    player_quest = await db.get(Player_Quest, player_quest_id )
    current_question_id = request.path_params['current_question_id']

    # check - may be user is answering already (prevent second answering with BACK command)

    pqa_exits_q = select(exists().where( Player_Quest_Answers.player_quest_id == player_quest_id, Player_Quest_Answers.question_id == current_question_id ) )
    pqa_exits = await db.scalar(pqa_exits_q)
    if not pqa_exits:
        async with request.form() as form:
            answer_var_id = form.get("answer_var")

            #detect the answer
            answer_var = await db.get(AnswerVar, answer_var_id )
            check_answer = answer_var.is_true_answer

            pqa = Player_Quest_Answers(
                player_quest_id = player_quest_id,
                question_id = current_question_id,
                answervar_id = answer_var_id,
                answered_dt = datetime.now(),
                is_right_answer = check_answer
            )
            db.add( pqa )
            await db.commit()
            # check - may be a quest is done?
            player_quest.final_score = player_quest.final_score + 1
            player_quest.answered_count = player_quest.answered_count + 1

            if check_answer:
                player_quest.answered_right_count = player_quest.answered_right_count + 1
            else:
                player_quest.answered_wrong_count = player_quest.answered_wrong_count + 1

            if player_quest.questions_count == player_quest.answered_count:
                player_quest.quest_end = datetime.now()

            await db.commit()

    return RedirectResponse(url='/quest/in_play_it/' + str( player_quest_id ) + '?current_question_id=' + str( current_question_id ), status_code=303 )

#