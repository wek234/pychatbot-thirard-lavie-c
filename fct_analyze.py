# -*- coding: utf-8 -*-
"""
PyChat Bot
Programme projet python semestre 01 L1 Efrei

Auteur : Téo Lavie & Wagner Thirard
Date : novembre-décembre 2023

Fichier : fct_analyze.py
Fonction : Fonctions d'analyse des discours
"""


from fct_tf_idf import *
# fonction liste des fichiers


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

# fonction qui calcule la matrice TF-IDF


############################
# Question 1:
############################

#Cette fonction identifie et retourne une liste de mots non importants avec les scores TF-IDF.
def mots_non_importants():

    # initialise une liste pour stocker les mots non importants
    mots_non_importants = []
    for i in range(len(tout_mots)):
        # initialise un booleen pour indiquer si le mot est "non important"
        est_non_important = True
        # vérifie si le score TF-IDF est 0 dans tous les fichiers
        for j in range(len(list_f)):
            if tfidf_matrice[i][j] != 0:
                est_non_important = False
            # si le mot est non important l'ajoute à la liste
        if est_non_important:
            mots_non_importants.append(tout_mots[i])
    return mots_non_importants

# affiche les mots non importants
def listniw():
    mots_non_importants_liste = mots_non_importants()
    print("Mots non importants :")
    print(mots_non_importants_liste)


############################
# Question 2:
############################

# fonction pour trouver le mot ayant le score TF-IDF le plus élevé
def plus_grand_tfidf():
    max_tfidf = -1
    max_tfidf_words = []
    for i in range(len(tout_mots)):
        mot = tout_mots[i]
        max_tfidf_word_score = max(tfidf_matrice[i])

        if max_tfidf_word_score > max_tfidf:
            max_tfidf = max_tfidf_word_score
            max_tfidf_words = [mot]
        elif max_tfidf_word_score == max_tfidf:
            max_tfidf_words.append(mot)

    return max_tfidf_words, max_tfidf

# affiche le mot ayant le score TF-IDF le plus élevé

def tdfmax():
    max_tfidf_words, max_tfidf_value = plus_grand_tfidf()
    print("Mot ayant le score TF-IDF le plus élevé ", max_tfidf_value, ":")
    print(max_tfidf_words)

############################
# Function n°3
############################

#fonction qui 1retourne une liste des 10 mots les plus répétés dans les discours du president Chirac.
def mots_plus_repetes_chirac(directory):
    chirac_occurrences = {}  # Dictionnaire pour stocker les occurrences de chaque mot pour Chirac
    chirac_files = [fichier for fichier in list_of_files(directory, '.txt') if 'Chirac' in fichier]

    for fichier in chirac_files:
        occurrences = calculer_tf(fichier)
        for mot, occ in occurrences.items():
            if mot != '':
                if mot in chirac_occurrences:
                    chirac_occurrences[mot] += occ
                else:
                    chirac_occurrences[mot] = occ

    mots_plus_repetes = sorted(chirac_occurrences.items(), key=lambda x: x[1], reverse=True)
    return mots_plus_repetes[:10]  # Les 10 mots les plus répétés

# affiche les mots les plus répétés par le président Chirac


def repete():
    directory = './cleaned/'
    mots_repetes_chirac = mots_plus_repetes_chirac(directory)
    print("Les mots les plus répétés par le président Chirac :", mots_repetes_chirac)

############################
# Function n°4
############################

#fonction qui prend un mot en entree et identifie les présidents qui ont parlé de ce mot et retourne le président qui l'a répété le plus de fois.
def occurrences_mot(directory):
    motchoisi = input("quel mot voulez vous chercher ? ")
    presidents_occurrences = {}  # Dictionnaire pour stocker les occurrences de chaque président pour "Nation"
    all_presidents = set()  # Ensemble pour stocker tous les noms de président

    for fichier in list_of_files(directory, '.txt'):
        # Extraire le nom du président en utilisant le modèle "_NomPresident."
        parts = fichier.split('_')
        if len(parts) > 1:
            president = parts[-1].replace('.txt', '')
            all_presidents.add(president)

            occurrences = calculer_tf(fichier)
            if motchoisi in occurrences:
                if president in presidents_occurrences:
                    presidents_occurrences[president] += occurrences[motchoisi]
                else:
                    presidents_occurrences[president] = occurrences[motchoisi]

    if not presidents_occurrences:  # Vérifier si la liste est vide
        return [], None  # Si la liste est vide, retourner des résultats vides

    # Trouve les présidents qui ont parlé de "nation"
    presidents_nation = [president for president, occ in presidents_occurrences.items() if occ > 0]
    # Trouve le président qui a répété le plus de fois le mot "nation"
    president_plus_repete = max(presidents_occurrences, key=presidents_occurrences.get)

    return presidents_nation, president_plus_repete, motchoisi

# affiche les président qui ont utilisé « nation » dans leurs discours


def occmot():
    directory = './cleaned/'
    presidents_nation, president_plus_repete, motchoisi = occurrences_mot(directory)

    if "Chirac2" in president_plus_repete:
        president_plus_repete = "Chirac"
    if "Mitterrand2" in president_plus_repete:
        president_plus_repete = "Mitterrand"
    if presidents_nation:
        print("Président(s) qui ont parlé de", motchoisi, ":", presidents_nation)
        print("Président qui l’a répété le plus de fois :", president_plus_repete)
    else:
        print("Aucun président n'a parlé de ", motchoisi, " dans les discours analysés.")

############################
# Function n°5
############################

#fonction qui identifie et retourne le premier président à parler du climat ou de l'écologie.
def climat_ecologie(directory):
    all_presidents = set()  # Ensemble pour stocker tous les noms de président

    for fichier in list_of_files(directory, '.txt'):
        # Extraire le nom du président à partir du nom du fichier
        president = fichier.split('_')[1].split('.')[0]
        all_presidents.add(president)

        occurrences = calculer_tf(fichier)
        if "climat" in occurrences or "écologie" in occurrences:
            return president  # Le premier président à parler du climat ou de l'écologie

# affiche le premier président à parler du climat ou de l’écologie


def climeco():
    directory = './cleaned/'
    premier_president = climat_ecologie(directory)
    print("Premier président à parler du climat et/ou de l’écologie :", premier_president)


############################
# Question 6:
############################

#fonction identifie et retourne une liste de mots qui sont communs à tous les présidents en se basant sur les scores TF-IDF.
def mots_communs(tfidf_matrice, tout_mots, list_f):
    mots_comm = []

    # boucle sur chaque mot
    for i, mot in enumerate(tout_mots):
        # initialise une variable pour indiquer si le mot est commun à tous les présidents
        est_commun = True
        # boucle sur chaque fichier pour vérifier si le score TF-IDF est non nul
        j = 0
        while est_commun and j < len(list_f):
            if tfidf_matrice[i][j] == 0:
                # si le score TF-IDF est nul dans un fichier le mot n'est pas commun
                est_commun = False
            j += 1
        # si le mot est commun à tous les présidents l'ajoute à la liste
        if est_commun:
            mots_comm.append(mot)
    return mots_comm

# affiche les mots communs à tous les présidents


def communs():
    directory = './cleaned/'
    # utilise la fonction qui calcule la matrice TF-IDF
    tfidf_matrice, tout_mots, list_f = calculer_tf_idf_matrice(directory)

    # affiche les mots communs à tous les présidents
    mots_communs_liste = mots_communs(tfidf_matrice, tout_mots, list_f)
    print("Mots important communs à tous les présidents :")
    print(mots_communs_liste)
