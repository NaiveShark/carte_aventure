from urllib.parse import parse_qsl

from starlette.requests import Request
from starlette.responses import (
    HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
)
from starlette_login.decorator import login_required
from starlette_login.utils import login_user, logout_user
from datetime import datetime

from .models import User, Quest, Question, AnswerVar, Player_Quest, Player_Quest_Answers, CONST_QUESTION_TYPE_TEXT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER, CONST_QUEST_QUIZ, CONST_QUEST_TREASURE_QUEST, CONST_PERMISSIBLE_DISTANCE_DEVIATION_QUIZ, CONST_PERMISSIBLE_DISTANCE_DEVIATION_TREASURE, News_Feed, Public_Treasure_Quest, Public_Treasure_Quest_User_Share, Public_Treasure_Quest_User_Try
from .gis import get_distance_m, random_x, random_y

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
                await User.create_user( db, username, username, password, is_admin=False )

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
    # main.LocalDBSession
    db = request.state.db
    user = request.user
    if not ( user is None ):
        news_q = select(News_Feed).where(News_Feed.is_active == True ).order_by(News_Feed.published_dt.desc()).options(selectinload(News_Feed.quest))
        news_c = await db.execute(news_q)
        news = news_c.scalars().all()

    return template.TemplateResponse(
    request,
        'home.html', context={ 'news' : news, }
    )

@login_required
async def view_user_profile(request: Request):
    # main.LocalDBSession
    db = request.state.db
    user = request.user
    if user is None:
        return None
    else:
        # list of quizzes
        quizzes_q = select(Player_Quest).where(Player_Quest.user_id == user.id ).options(selectinload(Player_Quest.quest))
        quizzes_c = await db.execute(quizzes_q)
        quizzes = quizzes_c.scalars().all()

        # list of treasure quests
        treasure_quests_q = select( Public_Treasure_Quest_User_Share ).where( Public_Treasure_Quest_User_Share.user_id == user.id ).options( selectinload( Public_Treasure_Quest_User_Share.public_treasurequest ).selectinload( Public_Treasure_Quest.quest ) )
        treasure_quests_c = await db.execute(treasure_quests_q)
        treasure_quests = treasure_quests_c.scalars().all()

        return template.TemplateResponse(
                 request,
                'user_profile.html', context={ "quizzes" : quizzes, 'treasure_quests' : treasure_quests,  }
            )

@login_required
async def view_quiz_top(request: Request):
    # main.LocalDBSession
    db = request.state.db
    player_quizzes_q = select(Player_Quest).where(Player_Quest.quest_end != None).options( selectinload( Player_Quest.quest ), selectinload( Player_Quest.user ) ).order_by(Player_Quest.final_score.desc())
    player_quizzes_d = await db.execute(player_quizzes_q)
    player_quizzes = player_quizzes_d.scalars().all()

    treasure_quests_q = select( Public_Treasure_Quest_User_Share ).options( selectinload( Public_Treasure_Quest_User_Share.public_treasurequest ).selectinload( Public_Treasure_Quest.quest ) ).order_by(Public_Treasure_Quest_User_Share.user_score.desc())
    treasure_quests_c = await db.execute(treasure_quests_q)
    treasure_quests = treasure_quests_c.scalars().all()

    top_players_q = select(User).where( User.is_bot == False, User.is_admin == False ).order_by(User.user_total_score.desc())
    top_players_c = await db.execute( top_players_q )
    top_players = top_players_c.scalars().all()
    
    return template.TemplateResponse(
                request,
                'view_quiz_top.html', context={ "player_quizzes" : player_quizzes, 'treasure_quests' : treasure_quests, 'top_players' : top_players, }
            )

