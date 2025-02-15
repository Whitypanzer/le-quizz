from flask import Flask , render_template , session, redirect
import os
from questions import questions
from resultats import resultats 
app=Flask("app_au_calme")
app.secret_key= os.urandom(24)

@app.route('/')
def index():
    session["nb-questions"]= 0
    session["score"] = {"black-templar":0,"grey-wolf":0,"grey-knight":0,}
    return render_template ("index.html")


@app.route('/questions')
def question():
    global questions
    nb_questions = session["nb-questions"]
    if nb_questions <len(questions):
        
        ennonce= questions[nb_questions]["ennonce"]

        questions_copy = questions[nb_questions].copy()

        questions_copy.pop("ennonce")

        reponses = list(questions_copy.values())

        clefs= list(questions_copy.keys())

        session["clefs"]=clefs

        return render_template("questions.html", questions = ennonce, reponses = reponses)
    else:
        score_trie = sorted(session["score"],key = session["score"].get, reverse = True)
        nom_vainqueur = score_trie[0]
        description = resultats[nom_vainqueur]
        return render_template("resultats.html",vainqueur = nom_vainqueur,description = description)
       
     
 



@app.route('/reponses/<numero>')
def reponses(numero):
    session["nb-questions"] +=1

    nom_personnage = session["clefs"][int(numero)]

    session["score"][nom_personnage] +=1

    return redirect("/questions")
 













app.run(host='0.0.0.0',port=81)