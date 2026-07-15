from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User, Quest, Question, AnswerVar, CONST_QUEST_TREASURE_QUEST, CONST_QUESTION_TYPE_MAP_POINT_AND_TEXT_VARS, CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER, News_Feed

from datetime import datetime

BOT_USER_NAME = 'Naive_shark_bot'
BOT_USER_TITLE = 'Naive shark bot'

# Treasure quest!
CONST_TREASURE_QUEST = [

   { "name" : "Are you ready for treasure quest?",
      "description" : "Treasure hunt! An unknown wealthy individual has hidden a mysterious treasure somewhere on the globe. Pinpoint the location on the map where it’s hidden! Finding it on the first try is impossible, but keep an eye on the spots marked by other players—and remember, they can see yours, too. Decide for yourself: is this a race against the clock, or a collaborative effort?",
     } ,

   { "name" : "Are you ready for UFO quest?",
      "description" : "Alien hunt! An unknown space traveler has parked a glowing craft somewhere on Earth. Pinpoint its beam on your radar map. Getting it right on your first try is very rare. Watch the glowing lights dropped by other alien seekers—and remember, they can see yours too. You must decide: is this a frantic race, or a shared mission?",
     } ,

   { "name" : "Spy Thriller Spin",
      "description" : "Top secret! A rogue spy has stashed a glowing microchip somewhere on the globe. Pinpoint the site on the intelligence map! Finding it on the first try is impossible, but keep a close eye on the safehouses marked by other agents—and remember, they can see yours, too. Decide for yourself: is this a race against the clock, or a collaborative effort?",
     } ,

   { "name" : "Secret Agency Recruitment Spin",
      "description" : "Agent selection! An unidentified subject has hidden a classified archive somewhere on the globe. Pinpoint the coordinates on the operational map. Locating it on your first attempt is impossible. Track the visual markers dropped by rival candidates—and remember, they can monitor your progress too. Decide your strategy: is this a high-speed elimination race, or a joint special operation?",
     } ,

   { "name" : "The Bigfoot Tracker",
      "description" : "Monster hunt! An elusive, undiscovered beast has vanished into the wilderness somewhere on the globe. Pinpoint its nesting ground on your field map! Catching a glimpse on your first try is impossible. Track the footprints left by rival cryptid hunters—and remember, they are tracking yours, too. Decide your strategy: is this a solo race for the ultimate discovery, or a shared expedition?",
     } ,

   { "name" : "The Paranormal Investigator",
      "description" : "Anomaly detected! A legendary cryptid has crossed over into our world somewhere on the planet. Pinpoint the anomaly's origin on your radar! Locking onto its signal on your first attempt is impossible. Monitor the heat signatures marked by other paranormal investigators—and remember, they can see your grid, too. Decide for yourself: is this a frantic race against the clock, or a collaborative investigation?",
     } ,

   { "name" : "The Mythic Cartographer ",
      "description" : "Mythical expedition! A creature thought to be extinct is nesting somewhere on the globe. Pinpoint the habitat on your research map! Finding the correct coordinates on your first try is impossible. Keep a close eye on the coordinates logged by other cryptozoologists—and remember, they can see your data, too. Is this a competitive race for scientific glory, or a joint global research effort?",
     } ,


]

