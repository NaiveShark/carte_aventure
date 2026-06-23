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

    { "name" : "Do you know the Roman Empire?", 
      "description" : "Do you know the history of ancient Roman Empire?", 
      "questions" : [ 
          { "question_title" : "Under which ruler did the Roman Empire reach its maximum territorial extent?", 
             "answers" : [ 
              [ "Hadrian", None, False, "No." ], 
              [ "Trajan", "Yes. Key geographic achievements under Trajan included Armenia, Assyria, Mesopotamia and Dacia.", True, None ], 
              [ "Nero", None, False, "No." ], 
              [ "Julius Caesar", None, False, "No." ],         
          ] }
          ]
     },
 
 
 {
    "name": "Do you know Roman Architecture?",
    "description": "Test your knowledge on the greatest engineering feats of Ancient Rome.",
    "questions": [
        {
            "question_title": "Which iconic Roman amphitheater was commissioned around 70-72 AD by Emperor Vespasian?",
            "answers": [
                ["The Pantheon", "None", False, "No."],
                ["The Colosseum", "Correct! The Colosseum is the largest ancient amphitheater ever built.", True, "None"],
                ["Circus Maximus", "None", False, "No."],
                ["The Roman Forum", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "The Fall of the Republic",
    "description": "Explore the dramatic transition from the Roman Republic to the Empire.",
    "questions": [
        {
            "question_title": "On which famous date was Julius Caesar assassinated in the Roman Senate?",
            "answers": [
                ["March 15, 44 BC", "Correct! This date is famously known as the Ides of March.", True, "None"],
                ["January 1, 45 BC", "None", False, "No."],
                ["August 19, 14 AD", "None", False, "No."],
                ["November 23, 50 BC", "None", False, "No."]
            ]
        }
    ]
},
 
{
    "name": "The Founding of Rome",
    "description": "Test your knowledge on the myths and early history of Rome's creation.",
    "questions": [
        {
            "question_title": "According to Roman mythology, who was the first king and legendary founder of Rome?",
            "answers": [
                ["Remus", "None", False, "No."],
                ["Romulus", "Yes. Romulus founded the city in 753 BC after a fatal dispute with his twin brother Remus.", True, "None"],
                ["Aeneas", "None", False, "No."],
                ["Numa Pompilius", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "The Punic Wars",
    "description": "Questions about Rome's legendary conflicts with Carthage.",
    "questions": [
        {
            "question_title": "Which brilliant Carthaginian general famously crossed the Alps with war elephants to attack Rome?",
            "answers": [
                ["Hannibal Barca", "Yes. Hannibal infamously invaded Italy during the Second Punic War, winning the Battle of Cannae.", True, "None"],
                ["Hamilcar Barca", "None", False, "No."],
                ["Scipio Africanus", "None", False, "No."],
                ["Hasdrubal", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Religion and Culture",
    "description": "Explore the deities and spiritual life of the Roman people.",
    "questions": [
        {
            "question_title": "Who was the king of the gods in Roman mythology, equivalent to the Greek god Zeus?",
            "answers": [
                ["Mars", "None", False, "No."],
                ["Neptune", "None", False, "No."],
                ["Jupiter", "Yes. Jupiter was the god of the sky and thunder, and the chief deity of the Roman state.", True, "None"],
                ["Apollo", "None", False, "No."]
            ]
        }
    ]
} 
 
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