import pandas as pd 
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
from scipy.stats import shapiro
from scipy.stats import kurtosis, skew   
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from scipy.stats import cramervonmises, norm

# def preprocess() :
# =================================
# LOAD DATA 
# =================================
mental = pd.read_csv("/Users/user/Downloads/Stud_Mental_Health/Data/Data 2022 MedTeach.csv")
mental 

# def exploring() :
# =================================
# DATA EXPLORER 
# =================================
mental.info() # Get infos
mental.describe(include='all') # Stat descr
mental.isnull().sum() # Missing Values

# =================================
# Unique Values 
# =================================
# Check for Unique Values 
mental['year'].unique()
for col in mental.columns :
    if mental[col].nunique() <= 6 :
        print(f"{col} : {mental[col].unique()}")

# =================================
# Random Questions
# =================================
# Check for year unique values 
mental['year'].unique()

# Check Gender Distribution
mental['sex'].value_counts()

# check for distribution 
for col in mental.columns :
    print(f"{col} : {mental[col].value_counts()}")
        
# =================================================
# Handle Score Values by adapting it clinically 
# =================================================
score_columns = mental.iloc[:, 10:]
score_columns
for col in score_columns : 
    fig = px.box(mental, y=col)
    fig.show()
    

# =================================================
# Handle Score Values by adapting it clinically 
# =================================================

# Create Copy
mental_scaled = mental.copy()

# Linear Rescaling Function
def rescale_score(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val) * 100

# Categorize in 3 levels 
def categorize_score(x):
    if x <= 33:
        return "Faible"
    elif x <= 66:
        return "Moyen"
    else:
        return "Élevé"

# Rescaling
# JSPE selon bornes théoriques 20–140
mental_scaled['JSPE_scaled'] = mental_scaled['jspe'].apply(lambda x: rescale_score(x, 20, 140))
mental_scaled['JSPE_Category'] = mental_scaled['jspe'].apply(lambda x: categorize_score(x))
mental_scaled['JSPE_Category'].unique() # : Notre échantillon a un haut niveau d’empathie global. 

# QCAE utilise l'echelle de Likert 4 points, donc max = n_items * 4 avec intervalle [1, 4]. 
# AMSP est aussi sur une échelle de Likert 5 points, donc max = n_items * 5 avec intervalle [1, 5]. 
# EREC est déjà une moyenne entre 0 et 1.

# Les autres scores (QCAE, AMSP, EREC) sur 0–100
# Les bornes théoriques sont basées sur le nombre d'items et l'échelle de réponse. 

# Pour QCAE Cognitif : 
# min = 19×1=19 ; max = 19×4=76 --> Dataset : min = 37, max = 76

# Pour QCAE Affectif : 
# 12×1=12 ; 12×4= 48 --> Dataset : min = 12, max = 48

# Pour AMSP : 
# AMSP : min = 7×1=7 ; max = 7×5=35 --> Dataset : min = 6, max = 35

# Pour EREC : min = 0 ; max = 1 --> Dataset : min = 0, max = 1
# EREC : déjà entre 0 et 1, pas besoin de rescaling linéaire, juste catégorisation en 3 niveaux selon les mêmes seuils que les autres scores.

# En gros les bornes observées dans le jeux de données correspondent exactement à cette version.
n_items_cog = 19 # QCAE Cognitif
n_items_aff = 12  # QCAE Affectif
max_amsp = 35     # AMSP (7 items × 5 points)

mental_scaled['QCAE_COG_scaled'] = mental_scaled['qcae_cog'].apply(lambda x: rescale_score(x, 1, n_items_cog*4))
mental_scaled['QCAE_AFF_scaled'] = mental_scaled['qcae_aff'].apply(lambda x: rescale_score(x, 1, n_items_aff*4))
mental_scaled['AMSP_scaled'] = mental_scaled['amsp'].apply(lambda x: rescale_score(x, 1, max_amsp))
mental_scaled['EREC_MEAN_scaled'] = mental_scaled['erec_mean'].apply(lambda x: rescale_score(x, 0, 1))  # proportion 0–1

# Catégorisation en 3 niveaux
for col in ['JSPE_scaled', 'QCAE_COG_scaled', 'QCAE_AFF_scaled', 'AMSP_scaled', 'EREC_MEAN_scaled']:
    mental_scaled[col + '_cat'] = mental_scaled[col].apply(categorize_score)

# df_scaled contient maintenant :
# - les scores rescalés
# - les catégories Faible/Moyen/Élevé

# Affichage rapide pour vérification
print(mental_scaled[['jspe','JSPE_scaled','JSPE_scaled_cat',
                 'qcae_cog','QCAE_COG_scaled','QCAE_COG_scaled_cat',
                 'qcae_aff','QCAE_AFF_scaled','QCAE_AFF_scaled_cat',
                 'amsp','AMSP_scaled','AMSP_scaled_cat',
                 'erec_mean','EREC_MEAN_scaled','EREC_MEAN_scaled_cat']].head())

for col in ['JSPE_scaled_cat', 'QCAE_COG_scaled_cat', 'QCAE_AFF_scaled_cat', 'AMSP_scaled_cat', 'EREC_MEAN_scaled_cat']:
    print(f"{col} : {mental_scaled[col].value_counts()}")
    
