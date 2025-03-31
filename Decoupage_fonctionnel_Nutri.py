import pandas as pd
import random

def charger_et_preparer_donnees(fichier):
    df = pd.read_excel(fichier, sheet_name="FAOdata")
    categories = {}
    for index, row in df.iterrows():
        Product_Name = row['Product']
        type_aliment = row['Type']
        sous_type = row["sous_type"]
        quantite = row['RetailUnit']
        
        liste_des_valeurs = [quantite,row['gProteinPerRetailUnit'], row['gFatPerRetailUnit'], row['gCarbPerRetailUnit']]
        if type_aliment not in categories:
            categories[type_aliment] = {}  
        if sous_type not in categories[type_aliment].keys():
            categories[type_aliment][sous_type]={}
        categories[type_aliment][sous_type][Product_Name] = liste_des_valeurs  # Ajouter le produit
    return categories


def demander_infos_utilisateur():
    age = int(input("Quel est votre âge ? "))
    sexe = input("Quel est votre sexe ? (H/F) ")
    poids = float(input("Quel est votre poids (kg) ? "))
    taille = float(input("Quelle est votre taille (cm) ? "))
    activite = input("Quel est votre niveau d'activité ? (Sedentary, Lightly active, Moderately active, Very active, Extra active) ")
    vegetarien = input("Souhaitez-vous une alimentation végétarienne ? (oui/non) ").lower() == "oui"
    if not vegetarien:
        fruits = input("Souhaitez-vous inclure des fruits ? (oui/non) ").lower() == "oui"
        legumes = input("Souhaitez-vous inclure des légumes ? (oui/non) ").lower() == "oui"
        eviter_lait = input("Souhaitez-vous éviter les produits laitiers ? (oui/non) ").lower() == "oui"
        eviter_poisson = input("Souhaitez-vous éviter les produits de la mer ? (oui/non) ").lower() == "oui"
    else:
        fruits = True
        legumes = True
        eviter_poisson = True
        eviter_lait = input("Souhaitez-vous éviter les produits laitiers ? (oui/non) ").lower() == "oui"
    eviter_cereales = input("Souhaitez-vous éviter les céréales ? (oui/non) ").lower() == "oui"
    eviter_alcool = input("Souhaitez-vous éviter les alcools ? (oui/non) ").lower() == "oui"
    return age, sexe, poids, taille, activite, vegetarien, fruits, legumes, eviter_lait, eviter_poisson, eviter_cereales, eviter_alcool

def filtrer_donnees_utilisateur(categories, vegetarien, fruits, legumes, eviter_lait, eviter_poisson, eviter_cereales, eviter_alcool):
    if vegetarien:
        categories["ProteinSource"].pop("viande", None)
        categories["ProteinSource"].pop("poisson", None)
    if not fruits:
        categories.pop("Fruit", None)
    if not legumes:
        categories.pop("Vegetable", None)
    if eviter_lait:
        categories["ProteinSource"].pop("laitier", None)
    if eviter_poisson:
        categories["ProteinSource"].pop("poisson", None)
    if eviter_cereales:
        categories["CarbSource"].pop("céréale", None)
    if eviter_alcool:
        categories["Extra"].pop("alcool", None)
    return categories

def calculer_besoins_caloriques(age, sexe, poids, taille, activite):
    if sexe == "H":
        base = 10 * poids + 6.25 * taille - 5 * age + 5
    else:
        base = 10 * poids + 6.25 * taille - 5 * age - 161
    facteur = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }
    return base * facteur.get(activite, 1.2)

def calculer_macros_pour_dejeuner(calories_total):
    calories_dej = calories_total * 0.4
    besoins = {"proteines":(0.2 * calories_dej) / 4,"lipides": (0.3 * calories_dej) / 9, "glucides": (0.5 * calories_dej) / 4}
    return besoins


def afficher_repas(repas, numero=1):
    print(f"\n Repas {numero} :")
    for nom, poids in repas.items():
        print(f"- {nom} : {poids}")

def generer_et_afficher_trois_repas(df, besoins, max_weight_dict):
    for i in range(3):
        repas = generer_repas_selon_besoins_macronutriments(df, besoins, max_weight_dict)
        afficher_repas(repas, i + 1)