@login_required
async def quizzes_page(request: Request):
    # main.LocalDBSession
    db = request.state.db

    query = select(Quest).where(Quest.is_active == True, Quest.quest_type == CONST_QUEST_QUIZ )
    result = await db.execute(query)
    if result is None:
        return None
    else:
        quests = result.scalars().all()
        return template.TemplateResponse(
                 request,
                'quizzes.html', context={ 'quests' : quests, }
            )

@login_required
async def quests_page(request: Request):
    # main.LocalDBSession
    db = request.state.db

    query = select(Quest).where(Quest.is_active == True, Quest.quest_type == CONST_QUEST_TREASURE_QUEST )
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
async def start_public_treasure_quest( request: Request ):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    quest_id = request.path_params['quest_id']

    ptq = Public_Treasure_Quest( quest_id = quest_id, quest_began = datetime.now(), started_user_id = user.id )
    db.add( ptq )
    await db.commit()
    ptqus = Public_Treasure_Quest_User_Share( public_treasure_quest_id = ptq.id, user_id = user.id, user_score = 1 )
    # add to user score
    user.increment_score( 1 )

    db.add( ptqus )
    await db.commit()

    return RedirectResponse(url='/view/quest/' + str( quest_id ) )

@login_required
async def get_treasure_quest_dots( request: Request ):
    # main.LocalDBSession
    db = request.state.db

    ptq_id = request.path_params['ptq_id']
    ptq = await db.get(Public_Treasure_Quest, ptq_id )

    ptqut_q = select( Public_Treasure_Quest_User_Try ).where( Public_Treasure_Quest_User_Try.public_treasure_quest_id == ptq_id )
    ptqut_e = await db.execute( ptqut_q )
    ptqut_list = ptqut_e.scalars().all()

    dots = []
    i = 1
    for ptqut in ptqut_list:
        dist = ptqut.distance_to_target
        if dist < CONST_PERMISSIBLE_DISTANCE_DEVIATION_TREASURE:
            caption = 'FIND IT!'
        else:
            caption = f"Miss {dist:,.2f} away".replace(",", " ")
        dots.append(
          {
            "id": i,
            "caption": caption,
            "longitude": ptqut.try_map_X,
            "latitude": ptqut.try_map_Y,
          }
        )
        i = i + 1

    return JSONResponse( dots )

@login_required
async def post_treasure_quest_dot( request: Request ):
    game_over = False
    try:
        # main.LocalDBSession
        db = request.state.db

        user = request.user

        ptq_id = request.path_params['ptq_id']
        ptq = await db.get(Public_Treasure_Quest, ptq_id )

        # Extract the JSON payload from the request body
        data = await request.json()

        # Extract coordinates
        x = data.get("x")
        y = data.get("y")

        # Simple validation check
        if x is None or y is None:
            return JSONResponse({"error": "Missing x or y coordinate"}, status_code=400)

        # Triсk. We don't have the true dot before users start to search
        if ( not ptq.target_map_X ) and ( not ptq.target_map_Y ):
            ptq.target_map_X = random_x( x )
            ptq.target_map_Y = random_y( y )
            await db.commit()

        new_dot = {"x": float(x), "y": float(y)}
        calc_distance_to_target = get_distance_m( ptq.target_map_X, ptq.target_map_Y, x, y )
        ptqut = Public_Treasure_Quest_User_Try( public_treasure_quest_id = ptq_id, user_id = user.id, saved_dt = datetime.now(),
                try_map_X = x,
                try_map_Y = y,
                distance_to_target = calc_distance_to_target
        )

        db.add( ptqut )
        await db.commit()

        # check try is close enought
        if calc_distance_to_target < CONST_PERMISSIBLE_DISTANCE_DEVIATION_TREASURE:
            # game over!
            game_over = True
            set_json_status = 'game_over'
            ptq.quest_end = datetime.now()
            ptq.ended_user_id = user.id
            await db.commit()

            ptqut.final_try = True
            await db.commit()
        else:
            set_json_status = 'success'

        # user score
        # new shooter in quest +1 score
        # final shooter +"difficulty_coefficient" score
        # for end of game at first shoot 1+"difficulty_coefficient"
        score_delta = 0
        if game_over:
            quest = await db.get( Quest, ptq.quest_id )
            score_delta = score_delta + quest.difficulty_coefficient

        ptqus_q = select( Public_Treasure_Quest_User_Share ).where( Public_Treasure_Quest_User_Share.public_treasure_quest_id == ptq.id, Public_Treasure_Quest_User_Share.user_id == user.id )
        ptqus_e = await db.execute(ptqus_q)
        ptqus = ptqus_e.scalars( ).first()
        if not ptqus:
            score_delta = score_delta + 1
            ptqus = Public_Treasure_Quest_User_Share( public_treasure_quest_id = ptq.id, user_id = user.id, user_score = score_delta )
            db.add( ptqus )

            await db.commit()
        else:
            if game_over:
                ptqus.user_score = ptqus.user_score + score_delta
                db.add( ptqus )
                
                # add to user score
                user.increment_score( ptqus.user_score )
                await db.commit()


        #print(f"Received new dot via Starlette at: X={x}, Y={y}")
        return JSONResponse({"status": set_json_status, "data": new_dot}, status_code=201)

    except Exception as e:
        return JSONResponse({"error": "Invalid JSON format"}, status_code=400)