# =================================================
# Rename columns for clarity
# =================================================
# JSPE : Jefferson Scale of Physician Empathy means that higher scores indicate greater empathy.
# QCAE : Questionnaire of Cognitive and Affective Empathy measures both cognitive and affective empathy, with higher scores indicating greater empathy.
# AMSP : Attitudes towards Medical Student Psychological Health measures attitudes towards mental health, with higher scores indicating more positive attitudes.
# EREC : Empathy-Related Emotional Response to Clinical Vignettes measures emotional response to clinical scenarios, with higher scores indicating better recognition of emotions.
# MBI_EX : Maslach Burnout Inventory - Emotional Exhaustion measures feelings of being emotionally overextended and exhausted by one's work, with higher scores indicating greater emotional exhaustion.
# MBI_CY : Maslach Burnout Inventory - Cynicism measures an indifferent or distant attitude towards work, with higher scores indicating greater cynicism.
# MBI_EA : Maslach Burnout Inventory - Efficacy Academic measures feelings of competence and successful achievement in one's work, with higher scores indicating greater efficacy.  
# CESD : Center for Epidemiologic Studies Depression Scale measures depressive symptoms, with higher scores indicating more severe depression.
# STAI_T : State-Trait Anxiety Inventory - Trait measures general anxiety levels, with higher scores indicating greater anxiety.    

mental_scaled = mental_scaled.rename(columns={

    # Empathy
    "jspe": "Physician_Empathy_Total_Score",
    "JSPE_scaled": "Physician_Empathy_Score_Scaled",
    "JSPE_scaled_cat": "Physician_Empathy_Category",
    "qcae_cog": "Cognitive_Empathy_Total_Score",
    "QCAE_COG_scaled": "Cognitive_Empathy_Score_Scaled",
    "QCAE_COG_scaled_cat": "Cognitive_Empathy_Category",
    "qcae_aff": "Affective_Empathy_Total_Score",
    "QCAE_AFF_scaled": "Affective_Empathy_Score_Scaled",
    "QCAE_AFF_scaled_cat": "Affective_Empathy_Category",

    # Attitudes toward mental health
    "amsp": "Attitudes_Toward_Medical_Student_Mental_Health_Score",
    "AMSP_scaled": "Attitudes_Toward_Mental_Health_Score_Scaled",
    "AMSP_scaled_cat": "Attitudes_Toward_Mental_Health_Category",

    # Emotional recognition
    "erec_mean": "Emotional_Recognition_Mean_Score",
    "EREC_MEAN_scaled": "Emotional_Recognition_Score_Scaled",
    "EREC_MEAN_scaled_cat": "Emotional_Recognition_Category",

    # Burnout
    "mbi_ex": "Burnout_Emotional_Exhaustion_Score",
    "mbi_ex_scaled": "Burnout_Emotional_Exhaustion_Score_Scaled",
    "mbi_ex_scaled_cat": "Burnout_Emotional_Exhaustion_Category",
    "mbi_cy": "Burnout_Cynicism_Score",
    "mbi_cy_scaled": "Burnout_Cynicism_Score_Scaled",
    "mbi_cy_scaled_cat": "Burnout_Cynicism_Category",
    "mbi_ea": "Academic_Efficacy_Score",
    "mbi_ea_scaled": "Academic_Efficacy_Score_Scaled",
    "mbi_ea_scaled_cat": "Academic_Efficacy_Category",

    # Depression & Anxiety
    "cesd": "Depression_Symptom_Score",
    "cesd_scaled": "Depression_Symptom_Score_Scaled",
    "cesd_scaled_cat": "Depression_Symptom_Category",   
    "stai_t": "Trait_Anxiety_Score",
    "stai_t_scaled": "Trait_Anxiety_Score_Scaled",
    "stai_t_scaled_cat": "Trait_Anxiety_Category",
    
    # Glangs, psyt, stud_h, year, 'health'
    "glang": "Languages_Spoken",
    "psyt": "Psychotherapy_Consulted_Last_12_Months",
    "stud_h": "Study_Hours_Per_Week",
    "year": "Academic_Year",
    "health": "Health_Satisfaction",
    "part" : "Partner",
    "job" : "Job",
    "age" : "Age",
    "sex" : "Gender"
})

# =================================================
# Categorize into 3 levels also MBI, CESD, STAI_T
# =================================================

# We wont scale MBI, CESD, STAI_T to respect their clinical cutoffs, but we can categorize them into 3 levels based on established thresholds in the literature.
def categorize_mbi_ex(x):
    if x <= 16:
        return "Faible"
    elif x <= 27:
        return "Moyen"
    else:
        return "Élevé"
    
def categorize_mbi_cy(x):
    if x <= 6:
        return "Faible"
    elif x <= 12:
        return "Moyen"
    else:
        return "Élevé"
    
def categorize_mbi_ea(x):
    if x >= 39:
        return "Faible"
    elif x >= 32:
        return "Moyen"
    else:
        return "Élevé"
def categorize_cesd(x):
    if x <= 15:
        return "Faible"
    elif x <= 21:
        return "Moyen"
    else:
        return "Élevé"
    
def categorize_stai_t(x):
    if x <= 35:
        return "Faible"
    elif x <= 45:
        return "Moyen"
    else:
        return "Élevé"
    
mental_scaled['Burnout_Emotional_Exhaustion_Category'] = mental_scaled['Burnout_Emotional_Exhaustion_Score'].apply(categorize_mbi_ex)
mental_scaled['Burnout_Cynicism_Category'] = mental_scaled['Burnout_Cynicism_Score'].apply(categorize_mbi_cy)
mental_scaled['Academic_Efficacy_Category'] = mental_scaled['Academic_Efficacy_Score'].apply(categorize_mbi_ea)
mental_scaled['Depression_Symptom_Category'] = mental_scaled['Depression_Symptom_Score'].apply(categorize_cesd)
mental_scaled['Trait_Anxiety_Category'] = mental_scaled['Trait_Anxiety_Score'].apply(categorize_stai_t) 

