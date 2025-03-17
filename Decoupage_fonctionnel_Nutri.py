def calculer_besoins_caloriques_par_jour(age, sexe, poids, taille, activite):
    """
    Calcule le nombre de calories nécessaires par jour en fonction des caractéristiques de l'utilisateur.
    Paramètres:
    - age (int) : Âge de l'utilisateur en années.
    - sexe (str) : "M" pour masculin, "F" pour féminin.
    - poids (float) : Poids de l'utilisateur en kilogrammes.
    - taille (float) : Taille de l'utilisateur en centimètres.
    - activite (int) : Niveau d'activité physique (1 = sédentaire, 5 = très actif).

    Retourne:
    - float : Besoins caloriques quotidiens en kcal.

    Formule utilisée:
    - Homme : 10 * poids + 6.25 * taille - 5 * âge + 5
    - Femme : 10 * poids + 6.25 * taille - 5 * âge - 161
    - Multiplié par un facteur d'activité pour ajuster selon le mode de vie.
    """
    if sexe == "H" :
        besoins_caloriques = 10 * poids + 6.25 * taille - 5 * age + 5 
        
    else : 
        besoins_caloriques = 10 * poids + 6.25 * taille - 5 * age - 161 
    return besoins_caloriques 
     

def calculer_macronutriments(besoins_caloriques):
    """
    Calcule les besoins en macronutriments (protéines, glucides, lipides, carbohydrates) en grammes par jour.

    Paramètres:
    - besoins_caloriques (float) : Nombre total de calories nécessaires par jour.

    Retourne:
    - my_nutriment : liste contenant les quantités recommandées en grammes pour :
      - "proteines"
      - "glucides"
      - "lipides"
      
    Répartition classique:
    - Protéines : 15-20% des calories (1g = 4 kcal)
    - Glucides : 45-55% des calories (1g = 4 kcal)
    - Lipides : 25-35% des calories (1g = 9 kcal)
    """ 
    proteines = round((0.18 * besoins_caloriques) / 4, 1)  # 18% des kcal en protéines
    glucides = round((0.50 * besoins_caloriques) / 4, 1)   # 50% des kcal en glucides
    lipides = round((0.30 * besoins_caloriques) / 9, 1)    # 30% des kcal en lipides 
    
    macronutriment_necessaire = [proteines,glucides,lipides] 
    return macronutriment_necessaire