@login_required
async def play_treasure_quest( request: Request, db, user, quest ):
    users_in_quest = None
    steps_overall = 0
    ptq_in_play = False

    ptq_query = select(Public_Treasure_Quest).where(Public_Treasure_Quest.quest_id == quest.id )
    ptq_e = await db.execute(ptq_query)
    ptq = ptq_e.scalar_one_or_none()

    if ptq and ptq.quest_end:
        # Target may diff from win dot. Get last win try
        win_ptqut_q = select( Public_Treasure_Quest_User_Try ).where( Public_Treasure_Quest_User_Try.public_treasure_quest_id == ptq.id, Public_Treasure_Quest_User_Try.final_try == True )
        win_ptqut_e = await db.execute( win_ptqut_q )
        win_ptqut = win_ptqut_e.scalar_one_or_none()

        start_dot_X = win_ptqut.try_map_X
        start_dot_Y = win_ptqut.try_map_Y

        #start_dot_X = ptq.target_map_X
        #start_dot_Y = ptq.target_map_Y

        start_map_ZOOM = 12
    else:
        start_dot_X = 0.0
        start_dot_Y = 0.0
        start_map_ZOOM = 2

    # hunt is proceed. make the tools available
    if ptq:
        # select users in game
        sub_users_in_quest_q = select( Public_Treasure_Quest_User_Try ).where( Public_Treasure_Quest_User_Try.user_id == User.id, Public_Treasure_Quest_User_Try.public_treasure_quest_id == ptq.id ).exists()
        users_in_quest_q = select(User).where( sub_users_in_quest_q )
        #print( str( users_in_quest_q ) )
        users_in_quest = await db.scalars( users_in_quest_q )

        ptq_in_play = ( ptq.quest_began) and ( not ptq.quest_end )
        if ptq.quest_end:
            query = (
                select(func.count(Public_Treasure_Quest_User_Try.id))
                .where(Public_Treasure_Quest_User_Try.public_treasure_quest_id == ptq.id )
                )
            steps_overall = await db.scalar(query) or 0

    return template.TemplateResponse(
             request,
            'play_treasure_quest.html',
            context={
                'quest' : quest,
                'ptq' : ptq,
                'ptq_in_play' : ptq_in_play,
                'users_in_quest' : users_in_quest,
                'start_dot_X' : start_dot_X,
                'start_dot_Y' : start_dot_Y,
                'start_map_ZOOM' : start_map_ZOOM,
                'steps_overall' : steps_overall,
            }
        )