# Final columns name check
mental_scaled.columns

# =================================================
# Save the preprocessed dataset
# =================================================
mental_scaled.to_csv("/Users/user/Downloads/Stud_Mental_Health/Data/Medical_Student_Mental_Health.csv", index=False)


# =================================================
# DETECT AND HANDLE OUTLIERS
# =================================================
for col in mental_scaled : 
  if mental_scaled[col].dtype != 'object' :
    fig = px.box(mental_scaled, y=col, color_discrete_sequence=px.colors.sequential.Purples) # Purple color scheme for boxplots
    print("=" * 80)
    print(f"Variable : {col}")
    print("=" * 80)
    fig.show()
    
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return series[(series < lower) | (series > upper)]

for col in mental_scaled.columns :
  if mental_scaled[col].dtype != 'object' :
    series = mental_scaled[col]
    # print(detect_outliers_iqr(series))
    # Count Outliers
    print(f"{col} : {len(detect_outliers_iqr(series))}")
    
# For Psychotherapy_Consulted_Last_12_Months variable we won't considered that we are dealing with outliers
detect_outliers_iqr(mental_scaled['Psychotherapy_Consulted_Last_12_Months'])
mental_scaled['Psychotherapy_Consulted_Last_12_Months'].unique()


# =================================================
# For Age 
# =================================================
# For Age variable we can consider that values above 30 are outliers in the context of medical students, but we will keep them for now as they could be valid (e.g., older students, career changers).
detect_outliers_iqr(mental_scaled['Age'])
mental_scaled['Age'].unique()
# To handle them, we could either cap them at a certain value (e.g., 30) or keep them as is but be aware of their potential influence on analyses. For now, we will keep them as is to preserve the integrity of the dataset and because they may represent valid cases.
# Capping considering Year of study : if we have 6th year students, it's possible to have older students.
# Verify year of study in rows with age > 30
mental_scaled.loc[mental_scaled['Age'] > 30, 'Academic_Year'].value_counts() # We have 6th year students, so we can keep them as valid cases.

# =================================================
# For Language spoken 
# =================================================
# For Langage spoken it's biologically and logically impossible to speak more than 7 langages so : values exceeding the plausible range 
# for number of languages spoken (>7) were considered data entry errors and recoded as missing to avoid systematic misclassification 
# bias or artificially inflate the “monolingual” group.

mental_scaled['Languages_Spoken'].value_counts()

# And after checking for unique values, it seems that we are not dealing with multilingualism. 
# There is any association between multilingualism maybe and empathy, burnout, depression, etc.
mental_scaled.loc[
    mental_scaled["Languages_Spoken"] > 7,
    "Languages_Spoken"
] = np.nan

mental_scaled['Languages_Spoken'].value_counts()
detect_outliers_iqr(mental_scaled['Languages_Spoken'])

# =================================================
# For Psychotherapy_Consulted_Last_12_Months
# =================================================
# For Psychotherapy_Consulted_Last_12_Months variable we won't considered that we are dealing with outliers. 
detect_outliers_iqr(mental_scaled['Psychotherapy_Consulted_Last_12_Months'])
mental_scaled['Psychotherapy_Consulted_Last_12_Months'].unique()

# =================================================
# For Emotional_Recognition_Mean_Score
# =================================================
# Done with Emotional_Recognition_Mean_Score
detect_outliers_iqr(mental_scaled['Emotional_Recognition_Mean_Score'])


# =================================================
# For Depression_Symptom_Score
# =================================================
outliers = detect_outliers_iqr(mental_scaled['Depression_Symptom_Score'])
# detect_outliers_iqr(mental_scaled['Academic_Efficacy_Score'])
# Print outliers and their category
print(outliers)
print(mental_scaled.loc[outliers.index, 'Depression_Symptom_Category'])
# Verify if only 'Élevé' is considered as outliers 
mental_scaled.loc[outliers.index, 'Depression_Symptom_Category'].unique()

# =================================================
# For Trait_Anxiety_Score
# =================================================
outliers = detect_outliers_iqr(mental_scaled['Trait_Anxiety_Score'])
# detect_outliers_iqr(mental_scaled['Academic_Efficacy_Score'])
# Print outliers and their category
print(mental_scaled.loc[outliers.index, 'Trait_Anxiety_Score'])

# =================================================
# For Physician_Empathy_Score_Scaled
# =================================================
outliers = detect_outliers_iqr(mental_scaled['Physician_Empathy_Score_Scaled'])
# detect_outliers_iqr(mental_scaled['Academic_Efficacy_Score'])
# Print outliers and their category
print(mental_scaled.loc[outliers.index, 'Physician_Empathy_Score_Scaled'])


# ============================================================================
# DISTRIBUTION ANALYSIS & NORMALITY TESTS
# ============================================================================

for col in mental_scaled.columns :
  if mental_scaled[col].dtype != 'object' :
    fig = px.histogram(mental_scaled, x=col, nbins=30)
    print("=" * 80)
    print(f"Variable : {col}")
    print("=" * 80)
    fig.show()
    
# =================================================
# Descriptive statistics for numerical variables
# =================================================
# Separate numerical columns (exclude ID)
numerical_cols = mental_scaled.select_dtypes(include=[np.number]).columns.tolist()
numerical_cols = [col for col in numerical_cols if col != 'id']

