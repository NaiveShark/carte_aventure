from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Quest, Question, AnswerVar

# CONST standart questions
CONST_QUESTS = [
    { "name" : "Do you know the planets?",
      "description" : "Do you know the planets of Solar system?",
      "questions" : [
          { "question_description" : "Earth", "answers" : [ "Is it a planet?", "Yes", True, "No" ] },
          { "question_description" : "Moon", "answers" : [ "Is it a natural satellite?", "Yes", True, "No" ] } ]
      },

    { "name" : "Do you know the Roman Empire?", "description" : "Do you know the history of ancient Roman Empire?", "questions" : [ { "question_description" : "Trajan" }, { "question_description" : "Marcus Aurelius" }, ] }
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
            q = Question( question_description = qd["question_description"], quest_id = quest.id )
            DB.add( q )
            await DB.commit()
            if qd.get("answers"):

                a = AnswerVar( answer_title = qd["answers"][0], question_id = q.id, right_message = qd["answers"][1], is_true_answer = qd["answers"][2], wrong_message = qd["answers"][3] )
                DB.add( a )
                await DB.commit()


#