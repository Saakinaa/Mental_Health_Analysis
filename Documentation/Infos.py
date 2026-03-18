# =========================
# Import Libraries 
# =========================

import pandas as pd 
import numpy as np

# =========================
# Load Descriptions 
# =========================
des = pd.read_csv("/Users/user/Downloads/Stud_Mental_Health/Data/Codebook 2022 MedTeach.csv", sep = ";")
des

# =========================
# Suppress Unnamed columns
# =========================
des.drop(['Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'], axis=1)


# =========================
# Check Variables   
# =========================
# for variable in des.columns :
    # for description in des.columns
variable = des["Variable Name"]   
description = des["Variable Label"]
Scaling = des["Variable Scale"]

descript = des.reset_index()
for index, row in des.iterrows() :
    print(f"{row['Variable Name']} : {row['Variable Label']}")
    
# =======================================
# Data Dictionary and Documentation 
# =======================================

import pandas as pd

# Création du dictionnaire des données
data_dict = [
    # Identification
    {"Variable": "id", "Type": "Numérique", "Description": "Identifiant unique du participant",
     "Académique": "Neutre, uniquement technique", "Entreprise": "Neutre, anonymisation obligatoire"},
    
    # Sociodémographie
    {"Variable": "age", "Type": "Numérique", "Description": "Âge du participant",
     "Académique": "Corrélation avec burnout, dépression, empathie",
     "Entreprise": "Facteur de segmentation, prédiction burnout ou performance"},
    
    {"Variable": "year", "Type": "Ordinale", "Description": "Année du cursus",
     "Académique": "Étudier évolution empathie / burnout selon l’année",
     "Entreprise": "Identifier groupes à risque, plan de formation ciblé"},
    
    {"Variable": "sex", "Type": "Catégorielle", "Description": "Genre identifié",
     "Académique": "Comparaison moyennes scores psychologiques",
     "Entreprise": "Segmentation, équité / diversité"},
    
    {"Variable": "glang", "Type": "Catégorielle", "Description": "Langue maternelle",
     "Académique": "Contrôle culturel / biais",
     "Entreprise": "Adaptation programmes, communication ciblée"},
    
    {"Variable": "part", "Type": "Binaire", "Description": "Partenaire ou non",
     "Académique": "Impact sur santé mentale, bien-être",
     "Entreprise": "Détection facteurs sociaux de risque"},
    
    {"Variable": "job", "Type": "Binaire", "Description": "Travail rémunéré ou non",
     "Académique": "Étudier stress lié emploi",
     "Entreprise": "Identifier surcharges, ajuster programme d’accompagnement"},
    
    # Habitudes & Santé
    {"Variable": "stud_h", "Type": "Numérique", "Description": "Heures d’étude par semaine",
     "Académique": "Analyse relation charge travail ↔ burnout",
     "Entreprise": "Identifier étudiants surchargés, ajuster planning"},
    
    {"Variable": "health", "Type": "Ordinale", "Description": "Satisfaction santé",
     "Académique": "Corrélation avec burnout / anxiété",
     "Entreprise": "KPI santé globale, suivi qualité de vie"},
    
    {"Variable": "psyt", "Type": "Binaire", "Description": "Psychothérapie consultée (12 mois)",
     "Académique": "Indicateur vulnérabilité mentale",
     "Entreprise": "Détection besoins support psychologique"},
    
    # Empathie
    {"Variable": "jspe", "Type": "Numérique", "Description": "Score total JSPE",
     "Académique": "Étudier capacité empathie",
     "Entreprise": "Facteur prédictif de relation patient/étudiant ou service client"},
    
    {"Variable": "qcae_cog", "Type": "Numérique", "Description": "Empathie cognitive",
     "Académique": "Étudier compréhension émotions",
     "Entreprise": "Identifier profils formation adaptés"},
    
    {"Variable": "qcae_aff", "Type": "Numérique", "Description": "Empathie affective",
     "Académique": "Étudier sensibilité émotionnelle",
     "Entreprise": "Détection stress lié émotionnel, coaching ciblé"},
    
    # Motivation & Reconnaissance émotionnelle
    {"Variable": "amsp", "Type": "Numérique", "Description": "Motivation académique",
     "Académique": "Corrélations avec performance, burnout",
     "Entreprise": "Identifier étudiants motivés ou à risque, plan incentives"},
    
    {"Variable": "erec_mean", "Type": "Numérique", "Description": "Reconnaissance émotionnelle (GERT)",
     "Académique": "Analyse liens empathie ↔ performance émotionnelle",
     "Entreprise": "Segmentation / formations émotionnelles ciblées"},
    
    # Santé mentale
    {"Variable": "cesd", "Type": "Numérique", "Description": "Dépression (CES-D)",
     "Académique": "Étudier prévalence / corrélation burnout",
     "Entreprise": "Indicateur risque santé mentale, interventions"},
    
    {"Variable": "stai_t", "Type": "Numérique", "Description": "Anxiété trait",
     "Académique": "Corrélation burnout / performance",
     "Entreprise": "Identifier étudiants à risque stress chronique"},
    
    # Burnout académique (MBI)
    {"Variable": "mbi_ex", "Type": "Numérique", "Description": "Épuisement émotionnel",
     "Académique": "Étudier burnout, liens empathie/anxiété",
     "Entreprise": "KPI pour programme prévention burnout"},
    
    {"Variable": "mbi_cy", "Type": "Numérique", "Description": "Cynisme",
     "Académique": "Étudier attitude détachée",
     "Entreprise": "Indicateur désengagement, intervention ciblée"},
    
    {"Variable": "mbi_ea", "Type": "Numérique", "Description": "Efficacité académique",
     "Académique": "Étudier performance / motivation",
     "Entreprise": "Détection étudiants en difficulté"},
]

# Création du DataFrame
df_data_dict = pd.DataFrame(data_dict)

# Affichage
# pd.set_option('display.max_rows', None)  # afficher toutes les lignes si nécessaire
df_data_dict