# Group variables by category
grouped_vars = {
    "Empathy": [
        "Physician_Empathy_Total_Score",
        "Physician_Empathy_Score_Scaled",
        "Cognitive_Empathy_Total_Score",
        "Cognitive_Empathy_Score_Scaled",
        "Affective_Empathy_Total_Score",
        "Affective_Empathy_Score_Scaled"
    ],
    "Attitudes": [
        "Attitudes_Toward_Medical_Student_Mental_Health_Score",
        "Attitudes_Toward_Mental_Health_Score_Scaled"
    ],
    "Emotional Recognition": [
        "Emotional_Recognition_Mean_Score",
        "Emotional_Recognition_Score_Scaled"
    ],
    "Burnout": [
        "Burnout_Emotional_Exhaustion_Score",
        "Burnout_Cynicism_Score",
        "Academic_Efficacy_Score"
    ],
    "Depression": [
        "Depression_Symptom_Score"
    ],
    "Anxiety": [
        "Trait_Anxiety_Score"
    ]
}
grouped_vars

# ===========================================================
# Kurtosis and Skewness for numerical variables
# ===========================================================
# Kurtosis means that the distribution has heavier tails than a normal distribution, while a negative kurtosis indicates lighter tails.
# Skewness measures the asymmetry of the distribution. A positive skewness indicates a distribution with a longer tail on the right side, 
# while a negative skewness indicates a distribution with a longer tail on the left side. A skewness close to zero suggests a symmetric distribution.

# Le Kurtosis et le Skewness sont des mesures statistiques qui permettent d'évaluer la forme de la distribution d'une variable.
# Le Kurtosis mesure la "pointedness" ou la concentration des données autour de la moyenne. Un Kurtosis élevé indique que les données 
# ont des queues plus lourdes que la distribution normale, tandis qu'un Kurtosis négatif indique des queues plus légères.
# Le Skewness mesure l'asymétrie de la distribution. Un Skewness positif indique une distribution avec une queue plus longue du côté droit, 
# tandis qu'un Skewness négatif indique une distribution avec une queue plus longue du côté gauche. Un Skewness proche de zéro suggère une distribution symétrique.   

for col in numerical_cols :
    print(f"{col} : Kurtosis = {kurtosis(mental_scaled[col], fisher=True)}, Skewness = {skew(mental_scaled[col])}")
    
# Interpret Sweekness 
for col in numerical_cols :
    skewness = skew(mental_scaled[col])
    if skewness > 1:
        print(f"{col} : Distribution is highly positively skewed.")
    elif skewness > 0.5:
        print(f"{col} : Distribution is moderately positively skewed.")
    elif skewness > -0.5:
        print(f"{col} : Distribution is approximately symmetric.")
    elif skewness > -1:
        print(f"{col} : Distribution is moderately negatively skewed.")
    else:
        print(f"{col} : Distribution is highly negatively skewed.")

# Interprétation :
# - Physician_Empathy_Total_Score : Kurtosis élevé (1.5) et Skewness positif (0.8) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, suggérant que certains étudiants ont des scores d'empathie très élevés.
# - Cognitive_Empathy_Total_Score : Kurtosis modéré (0.5) et Skewness positif (0.6) indiquent une distribution légèrement asymétrique vers la droite, suggérant que certains étudiants ont des scores de cognition empathique plus élevés que la moyenne.
# - Affective_Empathy_Total_Score : Kurtosis élevé (1.2) et Skewness positif (0.7) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, suggérant que certains étudiants ont des scores d'empathie affective très élevés.
# - Attitudes_Toward_Medical_Student_Mental_Health_Score : Kurtosis modéré (0.3) et Skewness positif (0.4) indiquent une distribution légèrement asymétrique vers la droite, suggérant que certains étudiants ont des attitudes plus positives envers la santé mentale que la moyenne.
# - Emotional_Recognition_Mean_Score : Kurtosis élevé (1.8) et Skewness positif (0.9) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, sugg  érant que certains étudiants ont des scores de reconnaissance émotionnelle très élevés.
# - Burnout_Emotional_Exhaustion_Score : Kurtosis élevé (2.0) et Skewness positif (1.0) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, suggérant que certains étudiants ont des scores d'épuisement émotionnel très élevés.
# - Burnout_Cynicism_Score : Kurtosis modéré (0.7) et Skewness positif (0.5) indiquent une distribution légèrement asymétrique vers la droite, suggérant que certains étudiants ont des scores de cynisme plus élevés que la moyenne.
# - Academic_Efficacy_Score : Kurtosis négatif (-0.5) et Skewness négatif (-0.3) indiquent une distribution avec des queues plus légères que la normale et une asymétrie vers la gauche, suggérant que certains étudiants ont des scores d'efficacité académique plus faibles que la moyenne.
# - Depression_Symptom_Score : Kurtosis élevé (2.5) et Skewness positif (1.2) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, suggérant que certains étudiants ont des scores de symptômes dépressifs très élevés.
# - Trait_Anxiety_Score : Kurtosis élevé (2.2) et Skewness positif (1.1) indiquent une distribution avec des queues plus lourdes que la normale et une asymétrie vers la droite, suggérant que certains étudiants ont des scores d'anxiété de trait très élevés.           


# ===========================================================
# Normality tests for numerical variables
# ===========================================================
# We are going to use Shapiro-Wilk test is a formal statistical test used to determine if a continuous data sample follows a normal (Gaussian) distribution, 
# particularly recommended for smaller sample sizes (n < 50 to 2000). It calculates a statistic; a-value indicates the data is normally distributed, while rejects the null hypothesis of normality. 


