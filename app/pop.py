from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Quest, Question, AnswerVar

# CONST standart questions
CONST_QUESTS = [
    { "name" : "Do you know the planets?",
      "description" : "Do you know the planets of Solar system?",
      "questions" : [
          { "question_title" : "Which planet from the Sun is Earth?", 
            "answers" : [ 
              [ "(2) Second", None, False, "No, second planet is a Venus." ], 
              [ "(3) Third", "Yes", True, None ], 
              [ "(4) Fourth", None, False, "No, fourth planet is a Mars." ], 
               
              ] },
          { "question_title" : "Which planet is Titan a natural satellite of?", 
            "answers" : [ 
              [ "Mars", None, False, "No" ],
              [ "Pluto", None, False, "No" ],
              [ "Jupyter", None, False, "No" ],
              [ "Saturn", "Yes", True, None ],
              [ "Earth", None, False, "No" ],
              ] } 
              ]
      },

    { "name" : "Do you know the Roman Empire?", "description" : "Do you know the history of ancient Roman Empire?", "questions" : [ { "question_title" : "Trajan" }, { "question_title" : "Marcus Aurelius" }, ] }
 ]

async def pop_data( DB : AsyncSession ):

    check_query = select(Quest)
    result = await DB.execute(check_query)
    if result.scalars().first():
        return 0


    for сq_d in CONST_QUESTS:
        quest = Quest( name = сq_d["name"], description = сq_d["description"], is_active = True  )
        DB.add( quest )
        await DB.commit()
        for qd in сq_d["questions"]:
            q = Question( question_title = qd["question_title"], quest_id = quest.id )
            DB.add( q )
            await DB.commit()
            if qd.get("answers"):
                for answer in qd.get("answers"):
                    a = AnswerVar( answer_title = answer[0], question_id = q.id, right_message = answer[1], is_true_answer = answer[2], wrong_message = answer[3] )
                    DB.add( a )
                    await DB.commit()


#