def generer_repas_selon_besoins_macronutriments(categories, besoins, max_weight_dict):
    repas = {}
    p_cible = besoins["proteines"]
    f_cible = besoins["lipides"]
    c_cible = besoins["glucides"]

    p = 0
    f = 0
    c = 0

    # Règles de sélection fixes :
    selection_plan = {
        "CarbSource": 2,
        "ProteinSource": 2,
        "FatSource": 1,
        "Fruit": 1,
        "Vegetable": 1
    }

    for source, nombre in selection_plan.items():
        if source in categories:
            sous_types = list(categories[source].keys())
            random.shuffle(sous_types)
    
            produits_possibles = []
    
            for sous_type in sous_types:
                produits_disponibles = list(categories[source][sous_type].keys())
                produits_possibles.extend(produits_disponibles)
    
            random.shuffle(produits_possibles)
    
            produits_selectionnes = []
            compteur = 0
            for produit in produits_possibles:
                if compteur < nombre:
                    produits_selectionnes.append(produit)
                    compteur += 1


        for produit in produits_selectionnes:
            for sous_type in categories[source]:
                if produit in categories[source][sous_type]:
                    data = categories[source][sous_type][produit]
                    unite = data[0]
                    prot = data[1]
                    lip = data[2]
                    carb = data[3]
                    poids_max = max_weight_dict.get(produit, 100)
                    poids_utilise = 0

                    if source == "ProteinSource":
                        if prot > 0:
                            poids_requis = ((p_cible - p) * 1000) / prot
                            poids_utilise = min(poids_requis, poids_max)

                    if source == "FatSource":
                        if lip > 0:
                            poids_requis = ((f_cible - f) * 1000) / lip
                            poids_utilise = min(poids_requis, poids_max)

                    if source == "CarbSource":
                        if carb > 0:
                            poids_requis = ((c_cible - c) * 1000) / carb
                            poids_utilise = min(poids_requis, poids_max)

                    if source == "Vegetable" or source == "Fruit":
                        poids_utilise = min(100, poids_max)

                    if poids_utilise > 0:
                        p += (prot * poids_utilise) / 1000
                        f += (lip * poids_utilise) / 1000
                        c += (carb * poids_utilise) / 1000

                        if unite == "L":
                            repas[produit] = f"{round(poids_utilise, 1)}ml"
                        else:
                            repas[produit] = f"{round(poids_utilise, 1)}g"

    return repas


if __name__ == "__main__":
    fichier = r"D:\Insa Lyon\Departement\3eme annne\Semestre 2\Info 3\Projet\Data\Documents related to the project-20250224\4-TableS1_augmented_with_FAO_data.xlsx"
    max_weight_dict = {
        "Wheat & Rye (Bread)": 60, "Maize (Meal)": 150, "Barley (Beer)": 355, "Oatmeal": 250, "Rice": 150,
        "Potatoes": 150, "Cassava": 150, "Cane Sugar": 50, "Beet Sugar": 50, "Other Pulses": 150,
        "Peas": 150, "Nuts": 28, "Groundnuts": 28, "Soymilk": 240, "Coffee": 240, "Soybean Oil": 5,
        "Palm Oil": 5, "Sunflower Oil": 5, "Dark Chocolate": 28, "Rapeseed Oil": 5, "Olive Oil": 5,
        "Onions & Leeks": 75, "Bananas": 118, "Brassicas": 85, "Apples": 182, "Citrus Fruit": 154,
        "Berries & Grapes": 74, "Tofu": 150, "Bovine Meat (beef herd)": 85, "Wine": 150, "Other Fruit": 150,
        "Poultry Meat": 85, "Eggs": 50, "Tomatoes": 180, "Bovine Meat (dairy herd)": 85, "Lamb & Mutton": 85,
        "Pig Meat": 85, "Root Vegetables": 150, "Milk": 240, "Cheese": 42, "Other Vegetables": 75,
        "Fish (farmed)": 85, "Crustaceans (farmed)": 85
    }

    age, sexe, poids, taille, activite, vegetarien, fruits, legumes, eviter_lait, eviter_poisson, eviter_cereales, eviter_alcool = demander_infos_utilisateur()
    categories = charger_et_preparer_donnees(fichier)
    categories = filtrer_donnees_utilisateur(categories, vegetarien, fruits, legumes, eviter_lait, eviter_poisson, eviter_cereales, eviter_alcool)
    besoins = calculer_besoins_caloriques(age, sexe, poids, taille, activite)
    macros = calculer_macros_pour_dejeuner(besoins)
    generer_et_afficher_trois_repas(categories, macros, max_weight_dict)