@login_required
async def view_quest(request: Request):
    # main.LocalDBSession
    db = request.state.db
    user = request.user

    quest_id = request.path_params['quest_id']
    quest = await db.get(Quest, quest_id, options= [ selectinload( Quest.user_creator ) ] )

    if quest is None:
        return None
    else:
        if quest.is_treasure_quest:
            return await play_treasure_quest( request, db, user, quest )
        else:
            # check - may be quest is already played by user
            pq_query = select(Player_Quest).where(Player_Quest.quest_id == quest_id, Player_Quest.user_id == user.id )
            pq_e = await db.execute(pq_query)
            pq = pq_e.scalar_one_or_none()

            return template.TemplateResponse(
                     request,
                    'play_quiz.html', context={ 'quest' : quest, "pq" : pq }
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
        current_question = None

        subq = select(
            Player_Quest_Answers.question_id, Player_Quest_Answers.is_right_answer,
            func.max(Player_Quest_Answers.id).label('max_sub_id')
        ).where(Player_Quest_Answers.player_quest_id==player_quest_id).group_by(Player_Quest_Answers.question_id).subquery()

        questions_q = select(Question, subq).outerjoin( subq, Question.id == subq.c.question_id).where( Question.quest_id == quest_id )
        questions = await db.execute( questions_q )


        pqa = None
        # we need to show the map for question
        question_need_map = False
        # we need to show the dot moving for map for question answering
        question_need_map_dot = False
        question_need_map_dot_mover = False
        start_dot_X = None
        start_dot_Y = None
        dot_color = ''

        if current_question_id:
            current_question = await db.get(Question, current_question_id )
            # if question contain MAP QUIZ or "Place the dot in the right place"
            question_need_map = ( current_question.question_type == CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS ) or ( current_question.question_type == CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER )
            # if question is "Place the dot in the right place"
            question_need_map_dot = ( current_question.question_type == CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER )

            # we need the answer variants?
            if ( current_question.question_type == CONST_QUESTION_TYPE_TEXT_AND_TEXT_VARS ) or ( current_question.question_type == CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS ):
                av_query = select(AnswerVar).where( AnswerVar.question_id == current_question_id )
                answer_await = await db.execute(av_query)
                answer_variants = answer_await.scalars().all()

            # detect, may be already answered
            pqa_query = select(Player_Quest_Answers).where(Player_Quest_Answers.player_quest_id == player_quest_id, Player_Quest_Answers.question_id == current_question_id ).options(selectinload(Player_Quest_Answers.answervar))

            pqa_e = await db.execute(pqa_query)
            pqa = pqa_e.scalar_one_or_none()
            # edit dot
            question_need_map_dot_mover = question_need_map_dot and (not pqa )
            if question_need_map_dot_mover:
                dot_color = "'#FFFF00'" # Yellow color
            else:
                if pqa:
                    if pqa.is_right_answer:
                        dot_color = "'#008000'" # Green color
                    else:
                        dot_color = "'#ff0000'" # Red color
            # started dot
            if question_need_map:
                start_dot_X = current_question.question_map_X
                start_dot_Y = current_question.question_map_Y
                start_dot_Y = current_question.question_map_Y
                if question_need_map_dot:
                    # if qestion is answered
                    if pqa:
                        start_dot_X = pqa.answer_map_X
                        start_dot_Y = pqa.answer_map_Y

        return template.TemplateResponse(
                 request,
                'play_quest_stage.html', context={
                    "quest" : quest,
                    "player_quest_id" : player_quest_id,
                    "player_quest" : player_quest,
                    "questions" : questions.all(),
                    "current_question_id" : current_question_id,
                    "current_question" : current_question,
                    "question_need_map" : question_need_map,
                    "question_need_map_dot" : question_need_map_dot,
                    "question_need_map_dot_mover" : question_need_map_dot_mover,
                    "dot_color" : dot_color,
                    "start_dot_X" : start_dot_X,
                    "start_dot_Y" : start_dot_Y,
                    "answer_variants" : answer_variants,
                    "pqa" : pqa,
                }
            )

# User in process of playing for this quest and want the next question
@login_required
async def in_play_it_next(request: Request ):
    # main.LocalDBSession
    db = request.state.db

    user = request.user

    player_quest_id = request.path_params['player_quest_id']
    player_quest = await db.get(Player_Quest, player_quest_id )
    next_question_id = None

    if player_quest is None:
        return None
    else:
        subq = select( Player_Quest_Answers.question_id ).where(Player_Quest_Answers.player_quest_id == player_quest_id )
        next_question_q = select(Question).where( Question.quest_id == player_quest.quest_id ).where(Question.id.not_in(subq))
        # get list of unanswered qeustions
        next_question_e = await db.execute(next_question_q)
        # get first
        next_question = next_question_e.scalars().first()

        if next_question:
            next_question_id = next_question.id
            return RedirectResponse(url='/quest/in_play_it/' + str( player_quest_id ) + '?current_question_id=' + str( next_question_id ) )
        else:
            return RedirectResponse(url='/quest/in_play_it/' + str( player_quest_id ) )

# user answered the question
@login_required
async def handle_qqa(request: Request ):
    db = request.state.db

    user = request.user

    player_quest_id = request.path_params['player_quest_id']
    player_quest = await db.get(Player_Quest, player_quest_id )
    quest = await db.get(Quest, player_quest.quest_id )
    current_question_id = request.path_params['current_question_id']

    # check - may be user is answering already (prevent second answering with BACK command)

    pqa_exits_q = select(exists().where( Player_Quest_Answers.player_quest_id == player_quest_id, Player_Quest_Answers.question_id == current_question_id ) )
    pqa_exits = await db.scalar(pqa_exits_q)
    if not pqa_exits:
        longitude = None
        latitude  = None
        distance = None
        async with request.form() as form:

            # this is a text varion choosed
            answer_var_id = form.get("answer_var")
            if answer_var_id:
                #detect the answer
                answer_var = await db.get(AnswerVar, answer_var_id )
                check_answer = answer_var.is_true_answer

            else:
               # it's a dot placed answer with coord
               answer_var_q = select( AnswerVar ).where( AnswerVar.question_id == current_question_id )
               answer_var_e = await db.execute(answer_var_q)
               answer_var = answer_var_e.scalars( ).first()
               answer_var_id = answer_var.id
               # check for coordinates distant
               longitude = float( form.get("longitude") )
               latitude  = float( form.get("latitude") )
               distance = get_distance_m( answer_var.true_answer_map_X, answer_var.true_answer_map_Y, longitude, latitude)

               check_answer = ( distance < CONST_PERMISSIBLE_DISTANCE_DEVIATION_QUIZ )


            pqa = Player_Quest_Answers(
                player_quest_id = player_quest_id,
                question_id = current_question_id,
                answervar_id = answer_var_id,
                answered_dt = datetime.now(),
                answer_map_X = longitude,
                answer_map_Y = latitude,
                answer_distance = distance,
                is_right_answer = check_answer
            )
            db.add( pqa )
            await db.commit()
            # check - may be a quest is done?
            player_quest.answered_count = player_quest.answered_count + 1

            if check_answer:
                player_quest.answered_right_count = player_quest.answered_right_count + 1
                player_quest.final_score = player_quest.final_score + quest.difficulty_coefficient
            else:
                player_quest.answered_wrong_count = player_quest.answered_wrong_count + 1

            if player_quest.questions_count == player_quest.answered_count:
                # fix the quest end
                player_quest.quest_end = datetime.now()
                # fix the user score
                user.increment_score( player_quest.final_score )

            await db.commit()

    return RedirectResponse(url='/quest/in_play_it/' + str( player_quest_id ) + '?current_question_id=' + str( current_question_id ), status_code=303 )

#