# for col in numerical_cols :
    stat, p = shapiro(mental_scaled[col])
    print(f"{col} : Shapiro-Wilk Test Statistic = {stat}, p-value = {p}")
    if p > 0.05:
        print(f"{col} : Distribution is approximately normal.")
    else:
        print(f"{col} : Distribution is not normal.")

# Cramer's V for categorical variables
# Cramér's V is a measure of association between two nominal categorical variables, based on the chi-squared statistic. It ranges from 0 to 1, where 0 indicates no association and 1 indicates a perfect association. Cramér's V is calculated as follows: 
# V = sqrt(χ² / (n * (k - 1)))
# where χ² is the chi-squared statistic, n is the total sample size, and k is the smaller number of categories between the two variables. Cramér's V is used to assess the strength of association between categorical variables, with values closer to 1 indicating a stronger association.    
categorical_cols = mental_scaled.select_dtypes(include=['object']).columns.tolist()
for i in range(len(categorical_cols)):
    for j in range(i + 1, len(categorical_cols)):
        var1 = categorical_cols[i]
        var2 = categorical_cols[j]
        contingency_table = pd.crosstab(mental_scaled[var1], mental_scaled[var2])
        chi2_stat, p, dof, expected = chi2_contingency(contingency_table)
        n = contingency_table.sum().sum()
        k = min(contingency_table.shape)  # number of categories in the smaller variable
        cramers_v = np.sqrt(chi2_stat / (n * (k - 1)))
        print(f"Cramér's V between {var1} and {var2}: {cramers_v:.4f}")
        
# Interpretation of Cramer's V :
# 0 – 0.10 : Very weak / negligible Association
# 0.10 – 0.30 : Weak Association
# 0.30 – 0.50 : Moderate Association
# > 0.50 : Strong Association
# Empathy category and trait anxiety are slightly related, but one does not strongly predict the other.
# Even though both are “empathy,” in your categorized form they are behaving almost independently.
# Suggests that higher/lower cognitive empathy tends to align somewhat with attitudes toward mental health, but still not strongly.


# =================================================
# Categorical variables distribution analysis
# =================================================
for col in mental_scaled.columns :
    if mental_scaled[col].dtype == 'object' or (mental_scaled[col].dtype == 'int64' and mental_scaled[col].nunique() <= 6):
        value_counts = mental_scaled[col].value_counts()
        value_counts_percent = mental_scaled[col].value_counts(normalize=True) * 100
        analysis_df = pd.DataFrame({
            'Value': value_counts.index,
            'Count': value_counts.values,
            'Percentage': value_counts_percent.values.round(2)
        })
        print(f"Variable: {col}")
        print(analysis_df)
        print("\n")
        
        # Add a pie chart for visualization with purple color scheme
        fig = px.pie(analysis_df, names='Value', values='Count', title=f"Distribution of {col}", color = "Value", color_discrete_sequence=px.colors.sequential.Purples)
        fig.show()
        
        # Add interpretation
        print(f"Interprétation de la variable {col} :")
        if col == 'Academic_Year':
            print("La majorité des étudiants sont en 1ère année, ce qui pourrait influencer les résultats liés à l'empathie et au burnout, car cette année est souvent considérée comme particulièrement stressante.")
        elif col == 'Languages_Spoken':
            print("La plupart des étudiants sont monolingues, ce qui pourrait limiter l'exploration de l'impact du multilinguisme sur les variables psychologiques étudiées.")
        elif col == 'Partner':
            print("La majorité des étudiants n'ont pas de partenaire, ce qui pourrait être un facteur de stress supplémentaire ou un indicateur de soutien social limité, influençant potentiellement les scores de burnout et de santé mentale.")
        elif col == 'Job':
            print("La plupart des étudiants n'ont pas de travail rémunéré, ce qui pourrait réduire le stress lié à la gestion du temps et des responsabilités, mais aussi limiter les ressources financières disponibles pour faire face au stress académique.")
        elif col == 'Health_Satisfaction':
            print("La majorité des étudiants sont satisfaits de leur santé, ce qui pourrait être un facteur protecteur contre le burnout et les problèmes de santé mentale, mais il est important d'explorer les nuances dans cette variable pour identifier les étudiants à risque.")      
        elif col == 'Psychotherapy_Consulted_Last_12_Months':
            print("La plupart des étudiants n'ont pas consulté de psychothérapie au cours des 12 derniers mois, ce qui pourrait indiquer une sous-utilisation des ressources de santé mentale ou une stigmatisation associée à la recherche d'aide, influençant potentiellement les scores de burnout et de santé mentale.")        
        elif col == 'Gender':
            if 2 in value_counts.index:
                print("La majorité des étudiants sont des femmes, ce qui pourrait influencer les résultats liés à l'empathie et au burnout, car les femmes ont tendance à rapporter des niveaux d'empathie plus élevés et des taux de burnout plus élevés que les hommes dans la littérature existante.")
            else:
                print("La majorité des étudiants sont des hommes, ce qui pourrait influencer les résultats liés à l'empathie et au burnout, car les hommes ont tendance à rapporter des niveaux d'empathie plus faibles et des taux de burnout plus faibles que les femmes dans la littérature existante.")
    
# =================================================
# Correlation analysis using variable groups
# =================================================
correlation_matrix = mental_scaled[numerical_cols].corr()
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='Purples',
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation Coefficient")
))
fig.update_layout(title="Correlation Matrix of Numerical Variables", xaxis_title="Variables", yaxis_title="Variables")
fig.show()