# CONST map questions
CONST_QUESTS_MAP = [

 {
    "name": "Stonehenge and Ancient Sights of Britain & Ireland",
    "description": "Test your knowledge on the mysterious stone circles, tombs, and ancient monuments of the British Isles! Discover structures older than the Egyptian pyramids, built by prehistoric societies using massive megaliths aligned with solar and lunar cycles. ![Stonehenge](https://upload.wikimedia.org/wikipedia/commons/5/57/Menir%2C_Stonehenge%2C_Inglaterra_.jpg)",
    "questions": [
        {
            "question_title": "Which Famous Neolithic stone circle is located here in Wiltshire, England? Constructed over several phases starting around 3000 BC, its massive sarsen stones and smaller bluestones were transported from miles away, serving as a complex burial ground and an astronomical observatory.",
            "question_map_X": -1.8262,
            "question_map_Y": 51.1789,
            "question_map_ZOOM": 14,
            "answers": [
                [ "Avebury", None, False, "No, Avebury is larger but located further north." ],
                [ "Stonehenge", "Yes! This iconic monument remains a masterpiece of engineering.", True, None ],
                [ "Newgrange", None, False, "No, Newgrange is a passage tomb located in Ireland." ],
                [ "Callanish", None, False, "No, the Callanish Stones are situated in Scotland." ],
                [ "Bryn Celli Ddu", None, False, "No, this is a famous passage tomb found in Wales." ],
            ]
        },
        {
            "question_title": "What is the name of this massive prehistoric tomb in County Meath, Ireland? Built around 3200 BC during the Neolithic period, this grand passage tomb features a unique roof box designed to illuminate the inner chamber with sunrise light during the winter solstice.",
            "question_map_X": -6.4444,
            "question_map_Y": 53.6947,
            "question_map_ZOOM": 13,
            "answers": [
                [ "Knowth", None, False, "No, Knowth is nearby but features different art and structures." ],
                [ "Dowth", None, False, "No, Dowth is part of the same complex but remains unexcavated." ],
                [ "Tara", None, False, "No, the Hill of Tara was the ancient seat of the High Kings." ],
                [ "Newgrange", "Yes! It is one of the most famous megalithic structures globally.", True, None ],
                [ "Poulnabrone", None, False, "No, Poulnabrone is a portal dolmen located in County Clare." ],
            ]
        },
        {
            "question_title": "Place the dot on the map where you think Avebury is located—the largest megalithic stone circle in the world. Dating from roughly 2850 BC to 2200 BC, this massive henge encloses a village, multiple stone avenues, and was used for ritual ceremonies.",
            "question_map_X": -2,
            "question_map_Y": 52,
            "question_map_ZOOM": 6,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot on the map very close to Avebury, which sits just north of Stonehenge in Wiltshire.",
                    "true_answer_map_X": -1.8592,
                    "true_answer_map_Y": 51.4286,
                    "right_message": "Yes, perfect accuracy!",
                    "wrong_message": "No, Avebury is located in Wiltshire, southern England."
                },
            ]
        },
        {
            "question_title": "This remote island chain holds the Callanish Stones, a cross-shaped setting of megaliths erected 5,000 years ago. Serving as a crucial ritual center for generations, place the dot on this historic Scottish site on the Isle of Lewis.",
            "question_map_X": -4,
            "question_map_Y": 56,
            "question_map_ZOOM": 5,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot right on the Outer Hebrides where the magnificent Callanish Stones stand.",
                    "true_answer_map_X": -6.7454,
                    "true_answer_map_Y": 58.1978,
                    "right_message": "Yes, excellent geographical knowledge!",
                    "wrong_message": "No, look further northwest toward the outer Scottish islands."
                },
            ]
        },

        {
            "question_title": "What is the name of this remarkably preserved Neolithic village in the Orkney Islands, Scotland? Occupied between 3180 BC and 2500 BC, it features stone-built houses with integrated beds, hearths, and cupboards, earning it the title of 'British Pompeii'.",
            "question_map_X": -3.3421,
            "question_map_Y": 59.0486,
            "question_map_ZOOM": 14,
            "answers": [
                [ "Jarlshof", None, False, "No, Jarlshof is a complex archaeological site in Shetland." ],
                [ "Maeshowe", None, False, "No, Maeshowe is a chambered cairn located nearby." ],
                [ "Skara Brae", "Yes! It offers an unparalleled glimpse into European Stone Age domestic life.", True, None ],
                [ "Knap of Howar", None, False, "No, though it is another ancient farmstead in Orkney." ],
                [ "Grime's Graves", None, False, "No, Grime's Graves is an ancient flint mining site in England." ],
            ]
        },
        {
            "question_title": "Place the dot on the map where you think Maiden Castle is located. This massive site is one of the largest and most complex Iron Age hillforts in Europe, featuring immense, labyrinthine earthen ramparts constructed around the 1st century BC to protect its thriving tribal community.",
            "question_map_X": -3,
            "question_map_Y": 50,
            "question_map_ZOOM": 7,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot right near Dorchester in Dorset, England, where this colossal hillfort stands.",
                    "true_answer_map_X": -2.4682,
                    "true_answer_map_Y": 50.6953,
                    "right_message": "Yes, superb spotting!",
                    "wrong_message": "No, Maiden Castle is located in Dorset, in the southwestern part of England."
                },
            ]
        },
        {
            "question_title": "What is the name of this famous prehistoric monument on the island of Anglesey, Wales? Meaning 'The Mound in the Dark Grove', it began as a henge monument around 3000 BC before being transformed into a passage tomb accurately aligned with the summer solstice sunrise.",
            "question_map_X": -4.2800,
            "question_map_Y": 53.2000,
            "question_map_ZOOM": 12,
            "answers": [
                [ "Pentre Ifan", None, False, "No, Pentre Ifan is a famous dolmen located in Pembrokeshire, South Wales." ],
                [ "Barclodiad y Gawres", None, False, "No, that is a different cruciform passage grave nearby on Anglesey." ],
                [ "Bryn Celli Ddu", "Yes! It is one of Wales' most iconic and archaeologically significant prehistoric sites.", True, None ],
                [ "Tinkinswood", None, False, "No, Tinkinswood is a megalithic burial chamber situated in South Wales." ],
                [ "Gop Cairn", None, False, "No, Gop Cairn is a massive enigmatic mound located in Flintshire." ],
            ],
        },
]
    },


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

          { "question_title" : "The Battle of Messana in 264 BC was the first military clash between the Roman Republic and Carthage.",
             "question_map_X" : 15,
             "question_map_Y" : 41,
             "question_map_ZOOM" : 4,
             "dot_answer" : [
              { "dot_question" : "Yes, you've placed the dot on the map very close to the target place.",
                "true_answer_map_X" : 15.5614,
                "true_answer_map_Y" : 38.18,
                "right_message" : "Yes.",
                "wrong_message" : "No",
              },
          ] },

          { "question_title" : "The Battle of the Aegates was a naval battle fought on 10 March 241 BC between the fleets of Carthage and Rome during the First Punic War. It took place among the Aegates Islands, off the western coast of the island of Sicily. It was the final and deciding battle of the 23-year-long First Punic War. Place the dot on map there it was occure.",
             "question_map_X" : 11,
             "question_map_Y" : 39,
             "question_map_ZOOM" : 4,
             "dot_answer" : [
              { "dot_question" : "Yes, you've placed the dot on the map very close to the target place.",
                "true_answer_map_X" : 12.2,
                "true_answer_map_Y" : 37.97,
                "right_message" : "Yes.",
                "wrong_message" : "No",
              },
          ] },

          { "question_title" : "Where is the westernmost point of the Roman Empire on the continental mainland?",
             "question_map_X" : -10,
             "question_map_Y" : 39,
             "question_map_ZOOM" : 8,
             "dot_answer" : [
              { "dot_question" : "Yes, you've placed the dot on the map very close to the target place. It's a Cabo da Roca, now Portugal, westernmost point of continental Europe.",
                "true_answer_map_X" : -9.500556,
                "true_answer_map_Y" : 38.780833,
                "right_message" : "Yes.",
                "wrong_message" : "No",
              },
          ] },
          ]
     }  ,

