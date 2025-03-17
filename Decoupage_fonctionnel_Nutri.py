import pandas as pd 
import random

fichier = r"D:\Insa Lyon\Departement\3eme annne\Semestre 2\Info 3\chp1\project\Documents related to the project-20250224\4-TableS1_augmented_with_FAO_data.xlsx"
df = pd.read_excel(fichier, sheet_name="FAOdata") 



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


def classer_aliments_selon_les_Types(df):
    
    """
    Classe les aliments selon leur type à partir d'un DataFrame.

    Cette fonction prend un DataFrame contenant des informations sur divers aliments,
    y compris leur type, leur nom et leurs valeurs nutritionnelles (calories, protéines, lipides, glucides).
    Elle renvoie un dictionnaire organisé par type d'aliment, où chaque type contient
    un sous-dictionnaire associant les noms des produits à leurs valeurs nutritionnelles.

    Paramètres :
    ------------
    df : pandas.DataFrame
        Un DataFrame contenant au minimum les colonnes suivantes :
        - 'Type' : Catégorie de l'aliment (ex: "ProteinSource", "CarbSource", "FatSource")
        - 'Product' : Nom du produit
        - 'kcalPerRetailUnit' : Calories par unité de vente
        - 'gProteinPerRetailUnit' : Protéines par unité de vente
        - 'gFatPerRetailUnit' : Lipides par unité de vente
        - 'gCarbPerRetailUnit' : Glucides par unité de vente

    Retourne :
    ----------
    dict
        Un dictionnaire de la forme :
        {
            "Type1": {
                "Produit1": [kcal, protéines, lipides, glucides],
                "Produit2": [kcal, protéines, lipides, glucides],
                ...
            },
            "Type2": {
                ...
            }
        }
    """
    
    categories = {}  # Dictionnaire vide
    for index, row in df.iterrows():
        type_aliment = row['Type']
        Product_Name = row['Product']
        valeurs = [
            row['kcalPerRetailUnit'], 
            row['gProteinPerRetailUnit'], 
            row['gFatPerRetailUnit'], 
            row['gCarbPerRetailUnit']
        ]
        if type_aliment not in categories:
            categories[type_aliment] = {}  # Créer la catégorie si elle n'existe pas

        categories[type_aliment][Product_Name] = valeurs  # Ajouter le produit
    return categories


def selectionner_produits_aleatoires_de_3categories(categories):
    """
    Sélectionne aléatoirement un produit dans chacune des trois catégories principales.

    Cette fonction prend en entrée un dictionnaire contenant des catégories d'aliments
    et leurs produits associés. Elle sélectionne aléatoirement un produit dans chacune
    des trois catégories suivantes : "ProteinSource", "CarbSource" et "FatSource".

    Paramètres :
    ------------
    categories : dict
        Un dictionnaire organisé par catégorie d'aliments, avec pour chaque catégorie
        un sous-dictionnaire associant les noms des produits à leurs valeurs nutritionnelles.

    Retourne :
    ----------
    dict
        Un dictionnaire contenant un produit sélectionné aléatoirement dans chaque catégorie :
        {
            "Produit_Protéine": [kcal, protéines, lipides, glucides],
            "Produit_Glucide": [kcal, protéines, lipides, glucides],
            "Produit_Lipide": [kcal, protéines, lipides, glucides]
        }

    Exceptions :
    ------------
    KeyError : Si l'une des catégories attendues n'est pas présente dans le dictionnaire.
    """
    selection = {}
    
    for cat in ['ProteinSource', 'CarbSource', 'FatSource']:
        my_dict=categories[cat]
        product_name= random.choice(list(my_dict.keys()))
        selection[product_name] = categories[cat][product_name]
    return selection 


