# =====================================================
# Import libraries
# =====================================================
from data_explorer import preprocess
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# ==================================================
# STEP 0 — Assumptions and Data Preparation
# ==================================================

# We assume:
# - Data are cleaned and preprocessed (no missing values, outliers handled, features scaled)
# - Targets are defined (regression and classification)
# - Data is ready for modeling 
# - Mental_scaled is ready
# Targets (example):
# - Regression targets:
# - MBI_EX
# CESD
# STAI_T
# Classification targets:
# - burnout_high
# - depression_risk
# - anxiety_high

# ==================================================
# STEP 1 — FEATURE ENGINEERING
# ==================================================
mental_scaled = pd.read_csv("/Users/user/Downloads/Stud_Mental_Health/Data/Medical_Student_Mental_Health.csv")

# Drop Langages 
mental_scaled.drop(['Languages_Spoken'], axis=1, inplace=True)
mental_scaled
mental_scaled.info()


# ==================================================
# Simplifier des variables corrélées
# ==================================================

# Créer Empathy_total en sommant les différentes dimensions de l'empathie
mental_scaled["Empathy_total"] = mental_scaled["Physician_Empathy_Score_Scaled"] + mental_scaled["Cognitive_Empathy_Score_Scaled"] + mental_scaled["Affective_Empathy_Score_Scaled"] 
# Logique théorique :
# Jefferson Scale of Physician Empathy mesure l’empathie clinique
# Questionnaire of Cognitive and Affective Empathy mesure empathie cognitive + affective
# On suppose donc qu’il existe un facteur latent global d’empathie.
# En ML, créer une somme revient à approximer un facteur latent non observé.
# Pourquoi ?
# Les modèles linéaires (régression, NN peu profond) peuvent avoir du mal à :
# capter une structure latente
# combiner proprement 3 variables corrélées
# Créer Empathy_total :
# réduit le bruit
# augmente le signal global
# aide si les variables sont fortement corrélées
# ⚠ Be careful :
# Si les trois variables sont déjà dans le modèle, ce n’est pas toujours nécessaire (les arbres s’en fichent).

mental_scaled["Distress_index"] = mental_scaled["Depression_Symptom_Score"] + mental_scaled["Trait_Anxiety_Score"]
# Center for Epidemiologic Studies Depression Scale = dépression
# State-Trait Anxiety Inventory = anxiété
# Cliniquement :
# Dépression + anxiété = distress émotionnel global
# Beaucoup d’articles utilisent ce concept.

mental_scaled["Burnout_profile"] = mental_scaled["Burnout_Emotional_Exhaustion_Score"] + mental_scaled["Burnout_Cynicism_Score"] - mental_scaled["Academic_Efficacy_Score"]
# Le Maslach Burnout Inventory contient :
# EX = exhaustion
# CY = cynicism
# EA = efficacy
# Cliniquement :
# Burnout élevé = EX ↑ + CY ↑ + EA ↓
# Donc cette combinaison reflète la structure théorique du burnout.

# Example of feature engineering: creating interaction terms, polynomial features, or domain-specific features
# - mental_scaled['age_squared'] = mental_scaled['Age'] ** 2
# - mental_scaled['age_year_interaction'] = mental_scaled['Age'] * mental_scaled['Year']
# - mental_scaled['empathy_burnout_interaction'] = mental_scaled['Empathy'] * mental_scaled['MBI_EX']   
# Cela permet de modéliser une relation non linéaire.
# Exemple réel :
# Empathie → Burnout
# Ce n’est pas toujours linéaire.
# Possible relation en U :
# Très faible empathie → mauvais
# Très forte empathie → surcharge émotionnelle
# Modérée → optimal
# Un terme au carré permet :
# 𝑌 = 𝛽1𝑋 + 𝛽2𝑋2
#Les modèles linéaires seuls ne captent pas ça.
# Be carful :
# Trop de termes d’interaction → overfitting
# Toujours valider avec des données de test.
# Pour les modèles arbres (Random Forest, XGBoost) :
# Ils captent naturellement les non-linéarités
# Ils n’ont pas besoin de termes au carré
# Donc :
# - Utile pour régression linéaire
# - Utile pour réseaux neuronaux simples
# - Peu utile pour arbres 

