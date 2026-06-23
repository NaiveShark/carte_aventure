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
},


{
    "name": "Roman Baths and Leisure",
    "description": "Explore the daily relaxation habits and social hubs of Roman citizens.",
    "questions": [
        {
            "question_title": "What was the name of the hot room in a traditional Roman bathhouse complex?",
            "answers": [
                ["Frigidarium", "None", False, "No."],
                ["Tepidarium", "None", False, "No."],
                ["Caldarium", "Yes. The caldarium was the hot, steamy room heated by an underground hypocaust system.", True, "None"],
                ["Apodyterium", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Entertainment",
    "description": "Test your knowledge on chariot racing and stadium spectacles.",
    "questions": [
        {
            "question_title": "Where did chariot races primarily take place in the city of Ancient Rome?",
            "answers": [
                ["Circus Maximus", "Yes. The Circus Maximus could hold over 150,000 spectators for thrilling chariot races.", True, "None"],
                ["The Colosseum", "None", False, "No."],
                ["The Theatre of Marcellus", "None", False, "No."],
                ["The Curia", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Engineering",
    "description": "Questions about the physical infrastructure that supported Roman life.",
    "questions": [
        {
            "question_title": "What volcanic ash-based material allowed Romans to build massive concrete structures underwater?",
            "answers": [
                ["Marble", "None", False, "No."],
                ["Pozzolana", "Yes. Pozzolana ash reacted chemically with lime to create incredibly durable, water-resistant concrete.", True, "None"],
                ["Granite", "None", False, "No."],
                ["Limestone", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Clothing",
    "description": "Learn about the social status garments worn by Roman citizens.",
    "questions": [
        {
            "question_title": "Which garment was a symbol of Roman citizenship and forbidden to be worn by foreigners or slaves?",
            "answers": [
                ["Tunic", "None", False, "No."],
                ["Chiton", "None", False, "No."],
                ["Toga", "Yes. The toga was the formal woolen garment reserved exclusively for free male Roman citizens.", True, "None"],
                ["Stola", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Domestic Life",
    "description": "Discover the structure of ancient Roman households and families.",
    "questions": [
        {
            "question_title": "What term refers to the absolute legal authority held by the male head of a Roman family?",
            "answers": [
                ["Patria Potestas", "Yes. Patria Potestas gave the male head of household complete legal power over his children and descendants.", True, "None"],
                ["Cursus Honorum", "None", False, "No."],
                ["Mos Maiorum", "None", False, "No."],
                ["Clientela", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Literature",
    "description": "Quiz yourself on the epic writers of the Golden Age of Roman literature.",
    "questions": [
        {
            "question_title": "Who wrote the national epic poem 'The Aeneid', detailing the journey of a Trojan hero to Italy?",
            "answers": [
                ["Ovid", "None", False, "No."],
                ["Horace", "None", False, "No."],
                ["Virgil", "Yes. Virgil wrote the Aeneid during the reign of Augustus to glorify Rome's divine origins.", True, "None"],
                ["Cicero", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Housing",
    "description": "Explore the contrasting living conditions between rich and poor Romans.",
    "questions": [
        {
            "question_title": "What was the name of the multi-story, crowded apartment buildings where lower-class Romans lived?",
            "answers": [
                ["Domus", "None", False, "No."],
                ["Insulae", "Yes. Insulae were apartment blocks that housed the majority of Rome's urban population, often prone to fires.", True, "None"],
                ["Villa", "None", False, "No."],
                ["Atrium", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Mythology",
    "description": "Delve into the gods protecting the Roman household.",
    "questions": [
        {
            "question_title": "What were the Lares and Penates in ancient Roman cultural beliefs?",
            "answers": [
                ["Military ranks", "None", False, "No."],
                ["Household gods", "Yes. The Lares and Penates were domestic guardian spirits worshipped daily at family shrines called lararia.", True, "None"],
                ["Gladiator types", "None", False, "No."],
                ["Types of wine", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Festivals",
    "description": "Uncover the wild celebrations of the Roman calendar.",
    "questions": [
        {
            "question_title": "Which December winter festival involved role reversals, where masters served meals to their slaves?",
            "answers": [
                ["Lupercalia", "None", False, "No."],
                ["Saturnalia", "Yes. Saturnalia was a joyful festival honoring Saturn, marked by feasting, gift-giving, and temporary social equality.", True, "None"],
                ["Liberalia", "None", False, "No."],
                ["Lemuria", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Food and Drink",
    "description": "Discover the unique culinary tastes of ancient Rome.",
    "questions": [
        {
            "question_title": "What highly popular fermented fish sauce was used as a universal condiment in Roman cuisine?",
            "answers": [
                ["Garum", "Yes. Garum was made by fermenting fish intestines in brine and was added to both sweet and savory dishes.", True, "None"],
                ["Posca", "None", False, "No."],
                ["Mulsum", "None", False, "No."],
                ["Defrutum", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Gladiatorial Culture",
    "description": "Test your knowledge on the fighters of the arena.",
    "questions": [
        {
            "question_title": "Which specific type of gladiator fought using a fishing net and a three-pronged trident?",
            "answers": [
                ["Murmillo", "None", False, "No."],
                ["Secutor", "None", False, "No."],
                ["Retiarius", "Yes. The Retiarius was lightly armored and relied on speed to ensnare heavily armed opponents like the Secutor.", True, "None"],
                ["Thraex", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Philosophy",
    "description": "Examine the moral frameworks that guided Roman politicians and emperors.",
    "questions": [
        {
            "question_title": "Which Hellenistic philosophy, emphasizing duty, self-control, and reason, became dominant among elite Romans?",
            "answers": [
                ["Epicureanism", "None", False, "No."],
                ["Stoicism", "Yes. Stoicism heavily influenced Roman culture, appealing to their traditional values of gravity and discipline.", True, "None"],
                ["Cynicism", "None", False, "No."],
                ["Skepticism", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Education",
    "description": "Learn how young Romans were prepared for public life.",
    "questions": [
        {
            "question_title": "What subject was considered the pinnacle of higher education for a young Roman nobleman planning a political career?",
            "answers": [
                ["Rhetoric", "Yes. Rhetoric, the art of public speaking and persuasion, was vital for winning court cases and political debates.", True, "None"],
                ["Geometry", "None", False, "No."],
                ["Astronomy", "None", False, "No."],
                ["Medicine", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Marriage",
    "description": "Explore the social contracts and ceremonies of Roman unions.",
    "questions": [
        {
            "question_title": "What was the traditional white bridal dress worn by Roman women on their wedding day?",
            "answers": [
                ["Tunica Recta", "Yes. The tunica recta was woven traditionally on an upright loom and tied with a special knot of Hercules.", True, "None"],
                ["Toga Pulla", "None", False, "No."],
                ["Paludamentum", "None", False, "No."],
                ["Subligaculum", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Roads and Commute",
    "description": "Understand how information and military power moved through the empire.",
    "questions": [
        {
            "question_title": "What was the name of the ancient state-run courier and postal service of the Roman Empire?",
            "answers": [
                ["Cursus Publicus", "Yes. Established by Augustus, the Cursus Publicus used a network of relay stations for fast imperial communication.", True, "None"],
                ["Via Appia", "None", False, "No."],
                ["Vigiles", "None", False, "No."],
                ["Praetorian Guard", "None", False, "No."]
            ]
        }
    ]
},


{
    "name": "Roman Baths and Leisure",
    "description": "Explore the daily relaxation habits and social hubs of Roman citizens.",
    "questions": [
        {
            "question_title": "What was the name of the hot room in a traditional Roman bathhouse complex?",
            "answers": [
                ["Frigidarium", "None", False, "No."],
                ["Tepidarium", "None", False, "No."],
                ["Caldarium", "Yes. The caldarium was the hot, steamy room heated by an underground hypocaust system.", True, "None"],
                ["Apodyterium", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Entertainment",
    "description": "Test your knowledge on chariot racing and stadium spectacles.",
    "questions": [
        {
            "question_title": "Where did chariot races primarily take place in the city of Ancient Rome?",
            "answers": [
                ["Circus Maximus", "Yes. The Circus Maximus could hold over 150,000 spectators for thrilling chariot races.", True, "None"],
                ["The Colosseum", "None", False, "No."],
                ["The Theatre of Marcellus", "None", False, "No."],
                ["The Curia", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Engineering",
    "description": "Questions about the physical infrastructure that supported Roman life.",
    "questions": [
        {
            "question_title": "What volcanic ash-based material allowed Romans to build massive concrete structures underwater?",
            "answers": [
                ["Marble", "None", False, "No."],
                ["Pozzolana", "Yes. Pozzolana ash reacted chemically with lime to create incredibly durable, water-resistant concrete.", True, "None"],
                ["Granite", "None", False, "No."],
                ["Limestone", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Clothing",
    "description": "Learn about the social status garments worn by Roman citizens.",
    "questions": [
        {
            "question_title": "Which garment was a symbol of Roman citizenship and forbidden to be worn by foreigners or slaves?",
            "answers": [
                ["Tunic", "None", False, "No."],
                ["Chiton", "None", False, "No."],
                ["Toga", "Yes. The toga was the formal woolen garment reserved exclusively for free male Roman citizens.", True, "None"],
                ["Stola", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Domestic Life",
    "description": "Discover the structure of ancient Roman households and families.",
    "questions": [
        {
            "question_title": "What term refers to the absolute legal authority held by the male head of a Roman family?",
            "answers": [
                ["Patria Potestas", "Yes. Patria Potestas gave the male head of household complete legal power over his children and descendants.", True, "None"],
                ["Cursus Honorum", "None", False, "No."],
                ["Mos Maiorum", "None", False, "No."],
                ["Clientela", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Literature",
    "description": "Quiz yourself on the epic writers of the Golden Age of Roman literature.",
    "questions": [
        {
            "question_title": "Who wrote the national epic poem 'The Aeneid', detailing the journey of a Trojan hero to Italy?",
            "answers": [
                ["Ovid", "None", False, "No."],
                ["Horace", "None", False, "No."],
                ["Virgil", "Yes. Virgil wrote the Aeneid during the reign of Augustus to glorify Rome's divine origins.", True, "None"],
                ["Cicero", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Housing",
    "description": "Explore the contrasting living conditions between rich and poor Romans.",
    "questions": [
        {
            "question_title": "What was the name of the multi-story, crowded apartment buildings where lower-class Romans lived?",
            "answers": [
                ["Domus", "None", False, "No."],
                ["Insulae", "Yes. Insulae were apartment blocks that housed the majority of Rome's urban population, often prone to fires.", True, "None"],
                ["Villa", "None", False, "No."],
                ["Atrium", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Mythology",
    "description": "Delve into the gods protecting the Roman household.",
    "questions": [
        {
            "question_title": "What were the Lares and Penates in ancient Roman cultural beliefs?",
            "answers": [
                ["Military ranks", "None", False, "No."],
                ["Household gods", "Yes. The Lares and Penates were domestic guardian spirits worshipped daily at family shrines called lararia.", True, "None"],
                ["Gladiator types", "None", False, "No."],
                ["Types of wine", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Festivals",
    "description": "Uncover the wild celebrations of the Roman calendar.",
    "questions": [
        {
            "question_title": "Which December winter festival involved role reversals, where masters served meals to their slaves?",
            "answers": [
                ["Lupercalia", "None", False, "No."],
                ["Saturnalia", "Yes. Saturnalia was a joyful festival honoring Saturn, marked by feasting, gift-giving, and temporary social equality.", True, "None"],
                ["Liberalia", "None", False, "No."],
                ["Lemuria", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Food and Drink",
    "description": "Discover the unique culinary tastes of ancient Rome.",
    "questions": [
        {
            "question_title": "What highly popular fermented fish sauce was used as a universal condiment in Roman cuisine?",
            "answers": [
                ["Garum", "Yes. Garum was made by fermenting fish intestines in brine and was added to both sweet and savory dishes.", True, "None"],
                ["Posca", "None", False, "No."],
                ["Mulsum", "None", False, "No."],
                ["Defrutum", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Gladiatorial Culture",
    "description": "Test your knowledge on the fighters of the arena.",
    "questions": [
        {
            "question_title": "Which specific type of gladiator fought using a fishing net and a three-pronged trident?",
            "answers": [
                ["Murmillo", "None", False, "No."],
                ["Secutor", "None", False, "No."],
                ["Retiarius", "Yes. The Retiarius was lightly armored and relied on speed to ensnare heavily armed opponents like the Secutor.", True, "None"],
                ["Thraex", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Philosophy",
    "description": "Examine the moral frameworks that guided Roman politicians and emperors.",
    "questions": [
        {
            "question_title": "Which Hellenistic philosophy, emphasizing duty, self-control, and reason, became dominant among elite Romans?",
            "answers": [
                ["Epicureanism", "None", False, "No."],
                ["Stoicism", "Yes. Stoicism heavily influenced Roman culture, appealing to their traditional values of gravity and discipline.", True, "None"],
                ["Cynicism", "None", False, "No."],
                ["Skepticism", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Education",
    "description": "Learn how young Romans were prepared for public life.",
    "questions": [
        {
            "question_title": "What subject was considered the pinnacle of higher education for a young Roman nobleman planning a political career?",
            "answers": [
                ["Rhetoric", "Yes. Rhetoric, the art of public speaking and persuasion, was vital for winning court cases and political debates.", True, "None"],
                ["Geometry", "None", False, "No."],
                ["Astronomy", "None", False, "No."],
                ["Medicine", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Marriage",
    "description": "Explore the social contracts and ceremonies of Roman unions.",
    "questions": [
        {
            "question_title": "What was the traditional white bridal dress worn by Roman women on their wedding day?",
            "answers": [
                ["Tunica Recta", "Yes. The tunica recta was woven traditionally on an upright loom and tied with a special knot of Hercules.", True, "None"],
                ["Toga Pulla", "None", False, "No."],
                ["Paludamentum", "None", False, "No."],
                ["Subligaculum", "None", False, "No."]
            ]
        }
    ]
},
{
    "name": "Roman Roads and Commute",
    "description": "Understand how information and military power moved through the empire.",
    "questions": [
        {
            "question_title": "What was the name of the ancient state-run courier and postal service of the Roman Empire?",
            "answers": [
                ["Cursus Publicus", "Yes. Established by Augustus, the Cursus Publicus used a network of relay stations for fast imperial communication.", True, "None"],
                ["Via Appia", "None", False, "No."],
                ["Vigiles", "None", False, "No."],
                ["Praetorian Guard", "None", False, "No."]
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