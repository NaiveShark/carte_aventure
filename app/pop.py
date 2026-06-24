from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Quest, Question, AnswerVar, CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS

# CONST map questions
CONST_QUESTS_MAP = [

   { "name" : "Do you know the Roman Empire's age geography?",
      "description" : "Do you know the geography  of ancient Roman Empire? ![SQPQR](https://upload.wikimedia.org/wikipedia/commons/d/d5/SPQR_skjaldamerki_R%C3%B3maveldis.png)",
      "questions" : [
          { "question_title" : "What was this city named during most of the period of Roman rule in Britannia?",
             "question_map_X" : 0,
             "question_map_Y" : 51.5,
             "question_map_ZOOM" : 12,
             "answers" : [
              [ "London", None, False, "No." ],
              [ "Landum", None, False, "No." ],
              [ "Londinium", "Yes.", True, None ],
              [ "Londonum", None, False, "No." ],
              [ "Caesarpolis", None, False, "No." ],
          ] },

          { "question_title" : "What was the name of the ancient Phoenician city located here that was destroyed after the Punic War?",
             "question_map_X" : 10.3233,
             "question_map_Y" : 36.8528,
             "question_map_ZOOM" : 10,
             "answers" : [
              [ "Byblos", None, False, "No." ],
              [ "Tyre", None, False, "No." ],
              [ "Carthage", "Yes.", True, None ],
              [ "Ugarit", None, False, "No." ],
              [ "Sidon", None, False, "No." ],
          ] },

          { "question_title" : "When did the eruption that destroyed Pompeii and Herculaneum occur?",
             "question_map_X" : 14.442778,
             "question_map_Y" : 40.821389,
             "question_map_ZOOM" : 13,
             "answers" : [
              [ "79 BC", None, False, "No." ],
              [ "97 BC", None, False, "No." ],
              [ "79 AD", "Yes.", True, None ],
              [ "97 AD", None, False, "No." ],
          ] },


          ]
     },
    ]

# CONST standart questions
CONST_QUESTS_TEXT = [
    { "name" : "Do you know the planets?",
      "description" : "Do you know the planets of *Solar system*? ![Solar system](https://upload.wikimedia.org/wikipedia/commons/5/5b/Solar_System_XXIX.png)",
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
              ] },

          { "question_title" : "Which planet is known as the Red Planet?",
            "answers" : [
              [ "Venus", None, False, "No, Venus is the brightest planet." ],
              [ "Mars", "Yes", True, None ],
              [ "Jupiter", None, False, "No, Jupiter is the largest gas giant." ],
              [ "Mercury", None, False, "No, Mercury is closest to the Sun." ]
              ] },
          { "question_title" : "Which planet is the largest in the Solar System?",
            "answers" : [
              [ "Saturn", None, False, "No, Saturn is the second largest." ],
              [ "Neptune", None, False, "No, Neptune is smaller than Uranus." ],
              [ "Jupiter", "Yes", True, None ],
              [ "Earth", None, False, "No, Earth is the largest terrestrial planet but much smaller than gas giants." ]
              ] },
          { "question_title" : "What is the hottest planet in our Solar System?",
            "answers" : [
              [ "Mercury", None, False, "No, despite being closest to the Sun, it has no atmosphere to trap heat." ],
              [ "Mars", None, False, "No, Mars is actually very cold." ],
              [ "Venus", "Yes", True, None ],
              [ "Jupiter", None, False, "No, Jupiter is a cold gas giant." ]
              ] },
          { "question_title" : "Which planet is famous for its large, prominent ring system?",
            "answers" : [
              [ "Uranus", None, False, "No, Uranus has rings, but they are faint." ],
              [ "Saturn", "Yes", True, None ],
              [ "Neptune", None, False, "No, Neptune's rings are very dark and thin." ],
              [ "Mars", None, False, "No, Mars has no rings." ]
              ] },

          { "question_title" : "Which celestial body was reclassified as a dwarf planet in 2006?",
            "answers" : [
              [ "Ceres", None, False, "No, Ceres was already considered an asteroid before becoming a dwarf planet." ],
              [ "Pluto", "Yes", True, None ],
              [ "Eris", None, False, "No, Eris was discovered around that time, forcing the new definition." ],
              [ "Mercury", None, False, "No, Mercury is a major terrestrial planet." ]
              ] },
          { "question_title" : "Which planet does the moon 'Europa', which has a subsurface ocean, orbit?",
            "answers" : [
              [ "Saturn", None, False, "No, Saturn's famous ocean moon is Enceladus." ],
              [ "Mars", None, False, "No, Mars only has two small, dry moons." ],
              [ "Jupiter", "Yes", True, None ],
              [ "Neptune", None, False, "No, Neptune's largest moon is Triton." ]
              ] },
          { "question_title" : "Which space probe was the first to visit and photograph Pluto in 2015?",
            "answers" : [
              [ "Voyager 1", None, False, "No, Voyager 1 left the Solar System without visiting Pluto." ],
              [ "Cassini", None, False, "No, Cassini spent its mission studying Saturn." ],
              [ "New Horizons", "Yes", True, None ],
              [ "Curiosity", None, False, "No, Curiosity is a rover operating on Mars." ]
              ] },


              ]
      },

    { "name" : "Do you know the Roman Empire?",
      "description" : "Do you know the history of ancient Roman Empire? ![SQPQR](https://upload.wikimedia.org/wikipedia/commons/d/d5/SPQR_skjaldamerki_R%C3%B3maveldis.png)",
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
    "description": "Questions about Rome's legendary conflicts with Carthage. ![](https://upload.wikimedia.org/wikipedia/commons/c/c8/TSC_hannibal_elephant.jpg))",
    "questions": [
        {
            "question_title": "Which brilliant Carthaginian general famously crossed the Alps with war elephants to attack Rome?",
            "answers": [
                ["Scipio Africanus", "None", False, "No."],
                ["Hamilcar Barca", "None", False, "No."],
                ["Hannibal Barca", "Yes. Hannibal infamously invaded Italy during the Second Punic War, winning the Battle of Cannae.", True, "None"],
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

    for cqm in CONST_QUESTS_MAP:
        quest = Quest( name = cqm["name"], description = cqm["description"], is_active = True  )
        DB.add( quest )
        await DB.commit()
        for qd in cqm["questions"]:
            q = Question( question_title = qd["question_title"],
                              question_type = CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS,
                              question_map_X = qd["question_map_X"],
                              question_map_Y = qd["question_map_Y"],
                              question_map_ZOOM = qd["question_map_ZOOM"],
                          quest_id = quest.id )
            DB.add( q )
            await DB.commit()
            if qd.get("answers"):
                for answer in qd.get("answers"):
                    a = AnswerVar( answer_title = answer[0], question_id = q.id, right_message = answer[1], is_true_answer = answer[2], wrong_message = answer[3] )
                    DB.add( a )
                    await DB.commit()


    for сq_d in CONST_QUESTS_TEXT:
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