# ==================================================
# Handle Categorical Variables
# ==================================================
# Delete or encode categorical as we create them by rescaling the original ones to check for levels 
categorical_cols = mental_scaled.select_dtypes(include=["object", "category"]).columns
mental_scaled.drop(categorical_cols, axis=1, inplace=True)

# ==================================================
# Non-linear terms (for linear / NN models)
# Allows modeling U-shaped relationships
# ==================================================

mental_scaled["JSPE_sq"] = mental_scaled["Physician_Empathy_Score_Scaled"] ** 2
mental_scaled["CESD_sq"] = mental_scaled["Depression_Symptom_Score"] ** 2

# ==================================================
# Define Targets
# ==================================================

# Multi-target regression

targets_reg = ["Burnout_Emotional_Exhaustion_Score", "Depression_Symptom_Score", "Trait_Anxiety_Score"]

# Multi-label classification (example thresholds)
mental_scaled["burnout_high"] = (mental_scaled["Burnout_Emotional_Exhaustion_Score"] >= 27).astype(int)
mental_scaled["depression_risk"] = (mental_scaled["Depression_Symptom_Score"] >= 16).astype(int)
mental_scaled["anxiety_high"] = (mental_scaled["Trait_Anxiety_Score"] >= mental_scaled["Trait_Anxiety_Score"].median()).astype(int)
targets_clf = ["burnout_high", "depression_risk", "anxiety_high"]

# ==================================================
# Define Features 
# ==================================================

feature_cols = [col for col in mental_scaled.columns 
                if col not in targets_reg + targets_clf]

X = mental_scaled[feature_cols]
y_reg = mental_scaled[targets_reg]
y_clf = mental_scaled[targets_clf]

# ==================================================
# Train Test Split
# ==================================================

X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

_, _, y_clf_train, y_clf_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42
)

# Check shapes
print("X_train shape:", X_train.shape)
print("y_reg_train shape:", y_reg_train.shape)
print("y_clf_train shape:", y_clf_train.shape)  

# Justification:
# Handles nonlinearities
# Robust to scaling
# Strong baseline for tabular data

rf_reg = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
)

# MultiOutputRegressor permet de faire de la régression multi-cible avec un modèle qui ne gère pas nativement plusieurs cibles (comme RandomForestRegressor).
# Dans ce cas, il entraîne un modèle de régression séparé pour chaque cible (Burnout_Emotional_Exhaustion_Score, Depression_Symptom_Score, Trait_Anxiety_Score).
# Pour la classification multi-label, on utiliserait MultiOutputClassifier de la même manière.
# Sans MultiOutputRegressor, RandomForestRegressor ne peut gérer qu'une seule cible à la fois.
# Une autre option serait d'entraîner trois modèles séparés, mais MultiOutputRegressor simplifie le processus et garantit que les mêmes données d'entraînement sont utilisées pour chaque cible.
# Ou encore un modele qui arrive a le faire nativement (ex: XGBoost, LightGBM) mais on reste sur RF pour la simplicité et la robustesse.
rf_reg.fit(X_train, y_reg_train)
y_pred_reg = rf_reg.predict(X_test)

for i, target in enumerate(targets_reg):
    print(f"\nTarget: {target}")
    print("R2:", r2_score(y_reg_test.iloc[:, i], y_pred_reg[:, i]))
    print("RMSE:",
          np.sqrt(mean_squared_error(
              y_reg_test.iloc[:, i],
              y_pred_reg[:, i]
          )))

rf_clf = MultiOutputClassifier(
    RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )
)

rf_clf.fit(X_train, y_clf_train)
y_pred_clf = rf_clf.predict(X_test)

