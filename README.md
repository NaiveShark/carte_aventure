# Carte d'aventure

Une application pour créer des quêtes, des énigmes et des compétitions.


# Lancement du système

Renommez le fichier `.env.example` en `.env` et saisissez votre `SECRET_KEY` générée aléatoirement ainsi que les chemins corrects pour les modèles et les fichiers statiques (`TEMPLATES_PATH`, `STATICS_PATH`).

    uvicorn app.main:app --reload
	
# Vérification
	
	python -m pytest