{
    "name": "Iceland History, Geography & Ancient Travels",
    "description": "Test your knowledge on the land of fire and ice, Viking settlements, and ancient North Atlantic voyages! ![Iceland](https://upload.wikimedia.org/wikipedia/commons/a/ab/Iceland_%286111906083%29.jpg)",
    "questions": [
        {
            "question_title": "Where did Iceland's historic Althing (parliament) meet from 930 AD until 1798?",
            "question_map_X": -21.12,
            "question_map_Y": 64.25,
            "question_map_ZOOM": 11,
            "answers": [
                [ "Reykjavík", None, False, "No." ],
                [ "Þingvellir (Thingvellir)", "Yes.", True, None ],
                [ "Akureyri", None, False, "No." ],
                [ "Húsavík", None, False, "No." ],
                [ "Skálholt", None, False, "No." ]
            ]
        },

        {
            "question_title": "In 1783, a massive, catastrophic volcanic eruption began here, creating a global climate crisis. What was the name of the fissure system?",
            "question_map_X": -18.23,
            "question_map_Y": 64.06,
            "question_map_ZOOM": 10,
            "answers": [
                [ "Eyjafjallajökull", None, False, "No." ],
                [ "Katla", None, False, "No." ],
                [ "Hekla", None, False, "No." ],
                [ "Laki", "Yes.", True, None ],
                [ "Askja", None, False, "No." ]
            ]
        },

        {
            "question_title": "Leif Erikson sailed from Iceland and established a settlement in Vinland (North America) around 1000 AD. Where is this modern-day archaeological site located?",
            "question_map_X": -55.53,
            "question_map_Y": 51.59,
            "question_map_ZOOM": 12,
            "answers": [
                [ "Greenland", None, False, "No." ],
                [ "Baffin Island", None, False, "No." ],
                [ "L'Anse aux Meadows", "Yes.", True, None ],
                [ "Cape Cod", None, False, "No." ]
            ]
        },

        {
            "question_title": "The Sagas state that Ingólfur Arnarson became the first permanent Norse settler in Iceland around 874 AD. Place a dot on the map where he founded his settlement, which later became Iceland's capital.",
            "question_map_X": -22,
            "question_map_Y": 65,
            "question_map_ZOOM": 6,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot on the map very close to the target place.",
                    "true_answer_map_X": -21.9426,
                    "true_answer_map_Y": 64.1466,
                    "right_message": "Yes, this is Reykjavík.",
                    "wrong_message": "No"
                }
            ]
        },

        {
            "question_title": "Erik the Red fled Iceland after being outlawed for manslaughter and went on to establish the first Norse settlement in Greenland. Place a dot on the southwestern coast of Greenland where his estate, Brattahlíð, was founded.",
            "question_map_X": -45.0,
            "question_map_Y": 62.0,
            "question_map_ZOOM": 6,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot on the map very close to the target place.",
                    "true_answer_map_X": -45.5186,
                    "true_answer_map_Y": 61.1558,
                    "right_message": "Yes, this is the Eastern Settlement area (Tunulliarfik Fjord).",
                    "wrong_message": "No"
                }
            ]
        },

        {
            "question_title": "Where is the northernmost point of mainland Iceland, located just a few kilometers south of the Arctic Circle?",
            "question_map_X": -17,
            "question_map_Y": 66,
            "question_map_ZOOM": 8,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot on the map very close to the target place. It's Hraunhafnartangi, the northernmost point of the mainland.",
                    "true_answer_map_X": -16.5411,
                    "true_answer_map_Y": 66.5375,
                    "right_message": "Yes.",
                    "wrong_message": "No"
                }
            ]
        },



        {
            "question_title": "According to the Landnámabók (Book of Settlements), this Irish-born Viking was the first to intentionally sail to Iceland and spend a winter there, naming it 'Garðarshólmur' after himself. Where did he land?",
            "question_map_X": -17.3,
            "question_map_Y": 66.0,
            "question_map_ZOOM": 10,
            "answers": [
                [ "Reykjavík", None, False, "No." ],
                [ "Húsavík", "Yes.", True, None ],
                [ "Seyðisfjörður", None, False, "No." ],
                [ "Vestmannaeyjar", None, False, "No." ]
            ]
        },
        {
            "question_title": "Iceland sits directly on top of the meeting point between two massive tectonic plates that are pulling apart. What are these two plates?",
            "question_map_X": -19.0,
            "question_map_Y": 65.0,
            "question_map_ZOOM": 6,
            "answers": [
                [ "Pacific and North American", None, False, "No." ],
                [ "Eurasian and African", None, False, "No." ],
                [ "North American and Eurasian", "Yes.", True, None ],
                [ "Nazca and South American", None, False, "No." ]
            ]
        },
        {
            "question_title": "In 1963, a brand new island was born off the southern coast of Iceland due to a massive underwater volcanic eruption. What is the name of this UNESCO protected island?",
            "question_map_X": -20.6,
            "question_map_Y": 63.3,
            "question_map_ZOOM": 11,
            "answers": [
                [ "Heimaey", None, False, "No." ],
                [ "Surtsey", "Yes.", True, None ],
                [ "Grimsey", None, False, "No." ],
                [ "Flatey", None, False, "No." ]
            ]
        },
        {
            "question_title": "Where is the legendary active volcano Hekla located, which was feared in medieval Europe and often called the 'Gateway to Hell'?",
            "question_map_X": -19.66,
            "question_map_Y": 63.99,
            "question_map_ZOOM": 10,
            "answers": [
                [ "Hekla", "Yes.", True, None ],
                [ "Katla", None, False, "No." ],
                [ "Katla", None, False, "No." ],
                [ "Krafla", None, False, "No." ]
            ]
        },
        {
            "question_title": "Before the Norse arrived, Iceland was briefly inhabited by Gaelic monks who sought absolute isolation for religious reflection. What were these early Christian hermits called?",
            "question_map_X": -14.5,
            "question_map_Y": 63.8,
            "question_map_ZOOM": 8,
            "answers": [
                [ "Skalds", None, False, "No." ],
                [ "Papar", "Yes.", True, None ],
                [ "Jarls", None, False, "No." ],
                [ "Thralls", None, False, "No." ]
            ]
        },

        # --- Dot Answers ---
        {
            "question_title": "Place the dot on Vatnajökull, the largest and most voluminous ice cap in Iceland (and one of the largest in Europe by area), which covers around 8% of the country.",
            "question_map_X": -16.8,
            "question_map_Y": 64.4,
            "question_map_ZOOM": 7,
            "dot_answer": [
                {
                    "dot_question": "Yes, you've placed the dot right on the massive Vatnajökull glacier.",
                    "true_answer_map_X": -16.81,
                    "true_answer_map_Y": 64.42,
                    "right_message": "Yes, this is Vatnajökull.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "The Snaefellsjökull volcano is famous worldwide as the entry point to the center of the Earth in Jules Verne's sci-fi novel 'Journey to the Center of the Earth'. Place the dot on the western tip of this peninsula.",
            "question_map_X": -23.7,
            "question_map_Y": 64.8,
            "question_map_ZOOM": 9,
            "dot_answer": [
                {
                    "dot_question": "Excellent! You've located the Snæfellsjökull glacier-capped volcano at the edge of the peninsula.",
                    "true_answer_map_X": -23.7766,
                    "true_answer_map_Y": 64.8081,
                    "right_message": "Yes, that's Snæfellsjökull.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "In the year 1000 AD, Iceland officially converted to Christianity at the Althing. To symbolize this, the Lawspeaker Thorgeir threw his pagan idols of the Norse gods into a spectacular waterfall. Place the dot on this 'Waterfall of the Gods' (Goðafoss) in northern Iceland.",
            "question_map_X": -17.5,
            "question_map_Y": 65.6,
            "question_map_ZOOM": 9,
            "dot_answer": [
                {
                    "dot_question": "Correct! You successfully located Goðafoss waterfall along the Skjálfandafljót river.",
                    "true_answer_map_X": -17.5502,
                    "true_answer_map_Y": 65.6828,
                    "right_message": "Yes, this is Goðafoss.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "Before discovering Greenland, Viking explorers used the Faroe Islands as a crucial stepping stone between Norway and Iceland. Place a dot on this small island archipelago in the middle of the North Atlantic.",
            "question_map_X": -6.7,
            "question_map_Y": 62.0,
            "question_map_ZOOM": 6,
            "dot_answer": [
                {
                    "dot_question": "Perfect! You found the Faroe Islands, the vital mid-way hub for ancient Norse longships.",
                    "true_answer_map_X": -6.78,
                    "true_answer_map_Y": 62.01,
                    "right_message": "Yes, these are the Faroe Islands.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "Where is the diamond-shaped black sand beach known as 'Diamond Beach' located, where glittering icebergs from the Jökulsárlón glacier lagoon wash ashore?",
            "question_map_X": -16.1,
            "question_map_Y": 64.0,
            "question_map_ZOOM": 11,
            "dot_answer": [
                {
                    "dot_question": "Great job! You pointed right to the outlet channel where the glacier lagoon meets the Atlantic ocean.",
                    "true_answer_map_X": -16.178,
                    "true_answer_map_Y": 64.043,
                    "right_message": "Yes, this is Diamond Beach.",
                    "wrong_message": "No"
                }
            ]
        },


        {
            "question_title": "Viking navigators used a mysterious crystal called a 'Sunstone' (silfrið berg) to find the sun's position even through thick fog or storm clouds. What local Icelandic mineral is this historically famous sunstone believed to be?",
            "question_map_X": -14.6,
            "question_map_Y": 65.0,
            "question_map_ZOOM": 10,
            "answers": [
                [ "Obsidian (Volcanic glass)", None, False, "No." ],
                [ "Iceland Spar (Optical Calcite)", "Yes.", True, None ],
                [ "Basalt", None, False, "No." ],
                [ "Sulfur", None, False, "No." ]
            ]
        },
        {
            "question_title": "In 1262, after decades of bloody internal civil war between powerful clans (the Age of the Sturlungs), Iceland lost its independence and signed an agreement submitting to the rule of which foreign king?",
            "question_map_X": 10.7,
            "question_map_Y": 59.9,
            "question_map_ZOOM": 5,
            "answers": [
                [ "King of Denmark", None, False, "No, Denmark came much later." ],
                [ "King of England", None, False, "No." ],
                [ "King of Norway", "Yes.", True, None ],
                [ "King of Sweden", None, False, "No." ]
            ]
        },
        {
            "question_title": "According to the Grœnlendinga saga, who was the very first Norse explorer to sight the coast of North America when his ship was blown off course in a storm, before Leif Erikson actually went there to build houses?",
            "question_map_X": -53.0,
            "question_map_Y": 47.0,
            "question_map_ZOOM": 4,
            "answers": [
                [ "Bjarni Herjólfsson", "Yes.", True, None ],
                [ "Thorvald Erikson", None, False, "No." ],
                [ "Thorfinn Karlsefni", None, False, "No." ],
                [ "Freydís Eiríksdóttir", None, False, "No." ]
            ]
        },
        {
            "question_title": "Which active stratovolcano located in southern Iceland is one of the island's most dangerous, famous for erupting underneath the Mýrdalsjökull ice cap and causing catastrophic glacial floods (jökulhlaups)?",
            "question_map_X": -19.0,
            "question_map_Y": 63.6,
            "question_map_ZOOM": 10,
            "answers": [
                [ "Grímsvötn", None, False, "No." ],
                [ "Katla", "Yes.", True, None ],
                [ "Bárðarbunga", None, False, "No." ],
                [ "Eyjafjallajökull", None, False, "No." ]
            ]
        },

        {
            "question_title": "Viking explorers sailed even further west than Vinland. Archaeological evidence suggests they regularly visited this massive island (which they called Helluland, meaning 'Land of Flat Stones') to gather timber and trade with indigenous peoples. Place the dot on Baffin Island.",
            "question_map_X": -70.0,
            "question_map_Y": 69.0,
            "question_map_ZOOM": 3,
            "dot_answer": [
                {
                    "dot_question": "Perfect! You've located Baffin Island, known to the ancient Norse as Helluland.",
                    "true_answer_map_X": -68.84,
                    "true_answer_map_Y": 66.52,
                    "right_message": "Yes, this is Helluland (Baffin Island).",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "The Western Settlement was a group of farms established by Icelandic vikings in Greenland around 985 AD, but it mysteriously vanished entirely in the 14th century. Place a dot on the Nuuk fjord region where this remote outpost once stood.",
            "question_map_X": -51.0,
            "question_map_Y": 64.2,
            "question_map_ZOOM": 5,
            "dot_answer": [
                {
                    "dot_question": "Excellent! You found the area of the lost Western Settlement near modern-day Nuuk.",
                    "true_answer_map_X": -50.25,
                    "true_answer_map_Y": 64.50,
                    "right_message": "Yes, this is the Western Settlement area.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "Where is the island of Grímsey located? It is the only part of Icelandic territory that is actually crossed by the official Arctic Circle line.",
            "question_map_X": -18.0,
            "question_map_Y": 66.5,
            "question_map_ZOOM": 9,
            "dot_answer": [
                {
                    "dot_question": "Great eye! You found Grímsey, sitting right on the edge of the Arctic Circle.",
                    "true_answer_map_X": -18.00,
                    "true_answer_map_Y": 66.55,
                    "right_message": "Yes, this is Grímsey island.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "Reynisdrangar are famous, jagged basalt sea stacks poking out of the ocean. According to local folklore, they were formed when two trolls tried to drag a three-masted ship to shore but were turned to stone by the sunrise. Place a dot on this southern black sand beach near Vík í Mýrdal.",
            "question_map_X": -19.0,
            "question_map_Y": 63.4,
            "question_map_ZOOM": 11,
            "dot_answer": [
                {
                    "dot_question": "Spot on! You pointed right to the dramatic southern coast of Vík.",
                    "true_answer_map_X": -19.02,
                    "true_answer_map_Y": 63.40,
                    "right_message": "Yes, these are the Reynisdrangar sea stacks.",
                    "wrong_message": "No"
                }
            ]
        },
        {
            "question_title": "During the Little Ice Age, sea ice completely blocked Iceland's trade routes for months. Ships from the Hanseatic League and Britain had to brave terrifying winter storms to reach Iceland's main trading outpost in the Westfjords. Place a dot on the historic trading town of Ísafjörður.",
            "question_map_X": -23.1,
            "question_map_Y": 66.0,
            "question_map_ZOOM": 9,
            "dot_answer": [
                {
                    "dot_question": "Correct! You successfully carved your way into the deep fjords to locate Ísafjörður.",
                    "true_answer_map_X": -23.12,
                    "true_answer_map_Y": 66.07,
                    "right_message": "Yes, this is Ísafjörður in the Westfjords.",
                    "wrong_message": "No"
                }
            ]
        }

    ]
}     ,



    {
        "name": "Do you know Caribbean geography?",
        "description": "Test your knowledge of the islands, history, and pirate havens of the Caribbean Sea! ![Caribbean](https://upload.wikimedia.org/wikipedia/commons/c/c4/Caribbean_Sea_and_West_Indies.png)",
        "questions": [
            {
                "question_title": "Which major Caribbean capital city was founded by Diego Columbus (son of Christopher Columbus) in 1498?",
                "question_map_X": -69.8908,
                "question_map_Y": 18.4861,
                "question_map_ZOOM": 12,
                "answers": [
                    ["Havana", None, False, "No, that is in Cuba."],
                    ["San Juan", None, False, "No, that is in Puerto Rico."],
                    ["Santo Domingo", "Yes.", True, None],
                    ["Kingston", None, False, "No, that is in Jamaica."],
                    ["Nassau", None, False, "No, that is in the Bahamas."],
                ]
            },
            {
                "question_title": "This city was known as the 'Richest and Wickedest City in the World' until a massive earthquake sank most of it into the sea in 1692. What was its name?",
                "question_map_X": -76.8408,
                "question_map_Y": 17.9378,
                "question_map_ZOOM": 14,
                "answers": [
                    ["Tortuga", None, False, "No, Tortuga is an island north of Haiti."],
                    ["Nassau", None, False, "No, Nassau became a pirate hub later."],
                    ["Port Royal", "Yes.", True, None],
                    ["St. Augustine", None, False, "No, that is in Florida."],
                    ["Willemstad", None, False, "No, that is in Curaçao."],
                ]
            },
            {
                "question_title": "In 1995, the Soufrière Hills volcano erupted, burying the capital city of this island in ash and turning the southern half of the island into an exclusion zone. Name the buried capital.",
                "question_map_X": -62.2147,
                "question_map_Y": 16.7014,
                "question_map_ZOOM": 13,
                "answers": [
                    ["Basseterre", None, False, "No, that is the capital of St. Kitts and Nevis."],
                    ["Plymouth", "Yes.", True, None],
                    ["Roseau", None, False, "No, that is the capital of Dominica."],
                    ["Kingstown", None, False, "No, that is the capital of St. Vincent."],
                ]
            },
            {
                "question_title": "The famous naval Battle of the Saintes took place in 1782 between British and French fleets.",
                "question_map_X": -60,
                "question_map_Y": 16,
                "question_map_ZOOM": 8,

                "dot_answer" : [
              { "dot_question" : "Yes, you've placed the dot on the map very close to the target place.",
                "true_answer_map_X" : -61.6,
                "true_answer_map_Y" : 15.8,
                "right_message" : "Yes.",
                "wrong_message" : "No",
              }, ]

            }
        ]
    },

    {
        "name": "Do you know South Georgia and the South Sandwich Islands geography?",
        "description": "Test your knowledge on one of the most remote, mountainous, and wildlife-rich British Overseas Territories in the sub-Antarctic! ![SGSSI](https://upload.wikimedia.org/wikipedia/commons/a/a3/Grytviken_Church%2C_South_Georgia_%287413025656%29.jpg)",
        "questions": [
            {
                "question_title": "What is the name of the historic, abandoned Norwegian whaling station on South Georgia where legendary explorer Sir Ernest Shackleton is buried?",
                "question_map_X": -36.5087,
                "question_map_Y": -54.2811,
                "question_map_ZOOM": 13,
                "answers": [
                    ["Stromness", None, False, "No, though Shackleton did hike there to get rescue."],
                    ["Husvik", None, False, "No, that is another whaling station nearby."],
                    ["Grytviken", "Yes.", True, None],
                    ["Leith Harbour", None, False, "No, Leith was the largest station but not his burial site."],
                ]
            },
            {
                "question_title": "Rising to 2,934 meters (9,626 ft) in the Allardyce Range, what is the highest peak in this territory (and across all UK sovereign territories outside Antarctica)?",
                "question_map_X": -36.5278,
                "question_map_Y": -54.4461,
                "question_map_ZOOM": 10,
                "answers": [
                    ["Mount Hope", None, False, "No, Mount Hope is located in the British Antarctic Territory."],
                    ["Mount Paget", "Yes.", True, None],
                    ["Mount Carse", None, False, "No, that is in the southern part of the island."],
                    ["Mount Belinda", None, False, "No, that is an active volcano in the South Sandwich chain."],
                ]
            },
            {
                "question_title": "Which island at the northwestern tip of South Georgia is famous for hosting a major British Antarctic Survey research station dedicated to seabirds and seals?",
                "question_map_X": -38.0500,
                "question_map_Y": -54.0083,
                "question_map_ZOOM": 11,
                "answers": [
                    ["Annenkov Island", None, False, "No, Annenkov sits off the central western coast."],
                    ["Cooper Island", None, False, "No, Cooper Island is at the southeastern tip."],
                    ["Bird Island", "Yes.", True, None],
                    ["Thule Island", None, False, "No, Thule is far away in the South Sandwich Islands."],
                ]
            },
            {
                "question_title": "During the 1982 Falklands War, Argentine forces briefly occupied South Georgia. At which administrative outpost on Cumberland East Bay did the main military clash occur?",
                "question_map_X": -36.4961,
                "question_map_Y": -54.2872,
                "question_map_ZOOM": 14,
                "answers": [
                    ["King Edward Point", "Yes.", True, None],
                    ["Prion Island", None, False, "No, Prion Island is an unpopulated wildlife sanctuary."],
                    ["Godthul", None, False, "No, that was a minor whaling harbor."],
                    ["St. Andrews Bay", None, False, "No, that is home to king penguins, not the garrison."],
                ]
            },
            {
                "question_title": "What is the name of the northernmost active volcanic island in the South Sandwich Islands chain?",
                "question_map_X": -26.4500,
                "question_map_Y": -56.3000,
                "question_map_ZOOM": 9,
                "answers": [
                    ["Zavodovski Island", "Yes.", True, None],
                    ["Visokoi Island", None, False, "No, Visokoi is slightly further south."],
                    ["Bristol Island", None, False, "No, Bristol is near the southern end of the arc."],
                    ["Saunders Island", None, False, "No, Saunders is located in the middle of the chain."],
                ]
            },
            {
                "question_title": "Zavodovski Island is internationally famous for hosting the world's largest colony of which specific type of penguin?",
                "question_map_X": -27.5667,
                "question_map_Y": -56.3,
                "question_map_ZOOM": 13,
                "answers": [
                    ["Emperor Penguin", None, False, "No, Emperors breed further south on continental ice."],
                    ["Chinstrap Penguin", "Yes.", True, None],
                    ["King Penguin", None, False, "No, Kings prefer the flat glacial plains of South Georgia."],
                    ["Adélie Penguin", None, False, "No, Adélies prefer true Antarctic pack ice zones."],
                ]
            },
            {
                "question_title": "Which prominent bay on South Georgia's north coast is renowned for hosting the island's single largest breeding colony of King Penguins, numbering over 100,000 pairs?",
                "question_map_X": -36.1667,
                "question_map_Y": -54.4333,
                "question_map_ZOOM": 11,
                "answers": [
                    ["Fortuna Bay", None, False, "No, though Fortuna does have a notable smaller colony."],
                    ["St. Andrews Bay", "Yes.", True, None],
                    ["Royal Bay", None, False, "No, Royal Bay is further south."],
                    ["Elsehul", None, False, "No, Elsehul is primarily known for fur seals."],
                ]
            },
            {
                "question_title": "In 1775, which famous European explorer made the first definitive landing on South Georgia, mapping it and claiming it for Great Britain?",
                "question_map_X": -36.0000,
                "question_map_Y": -54.5000,
                "question_map_ZOOM": 7,
                "answers": [
                    ["Captain James Cook", "Yes.", True, None],
                    ["Sir Francis Drake", None, False, "No, Drake sailed much further north and west."],
                    ["James Weddell", None, False, "No, Weddell explored the area decades later in the 1820s."],
                    ["Thaddeus Bellingshausen", None, False, "No, Bellingshausen mapped the South Sandwich chain later."],
                ]
            },
            {
                "question_title": "At the southern tip of the South Sandwich Islands lies Thule Island. What is the name of the secret military naval station Argentina illegally maintained there from 1976 to 1982?",
                "question_map_X": -27.3000,
                "question_map_Y": -59.4500,
                "question_map_ZOOM": 11,
                "answers": [
                    ["Corbeta Uruguay", "Yes.", True, None],
                    ["Base Orcadas", None, False, "No, Orcadas is in the South Orkney Islands."],
                    ["Base Marambio", None, False, "No, Marambio is on the Antarctic Peninsula."],
                    ["Puerto Belgrano", None, False, "No, that is a major naval base in mainland Argentina."],
                ]
            },
            {
                "question_title": "South Georgia successfully completed the world's largest island rodent eradication program in 2018. Which invasive species, brought by historical ships, was completely wiped out to save native bird populations?",
                "question_map_X": -36.6000,
                "question_map_Y": -54.2500,
                "question_map_ZOOM": 8,
                "answers": [
                    ["Black Rat", None, False, "No, it was specifically the brown/Norway rat."],
                    ["Norway (Brown) Rat", "Yes.", True, None],
                    ["House Mouse", None, False, "No, mice were only an issue on neighboring islands like Gough."],
                    ["European Rabbit", None, False, "No, rabbits were never successfully established here."],
                ]
            },
            {
                "question_title": "What is the name of the narrow, dramatic maritime passage at the southeastern tip of South Georgia that separates the main island from Cooper Island?",
                "question_map_X": -35.8000,
                "question_map_Y": -54.7800,
                "question_map_ZOOM": 11,
                "answers": [
                    ["Drygalski Fjord", None, False, "No, Drygalski is a nearby fjord, not a strait."],
                    ["Cooper Sound", "Yes.", True, None],
                    ["Drake Passage", None, False, "No, the Drake Passage separates South America from Antarctica."],
                    ["Cumberland Sound", None, False, "No, Cumberland is the massive bay near Grytviken."],
                ]
            },
            {
                "question_title": "The South Sandwich Trench is one of the deepest oceanic trenches in the world. Place the dot on the map as close as you can to Meteor Deep, where this deep underwater abyss runs parallel to the east of the island chain. The deepest point in the entire trench is the Meteor Deep, whose location prior to February 2019 was identified at a depth of 8,202 metres (26,909 ft).",
                "question_map_X": -26.5000,
                "question_map_Y": -55.5000,
                "question_map_ZOOM": 5,

                   "dot_answer" : [
              { "dot_question" : "Where is Meteor Deep?",
                "true_answer_map_X" : -26.404667,
                "true_answer_map_Y" : -55.418667,
                "right_message" : "Yes, you've placed the dot on the map very close to the target place. It's a Meteor Deep.",
                "wrong_message" : "No",
              },
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
        [ "The Pantheon", "None", False, "No." ],
        [ "The Colosseum", "Correct! The Colosseum is the largest ancient amphitheater ever built.", True, "None" ],
        [ "Circus Maximus", "None", False, "No." ],
        [ "The Roman Forum", "None", False, "No." ]
      ]
    },
    {
      "question_title": "Which temple features a massive concrete dome with a central opening (oculus) at its top?",
      "answers": [
        [ "The Pantheon", "Correct! The Pantheon dome remains the world's largest unreinforced concrete dome.", True, "None" ],
        [ "Temple of Venus and Roma", "None", False, "No." ],
        [ "Temple of Saturn", "None", False, "No." ],
        [ "Maison Carrée", "None", False, "No." ]
      ]
    },
    {
      "question_title": "What volcanic ash material did Romans mix with lime to create their incredibly durable concrete?",
      "answers": [
        [ "Marble dust", "None", False, "No." ],
        [ "Granite aggregate", "None", False, "No." ],
        [ "Pozzolana", "Correct! Pozzolana allowed Roman concrete to set even underwater.", True, "None" ],
        [ "Pumice stone", "None", False, "No." ]
      ]
    },
    {
      "question_title": "Which major structure was built to transport fresh water over long distances into Roman cities?",
      "answers": [
        [ "The Appian Way", "None", False, "No." ],
        [ "The Cloaca Maxima", "None", False, "No." ],
        [ "Aqueduct of Segovia", "Correct! Aqueducts used a precise gravity gradient to move water.", True, "None" ],
        [ "Baths of Caracalla", "None", False, "No." ]
      ]
    },
    {
      "question_title": "Which architectural order did the Romans adapt from the Greeks, adding a base and removing column fluting?",
      "answers": [
        [ "Doric Order", "None", False, "No." ],
        [ "Tuscan Order", "Correct! The Tuscan order is a simplified, sturdier version of the Greek Doric order.", True, "None" ],
        [ "Ionic Order", "None", False, "No." ],
        [ "Corinthian Order", "None", False, "No." ]
      ]
    },
    {
      "question_title": "What is the name of the oldest and most famous strategic military highway built by the Romans in 312 BC?",
      "answers": [
        [ "Via Flaminia", "None", False, "No." ],
        [ "Via Appia", "Correct! The Appian Way connected Rome to Brindisi and was called the queen of long-distance roads.", True, "None" ],
        [ "Via Aurelia", "None", False, "No." ],
        [ "Via Sacra", "None", False, "No." ]
      ]
    },
    {
      "question_title": "Which structural element, consisting of an arch extended along a continuous path, did the Romans use to create long corridors and tunnels?",
      "answers": [
        [ "Groin vault", "None", False, "No." ],
        [ "Barrel vault", "Correct! A barrel vault is a simple, semi-cylindrical arch structure used for ceilings.", True, "None" ],
        [ "Rib vault", "None", False, "No." ],
        [ "Dome", "None", False, "No." ]
      ]
    },
    {
      "question_title": "Which massive Roman bath complex could accommodate up to 1,600 bathers and featured a complex underfloor heating system (hypocaust)?",
      "answers": [
        [ "Baths of Diocletian", "None", False, "No." ],
        [ "Baths of Trajan", "None", False, "No." ],
        [ "Baths of Caracalla", "Correct! The Baths of Caracalla were a massive public leisure complex.", True, "None" ],
        [ "Baths of Nero", "None", False, "No." ]
      ]
    },
    {
      "question_title": "What architectural masterpiece in southern France is a triple-tiered bridge that served as both an aqueduct and a road?",
      "answers": [
        [ "Pont du Gard", "Correct! The Pont du Gard is a brilliant example of Roman precision hydraulic engineering.", True, "None" ],
        [ "Bridge of Alcántara", "None", False, "No." ],
        [ "Pont d'Avignon", "None", False, "No." ],
        [ "Milvian Bridge", "None", False, "No." ]
      ]
    },
    {
      "question_title": "What unique architectural form is created by the perpendicular intersection of two barrel vaults?",
      "answers": [
        [ "An oculus", "None", False, "No." ],
        [ "A groin vault", "Correct! Groin vaults allowed Romans to concentrate weight on specific corner pillars rather than solid walls.", True, "None" ],
        [ "A flying buttress", "None", False, "No." ],
        [ "A corbel arch", "None", False, "No." ]
      ]
    }
  ]
}

,
{
    "name": "The Fall of the Republic",
    "description": "Explore the dramatic transition from the Roman Republic to the Empire.",
    "questions": [
        {
            "question_title": "On which famous date was Julius Caesar assassinated in the Roman Senate?",
            "answers": [
                ["January 1, 45 BC", "None", False, "No."],
                ["March 15, 44 BC", "Correct! This date is famously known as the Ides of March.", True, "None"],
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
                ["Via Appia", "None", False, "No."],
                ["Vigiles", "None", False, "No."],
                ["Cursus Publicus", "Yes. Established by Augustus, the Cursus Publicus used a network of relay stations for fast imperial communication.", True, "None"],
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
    # check db is empty
    if result.scalars().first():
        return None

    # check we have the bot in user list
    bot_user = await User.get_user_by_username(DB, BOT_USER_NAME )
    if not bot_user:
        return None

    # quiz
    for cqm in CONST_QUESTS_MAP:
        quest = Quest( name = cqm["name"], description = cqm["description"], user_creator = bot_user, is_active = True, difficulty_coefficient = 3  )
        DB.add( quest )
        await DB.commit()

        nf = News_Feed( published_dt = datetime.now(), title = 'New quiz!', description = "Our mighty bot has made a new quiz for you! " + quest.name, is_active = True, user_creator = bot_user, quest = quest )
        DB.add( nf )
        await DB.commit()

        for qd in cqm["questions"]:
            if qd.get("dot_answer"):
                q = Question( question_title = qd["question_title"],
                                  question_type = CONST_QUESTION_TYPE_MAP_POINT_AND_DOT_ANSWER,
                                  question_map_X = qd["question_map_X"],
                                  question_map_Y = qd["question_map_Y"],
                                  question_map_ZOOM = qd["question_map_ZOOM"],
                              quest_id = quest.id )
                DB.add( q )
                await DB.commit()
                for answer in qd.get("dot_answer"):
                    a = AnswerVar( question_id = q.id,
                                   answer_title = answer["dot_question"],
                                   right_message = answer["right_message"],
                                   is_true_answer = False,
                                   true_answer_map_Y = answer["true_answer_map_Y"],
                                   wrong_message = answer["wrong_message"],
                                   true_answer_map_X = answer["true_answer_map_X"],
                                   )

                    DB.add( a )
                    await DB.commit()
            else:
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
        quest = Quest( name = сq_d["name"], description = сq_d["description"], user_creator = bot_user, is_active = True  )
        DB.add( quest )
        await DB.commit()

        nf = News_Feed( published_dt = datetime.now(), title = 'New quiz!', description = "Our mighty bot has made a new quiz for you! " + quest.name, is_active = True, user_creator = bot_user, quest = quest )
        DB.add( nf )
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


    # Treasure quest
    for ctq in CONST_TREASURE_QUEST:
        quest = Quest( name = ctq["name"], description = ctq["description"], quest_type = CONST_QUEST_TREASURE_QUEST, user_creator = bot_user, is_active = True, difficulty_coefficient = 50  )
        DB.add( quest )
        await DB.commit()

        nf = News_Feed( published_dt = datetime.now(), title = 'New treasure quest!', description = "Our mighty bot has made a new quest for you! " + quest.name, is_active = True, user_creator = bot_user, quest = quest )
        DB.add( nf )
        await DB.commit()


#