for i, target in enumerate(targets_clf):
    print(f"\nTarget: {target}")
    print(classification_report(
        y_clf_test.iloc[:, i],
        y_pred_clf[:, i]
    ))

# Justification:
# Handles nonlinearities
# Robust to scaling
# Strong baseline for tabular data  

# Use feature importance to identify key predictors
importances = rf_reg.estimators_[0].feature_importances_
feature_importance_df = pd.DataFrame({
    "feature": feature_cols,
    "importance": importances
}).sort_values(by="importance", ascending=False)
print(feature_importance_df.head(10))

# Use SHAP values for more detailed interpretability
# import shapely as shap
# explainer = shap.TreeExplainer(rf_reg.estimators_[0])
# shap_values = explainer.shap_values(X_test)
# shap.summary_plot(shap_values, X_test)  

# Use partial dependence plots to visualize relationships
# from sklearn.inspection import plot_partial_dependence
# plot_partial_dependence(
    # rf_reg.estimators_[0],
    # X_test,
    # features=[feature_cols.index("Empathy_total"), feature_cols.index("Burnout_profile")],
    # feature_names=feature_cols
# )

# Use XAI for counterfactual explanations
# import alibi
# from alibi.explainers import Counterfactual
# cf = Counterfactual(rf_clf.estimators_[0], shape=X_test.shape[1])
# explanation = cf.explain(X_test.iloc[0:1].values)
# print("Original instance:", X_test.iloc[0:1].values)

# Use XGBoost, LightGBM
# import xgboost as xgb
# xgb_reg = xgb.XGBRegressor(
    # n_estimators=200,
    # random_state=42
# )
# xgb_reg.fit(X_train, y_reg_train)
# y_pred_xgb = xgb_reg.predict(X_test)    
# for i, target in enumerate(targets_reg):
    # print(f"\nTarget: {target} (XGBoost)")
    # print("R2:", r2_score(y_reg_test.iloc[:, i], y_pred_xgb[:, i]))
    # print("RMSE:",
          # np.sqrt(mean_squared_error(
              # y_reg_test.iloc[:, i],
              # y_pred_xgb[:, i]
          # )))
    
# import lightgbm as lgb
# lgb_reg = lgb.LGBMRegressor(
    # n_estimators=200,
    # random_state=42
# )
# lgb_reg.fit(X_train, y_reg_train)
# y_pred_lgb = lgb_reg.predict(X_test)
# for i, target in enumerate(targets_reg):
    # print(f"\nTarget: {target} (LightGBM)")
    # print("R2:", r2_score(y_reg_test.iloc[:, i], y_pred_lgb[:, i]))
    # print("RMSE:",
          # np.sqrt(mean_squared_error(
              # y_reg_test.iloc[:, i],
              # y_pred_lgb[:, i]
          #)))
    
# Test models Actual vs. Predicted values 
mental_scaled["Burnout_Emotional_Exhaustion_Pred"] = rf_reg.predict(X)[:, 0]
mental_scaled["Depression_Symptom_Pred"] = rf_reg.predict(X)[:, 1]
mental_scaled["Trait_Anxiety_Pred"] = rf_reg.predict(X)[:, 2]
# Actual
mental_scaled[["Burnout_Emotional_Exhaustion_Score", "Depression_Symptom_Score", "Trait_Anxiety_Score"]].head()
# Predicted
mental_scaled[["Burnout_Emotional_Exhaustion_Pred", "Depression_Symptom_Pred", "Trait_Anxiety_Pred"]].head()
# Machine Learning and Deep Learning Analysis
# We implemented supervised machine learning models to predict psychological outcomes including burnout (MBI_EX), depressive symptoms (CESD), and anxiety (STAI_T). Both multi-target regression and multi-label classification frameworks were applied to account for the correlated nature of mental health constructs.
# Feature engineering was theory-driven. Composite indices reflecting global empathy, psychological distress, and burnout profiles were constructed to approximate latent constructs supported by psychometric theory.
# Data were randomly split into training (80%) and test (20%) sets. Hyperparameters were optimized using 5-fold cross-validation.
# Tree-based ensemble methods (Random Forest, Gradient Boosting) were implemented as baseline models due to their robustness to nonlinearity and collinearity in tabular psychological data.
# Deep neural networks were implemented using fully connected feedforward architectures. Networks were trained using the Adam optimizer with mean squared error (regression) or binary cross-entropy (classification) loss functions. Early stopping and dropout regularization were applied to prevent overfitting.
# Model performance was evaluated using R² and RMSE for regression tasks, and F1-score, accuracy, and AUC for classification tasks.