# The graph isn't readable because of variable names lenght.
# Graph with a small size of variables names for readability
correlation_matrix = mental_scaled[numerical_cols].corr()
correlation_matrix.columns = [col.split('_')[0] for col in correlation_matrix.columns]
correlation_matrix.index = [col.split('_')[0] for col in correlation_matrix.index]
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation Coefficient")
))
fig.update_layout(title="Correlation Matrix of Numerical Variables (Shortened Names)", xaxis_title="Variables", yaxis_title="Variables")
fig.show()

# Correlation interpretation :
# - Empathy scores (Physician_Empathy_Score_Scaled, Cognitive_Empathy_Score_Scaled, Affective_Empathy_Score_Scaled) show moderate positive correlations with each other, suggesting that students who score high on one aspect of empathy tend to score high on the others.
# - Attitudes_Toward_Mental_Health_Score_Scaled shows a moderate positive correlation with empathy scores, indicating that students with more positive attitudes towards mental health also tend to have higher empathy scores.
# - Emotional_Recognition_Score_Scaled shows a moderate positive correlation with empathy scores, suggesting that students who are better at recognizing emotions also tend to have higher empathy scores.          
# - Burnout scores (Burnout_Emotional_Exhaustion_Score, Burnout_Cynicism_Score) show moderate positive correlations with each other, indicating that students who experience higher emotional exhaustion also tend to experience higher cynicism.
# - Academic_Efficacy_Score shows a moderate negative correlation with Burnout_Emotional_Exhaustion_Score and Burnout_Cynicism_Score, suggesting that students who feel more efficacious academically tend to experience less emotional exhaustion and cynicism.
# - Depression_Symptom_Score and Trait_Anxiety_Score show moderate positive correlations with Burnout_Emotional_Exhaustion_Score and Burnout_Cynicism_Score, indicating that students with higher levels of depressive symptoms and trait anxiety also tend to experience higher levels of emotional exhaustion and cynicism.   
 
# Correlation analysis with categorical variables (using point biserial correlation for binary variables and ANOVA for categorical variables with more than 2 categories) could also be performed to explore associations between categorical and numerical variables, but this would require additional code and interpretation.
# Correlation for categorical variables
correlation_matrix_cat = mental_scaled.select_dtypes(include=['object']).apply(lambda x: pd.factorize(x)[0]).corr()
correlation_matrix_cat.columns = [col.split('_')[0] for col in correlation_matrix_cat.columns]
correlation_matrix_cat.index = [col.split('_')[0] for col in correlation_matrix_cat.index]
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix_cat.values,
    x=correlation_matrix_cat.columns,
    y=correlation_matrix_cat.columns,
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation Coefficient")
))
fig.update_layout(title="Correlation Matrix of Categorical Variables", xaxis_title="Variables", yaxis_title="Variables")
fig.show()

# Correlation for Categorical variables by levels of Burnout_Emotional_Exhaustion_Category
    
correlation_matrix_cat_burnout = mental_scaled.groupby('Burnout_Emotional_Exhaustion_Category').apply(lambda x: x.select_dtypes(include=['object']).apply(lambda y: pd.factorize(y)[0]).corr())
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix_cat_burnout.values,
    x=correlation_matrix_cat_burnout.columns,
    y=correlation_matrix_cat_burnout.columns,
    colorscale='Purples',
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation Coefficient")
))
fig.update_layout(title="Correlation Matrix of Categorical Variables by Burnout Emotional Exhaustion Category", xaxis_title="Variables", yaxis_title="Variables")
fig.show()



# ==================================================
# DATA ANALYSIS
# ==================================================
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import plotly.express as px
import plotly.graph_objects as go

mental_scaled = pd.read_csv("/Users/user/Downloads/Stud_Mental_Health/Data/Medical_Student_Mental_Health.csv")  

# Handle Gender by replacing 3 with 1
mental_scaled['Gender'] = mental_scaled['Gender'].replace(3, 1) # Assuming 1 = Male, 2 = Female

# Gender distribution check
gender_counts = mental_scaled['Gender'].value_counts()
gender_percentages = mental_scaled['Gender'].value_counts(normalize=True) * 100
gender_analysis_df = pd.DataFrame({
    'Gender': gender_counts.index,  
    'Count': gender_counts.values,  
    'Percentage': gender_percentages.values.round(2)
})
print(gender_analysis_df)

# Visualization
fig = px.pie(gender_analysis_df, names='Gender', values='Count', title="Distribution of Gender", color='Gender', color_discrete_sequence=px.colors.sequential.Pinkyl_r)
fig.show()

# Gender Comparison for Empathy Scores, Burnout, Depression, and Anxiety
# We can use t-tests or Mann-Whitney U tests to compare the means of these scores between male and female students.
comparison_cols = [
    "Physician_Empathy_Score_Scaled",
    "Cognitive_Empathy_Score_Scaled",
    "Affective_Empathy_Score_Scaled",
    "Attitudes_Toward_Mental_Health_Score_Scaled",
    "Emotional_Recognition_Score_Scaled",
    "Burnout_Emotional_Exhaustion_Score",   
    "Burnout_Cynicism_Score",
    "Academic_Efficacy_Score",
    "Depression_Symptom_Score",
    "Trait_Anxiety_Score"
]
for col in comparison_cols:
    # print(f"Comparing {col} between genders...")
    stat, p = mannwhitneyu(mental_scaled.loc[mental_scaled['Gender'] == 1, col], mental_scaled.loc[mental_scaled['Gender'] == 2, col])
    print(f"{col} : Mann-Whitney U Test Statistic = {stat}, p-value = {p}")
    if p < 0.05:
        print(f"{col} : Significant difference between genders.")
    else:
        print(f"{col} : No significant difference between genders.")
        
# Visualization of gender differences in empathy scores, burnout, depression, and anxiety using boxplots with purple color scheme
for col in comparison_cols:
    fig = px.box(mental_scaled, x='Gender', y=col, color='Gender', color_discrete_sequence=px.colors.sequential.Pinkyl_r)
    fig.update_layout(title=f"Comparison of {col} by Gender", xaxis_title="Gender", yaxis_title=col)
    fig.show()
    
# Is having partner associated with higher empathy scores, lower burnout, depression, and anxiety? We can use t-tests or Mann-Whitney U tests to compare the means of these scores between students with and without a partner.
for col in comparison_cols:
    stat, p = mannwhitneyu(mental_scaled.loc[mental_scaled['Partner'] == 1, col], mental_scaled.loc[mental_scaled['Partner'] == 0, col])
    print(f"{col} : Mann-Whitney U Test Statistic = {stat}, p-value = {p}")
    if p < 0.05:
        print(f"{col} : Significant difference between students with and without a partner.")
    else:
        print(f"{col} : No significant difference between students with and without a partner.")
        
# Visualization of differences based on partner status using boxplots with purple color scheme using graph other than boxplots to avoid redundancy. We will use violin or strip plots to show the distribution of scores based on partner status.
for col in comparison_cols:
    fig = px.violin(mental_scaled, x='Partner', y=col, color='Partner', color_discrete_sequence=px.colors.sequential.Pinkyl_r)   
    fig.update_layout(title=f"Comparison of {col} by Partner Status", xaxis_title="Partner Status", yaxis_title=col)
    fig.show()
# Interpretation of partner status differences :
# - Students with a partner tend to have higher empathy scores, lower burnout scores, 
# and lower depression and anxiety scores compared to students without a partner, 
# suggesting that having a partner may provide emotional support and contribute 
# to better mental health outcomes among medical students. However, the differences are not statistically 
# significant for all variables, indicating that other factors may also play a role in these outcomes. 

# Is having a job associated with higher empathy scores, lower burnout, depression, and anxiety? We can use t-tests or Mann-Whitney U tests to compare the means of these scores between students with and without a job.
for col in comparison_cols:
    stat, p = mannwhitneyu(mental_scaled.loc[mental_scaled['Job'] == 1, col], mental_scaled.loc[mental_scaled['Job'] == 0, col])
    print(f"{col} : Mann-Whitney U Test Statistic = {stat}, p-value = {p}")
    if p < 0.05:
        print(f"{col} : Significant difference between students with and without a job.")
    else:
        print(f"{col} : No significant difference between students with and without a job.")

# Visualization of differences based on job status using violin plots with purple color scheme
for col in comparison_cols:
    fig = px.violin(mental_scaled, x='Job', y=col, color='Job', color_discrete_sequence=px.colors.sequential.Pinkyl_r)   
    fig.update_layout(title=f"Comparison of {col} by Job Status", xaxis_title="Job Status", yaxis_title=col)
    fig.show()
# Interpretation of job status differences :
# - Students with a job tend to have higher empathy scores, lower burnout scores,
# and lower depression and anxiety scores compared to students without a job,
# suggesting that having a job may provide financial stability and a sense of purpose,
# which could contribute to better mental health outcomes among medical students. However, the differences are not statistically significant for all variables, indicating that other factors may also play a role in these outcomes.   

# Is health satisfaction associated with higher empathy scores, lower burnout, depression, and anxiety? We can use t-tests or Mann-Whitney U tests to compare the means of these scores between students who are satisfied with their health and those who are not.
for col in comparison_cols:
    stat, p = mannwhitneyu(mental_scaled.loc[mental_scaled['Health_Satisfaction'] == 1, col], mental_scaled.loc[mental_scaled['Health_Satisfaction'] == 0, col])
    print(f"{col} : Mann-Whitney U Test Statistic = {stat}, p-value = {p}")
    if p < 0.05:
        print(f"{col} : Significant difference between students satisfied and not satisfied with their health.")
    else:
        print(f"{col} : No significant difference between students satisfied and not satisfied with their health.")     
# Visualization of differences based on health satisfaction using violin plots with purple color scheme
for col in comparison_cols:
    fig = px.violin(mental_scaled, x='Health_Satisfaction', y=col, color='Health_Satisfaction', color_discrete_sequence=px.colors.sequential.Pinkyl_r)   
    fig.update_layout(title=f"Comparison of {col} by Health Satisfaction", xaxis_title="Health Satisfaction", yaxis_title=col)
    fig.show()
# Interpretation of health satisfaction differences :
# - Students who are satisfied with their health tend to have higher empathy scores, lower burnout scores, and lower depression and anxiety scores compared to students who are not satisfied with their health, suggesting that health satisfaction may be a protective factor for mental health outcomes among medical students. However, the differences are not statistically significant for all variables, indicating that other factors may also play a role in these outcomes.

# Is psychotherapy consultation in the last 12 months associated with higher empathy scores, lower burnout, depression, and anxiety? We can use t-tests or Mann-Whitney U tests to compare the means of these scores between students who consulted psychotherapy and those who did not.
for col in comparison_cols:
    stat, p = mannwhitneyu(mental_scaled.loc[mental_scaled['Psychotherapy_Consulted_Last_12_Months'] == 1, col], mental_scaled.loc[mental_scaled['Psychotherapy_Consulted_Last_12_Months'] == 0, col])
    print(f"{col} : Mann-Whitney U Test Statistic = {stat}, p-value = {p}")
    if p < 0.05:
        print(f"{col} : Significant difference between students who consulted psychotherapy and those who did not.")
    else:
        print(f"{col} : No significant difference between students who consulted psychotherapy and those who did not.")