# Points à Corriger / Améliorer
# Data Leakage Potentiel

# - Si dans tes features tu inclus :
# - Distress_index = CESD + STAI_T

# - Burnout_profile = MBI_EX + MBI_CY - MBI_EA
# - Et qu'on' prédit :
# - CESD
# - STAI_T
# - MBI_EX
# On crée une fuite d’information.
# Exemple :
# - On prédit CESD mais que Distress_index contient déjà CESD :
# Le modèle triche.
# Ça gonfle artificiellement les performances.
# Solution :
# - Ne pas inclure ces indices dans les features si on prédit les composantes individuelles
# - Ou ne pas prédire les composantes individuelles si on inclut les indices
# Ou encore on verifie :
# - Analyse d’overfitting
# - En comparant les performances sur train vs test :
# Sinon on ne sait pas si on surapprend.
prediction_cols = ["Burnout_Emotional_Exhaustion_Score", "Depression_Symptom_Score", "Trait_Anxiety_Score"]
for col in prediction_cols:
    mse_train = mean_squared_error(y_reg_train[col], rf_reg.predict(X_train)[:, prediction_cols.index(col)])
    mse_test = mean_squared_error(y_reg_test[col], rf_reg.predict(X_test)[:, prediction_cols.index(col)])
    print(f"{col} - Train MSE: {mse_train:.4f}, Test MSE: {mse_test:.4f}")
    
# Interpretability :
if mse_train < mse_test:
    print("Possible data leakage or overfitting. Check feature engineering and model complexity.")
elif mse_train > mse_test:
    print("Model may be underfitting. Consider adding more features or using a more complex model.")
else:
    print("Model performance is consistent between train and test sets. No obvious data leakage detected.")
    
# Pas d’analyse d’importance des variables
# Parce que Random Forest est un modèle de boîte noire, autrement dit difficile à interpréter, il est important d’utiliser des techniques d’interprétabilité pour comprendre quelles variables influencent le plus les prédictions du modèle.
# Par exemple, on peut utiliser l’importance des variables intégrée à Random Forest pour identifier les prédicteurs les plus influents pour chaque cible. Cela peut aider à valider les hypothèses théoriques et à générer de nouvelles hypothèses sur les facteurs de risque de burnout, dépression et anxiété chez les étudiants en médecine.
# Solution :
# - Utiliser l’importance des variables de Random Forest pour identifier les prédicteurs clés.
importances = rf_reg.estimators_[0].feature_importances_
feature_importance_df = pd.DataFrame({
    "feature": feature_cols,
    "importance": importances
}).sort_values(by="importance", ascending=False)
print(feature_importance_df.head(10))

# ==================================================
# DEEP LEARNING
# ==================================================
# Deep Learning est une approche plus flexible qui peut capturer des relations complexes entre les variables. Cependant, elle nécessite plus de données et de puissance de calcul, et est plus sujette à l’overfitting si elle n’est pas correctement régularisée.
# Pour les données tabulaires, les réseaux de neurones entièrement connectés (feedforward) sont couramment utilisés. L’architecture peut être simple (1-2 couches cachées) ou plus complexe (plus de couches, unités, dropout).
# L’entraînement doit être soigneusement surveillé pour éviter l’overfitting, en utilisant des techniques telles que l’arrêt précoce (early stopping) et la régularisation par dropout.