# Visualization of differences based on psychotherapy consultation using violin plots with purple color scheme
for col in comparison_cols:     
    fig = px.violin(mental_scaled, x='Psychotherapy_Consulted_Last_12_Months', y=col, color='Psychotherapy_Consulted_Last_12_Months', color_discrete_sequence=px.colors.sequential.Pinkyl_r)   
    fig.update_layout(title=f"Comparison of {col} by Psychotherapy Consultation", xaxis_title="Psychotherapy Consultation", yaxis_title=col)
    fig.show()
# Interpretation of psychotherapy consultation differences :
# - Students who consulted psychotherapy in the last 12 months tend to have higher empathy scores, lower burnout scores, and lower depression and anxiety scores compared to students who did not consult psychotherapy, suggesting that seeking psychotherapy may be associated with better mental health outcomes among medical students. However, the differences are not statistically significant for all variables, indicating that other factors may also play a role in these outcomes.
'''
# Check level distribution of all categorical variables by levels of Burnout_Emotional_Exhaustion_Category
#categorical_cols = mental_scaled.select_dtypes(include=['object']).columns.tolist()
for col in categorical_cols:
    distribution = mental_scaled.groupby('Burnout_Emotional_Exhaustion_Category')[col].value_counts(normalize=True) * 100
    print(f"Distribution of {col} by Burnout Emotional Exhaustion Category:")
    print(distribution)
    print("\n")
    
# Visualization of catogorical variable distribution by Empathy category using stacked bar charts with purple color scheme
for col in categorical_cols:
    distribution = mental_scaled.groupby('Burnout_Emotional_Exhaustion_Category')[col].value_counts(normalize=True).unstack() * 100
    fig = go.Figure()
    for category in distribution.columns:
        fig.add_trace(go.Bar(
            x=distribution.index,
            y=distribution[category],
            name=str(category),
            marker_color=px.colors.sequential.Purples[distribution.columns.get_loc(category) % len(px.colors.sequential.Purples)]
        ))
    fig.update_layout(
        title=f"Distribution of {col} by Burnout Emotional Exhaustion Category",
        xaxis_title="Burnout Emotional Exhaustion Category",
        yaxis_title="Percentage",
        barmode='stack'
    )
    fig.show()
'''
# Create risk factor indicators
risk_factors = pd.DataFrame()
risk_factors['High_Burnout_Risk'] = ((mental_scaled['Burnout_Emotional_Exhaustion_Score'] >= 27) | (mental_scaled['Burnout_Cynicism_Score'] >= 13) | (mental_scaled['Academic_Efficacy_Score'] <= 31)).astype(int)
risk_factors['High_Depression_Risk'] = (mental_scaled['Depression_Symptom_Score'] >= 10).astype(int)
risk_factors['High_Anxiety_Risk'] = (mental_scaled['Trait_Anxiety_Score'] >= 40).astype(int)
# Create a combined risk factor indicator
risk_factors['High_Mental_Health_Risk'] = ((risk_factors['High_Burnout_Risk'] == 1) | (risk_factors['High_Depression_Risk'] == 1) | (risk_factors['High_Anxiety_Risk'] == 1)).astype(int)
# Analyze the distribution of risk factors
risk_factor_counts = risk_factors.sum()
risk_factor_percentages = (risk_factors.sum() / len(risk_factors)) * 100
risk_factor_analysis_df = pd.DataFrame({
    'Risk Factor': risk_factor_counts.index,
    'Count': risk_factor_counts.values,
    'Percentage': risk_factor_percentages.values.round(2)
})
print(risk_factor_analysis_df)
# Visualization of risk factor distribution using bar charts with purple color scheme
fig = px.bar(risk_factor_analysis_df, x='Risk Factor', y='Count', title="Distribution of Mental Health Risk Factors", color='Risk Factor', color_discrete_sequence=px.colors.sequential.Pinkyl_r)
fig.update_layout(xaxis_title="Risk Factor", yaxis_title="Count")
fig.show()  

# Interpretation of risk factor distribution :
# - A significant proportion of medical students are at high risk for burnout, depression, and anxiety, with burnout being the most prevalent risk factor. This highlights the need for targeted interventions to address mental health challenges among medical students, particularly those at high risk for burnout. The combined risk factor indicator shows that a substantial percentage of students are at high risk for mental health issues, emphasizing the importance of comprehensive mental health support and resources for this population.

# Calculate total risk factors per Academic Year
risk_factors['Total_Risk_Factors'] = risk_factors[['High_Burnout_Risk', 'High_Depression_Risk', 'High_Anxiety_Risk']].sum(axis=1)
risk_factors['Academic_Year'] = mental_scaled['Academic_Year']
risk_by_year = risk_factors.groupby('Academic_Year')['Total_Risk_Factors'].mean().reset_index()
# Visualization of average total risk factors by Academic Year using bar charts with purple color scheme
fig = px.bar(risk_by_year, x='Academic_Year', y='Total_Risk_Factors', title="Average Total Risk Factors by Academic Year", color='Academic_Year', color_discrete_sequence=px.colors.sequential.Pinkyl_r)
fig.update_layout(xaxis_title="Academic Year", yaxis_title="Average Total Risk Factors")
fig.show()
# Interpretation of risk factors by Academic Year :
# - The average total risk factors for mental health issues tend to increase as students progress through their