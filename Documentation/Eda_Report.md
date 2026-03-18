# COMPREHENSIVE EXPLORATORY DATA ANALYSIS REPORT
## Medical Student Mental Health Dataset

**Analysis Date:** February 13, 2026  
**Dataset:** Data_2022_MedTeach.csv  
**Sample Size:** N = 886 medical students

---

## EXECUTIVE SUMMARY

This comprehensive analysis reveals a **mental health crisis among medical students**, with over half showing depression risk and 60% experiencing high anxiety. The analysis examined demographic, psychological, and behavioral variables across 886 medical students, revealing critical patterns in mental health, empathy, and burnout.

### Key Alarming Findings:
- **52.0%** of students meet criteria for depression risk (CES-D ≥ 16)
- **60.3%** experience high trait anxiety (STAI-T ≥ 40)
- **44.4%** have comorbid depression AND anxiety
- **48.9%** have 3 or more mental health risk factors
- **22.5%** consulted psychotherapy in the past 12 months

---

## 1. DATASET OVERVIEW

### 1.1 Sample Characteristics
- **Total Participants:** 886
- **Age:** Mean = 22.4 years (SD = 3.3, Range: 17-49)
- **Gender Distribution:**
  - Female: 606 (68.4%)
  - Male: 275 (31.0%)
  - Other: 5 (0.6%)
- **Academic Year:**
  - Year 1: 245 (27.7%)
  - Year 2: 135 (15.2%)
  - Year 3: 143 (16.1%)
  - Year 4: 123 (13.9%)
  - Year 5: 127 (14.3%)
  - Year 6: 113 (12.8%)

### 1.2 Behavioral Characteristics
- **Study Hours per Week:** Mean = 25.3 hours (SD = 15.9)
- **Has Partner:** 499 (56.3%)
- **Employed:** 309 (34.9%)
- **Health Satisfaction:** Mean = 3.78/5 (SD = 1.06)

### 1.3 Data Quality
✅ **Complete Dataset:** No missing values in original data  
✅ **No Duplicates:** All 886 participants have unique IDs  
✅ **Consistent Ranges:** All scores within expected theoretical bounds  
⚠️ **Post-Processing:** 169 implausible language values (>7) recoded as missing

---

## 2. MENTAL HEALTH CRISIS INDICATORS

### 2.1 Depression (CES-D Scale)
- **Mean Score:** 18.05 (SD = 11.48, Range: 0-56)
- **At Risk (≥16):** 461 students (52.0%)
- **Severe (≥22):** 301 students (34.0%)
- **Theoretical Cutoff:** Scores ≥16 indicate clinical depression risk

### 2.2 Anxiety (STAI-T Scale)
- **Mean Score:** 42.90 (SD = 11.98, Range: 20-77)
- **High Anxiety (≥40):** 534 students (60.3%)
- **Very High (≥50):** 253 students (28.6%)
- **Clinical Interpretation:** Scores ≥40 indicate elevated trait anxiety

### 2.3 Burnout (Maslach Burnout Inventory)

**Emotional Exhaustion (MBI-EX):**
- Mean: 16.88 (SD = 5.26, Range: 5-30)
- High (≥27): 37 students (4.2%)
- Moderate (17-26): Majority of sample
- Low (≤16): 459 students (51.8%)

**Cynicism (MBI-CY):**
- Mean: 10.08 (SD = 4.59, Range: 4-24)
- High (≥13): 237 students (26.7%)
- Moderate (7-12): 346 students (39.1%)
- Low (≤6): 303 students (34.2%)

**Academic Efficacy (MBI-EA):**
- Mean: 24.21 (SD = 4.63, Range: 10-36)
- **Low (<32):** 845 students (95.4%) ⚠️
- Moderate (32-38): 37 students (4.2%)
- High (≥39): 4 students (0.5%)

### 2.4 Mental Health Service Utilization
- **Psychotherapy Consultation (past 12 months):** 199 students (22.5%)

### 2.5 Co-morbidity Analysis
- **Depression + Anxiety:** 393 students (44.4%)
- **Depression + Anxiety + Burnout:** 31 students (3.5%)

### 2.6 Risk Factor Accumulation
- **0 risk factors:** 28 (3.2%) - Very few students are completely well
- **1 risk factor:** 234 (26.4%)
- **2 risk factors:** 191 (21.6%)
- **3+ risk factors:** 433 (48.9%) - Nearly half the sample

---

## 3. EMPATHY & EMOTIONAL COMPETENCE

### 3.1 Physician Empathy (JSPE)
- **Mean:** 106.37 (SD = 8.78, Range: 67-125)
- **Theoretical Range:** 20-140 (higher = more empathetic)
- **Interpretation:** Sample shows relatively high empathy levels
- **Coefficient of Variation:** 8.26% (low variability, homogeneous group)

### 3.2 Cognitive Empathy (QCAE-COG)
- **Mean:** 58.53 (SD = 6.57, Range: 37-76)
- **Theoretical Range:** 19-76
- **CV:** 11.23% (low variability)

### 3.3 Affective Empathy (QCAE-AFF)
- **Mean:** 34.78 (SD = 5.38, Range: 18-48)
- **Theoretical Range:** 12-48
- **CV:** 15.46% (moderate variability)

### 3.4 Emotion Recognition (GERT)
- **Mean:** 0.72 (SD = 0.09, Range: 0.36-0.95)
- **Interpretation:** 72% accuracy in recognizing emotions
- **Scale:** Proportion correct (0-1)

### 3.5 Academic Motivation (AMSP)
- **Mean:** 23.15 (SD = 4.99, Range: 6-35)
- **Theoretical Range:** 7-35

---

## 4. CRITICAL CORRELATIONS

### 4.1 Mental Health Inter-Correlations (p < 0.001)
1. **Depression ↔ Anxiety:** r = 0.716 (Strong positive) ⚠️
2. **Depression ↔ Emotional Exhaustion:** r = 0.606 (Strong positive)
3. **Anxiety ↔ Emotional Exhaustion:** r = 0.530 (Strong positive)
4. **Cynicism ↔ Academic Efficacy:** r = -0.566 (Strong negative)
5. **Emotional Exhaustion ↔ Academic Efficacy:** r = -0.481 (Moderate negative)

**Interpretation:** Mental health symptoms are highly interconnected, suggesting a systemic crisis rather than isolated issues.

### 4.2 Empathy × Mental Health Relationships
1. **Affective Empathy ↔ Anxiety:** r = 0.331 (Moderate positive) ⚠️
2. **Affective Empathy ↔ Depression:** r = 0.251 (Weak positive)
3. **Affective Empathy ↔ Emotional Exhaustion:** r = 0.216 (Weak positive)

**Key Finding:** Higher affective empathy is associated with WORSE mental health outcomes, suggesting emotional contagion or compassion fatigue.

### 4.3 Study Hours Relationships
- **Study Hours → Depression:** r = 0.173 (p < 0.001)
- **Study Hours → Anxiety:** r = 0.117 (p < 0.001)
- **Study Hours → Emotional Exhaustion:** r = 0.188 (p < 0.001)

---

## 5. GROUP COMPARISONS

### 5.1 Gender Differences (Independent t-tests)

**Mental Health - Females significantly worse:**
- Depression (CES-D): Female = 19.91 vs Male = 14.00, **p < 0.001**, d = -0.55
- Anxiety (STAI-T): Female = 45.02 vs Male = 38.27, **p < 0.001**, d = -0.59
- Emotional Exhaustion: Female = 17.46 vs Male = 15.62, **p < 0.001**, d = -0.35

**Empathy - Females significantly higher:**
- Physician Empathy (JSPE): Female = 107.01 vs Male = 104.83, **p < 0.001**, d = -0.25
- Cognitive Empathy: Female = 59.01 vs Male = 57.41, **p < 0.001**, d = -0.24
- Affective Empathy: Female = 36.06 vs Male = 31.91, **p < 0.001**, d = -0.83 (large effect!)

### 5.2 Academic Year Trends (ANOVA, all p < 0.001)

**Depression (CES-D) decreases with year:**
- Year 1: 21.92 → Year 6: 13.64 (38% reduction)

**Emotional Exhaustion decreases:**
- Year 1: 17.68 → Year 6: 14.03 (21% reduction)

**Physician Empathy increases:**
- Year 1: 101.65 → Year 6: 109.03 (7% increase)

**Interpretation:** Mental health improves with academic progression, possibly due to adaptation, resilience development, or survivor bias.

### 5.3 Psychotherapy Consultation Comparison

**Students who consulted psychotherapy have significantly worse mental health:**
- Depression: 23.77 vs 16.39 (p < 0.001)
- Anxiety: 49.42 vs 41.01 (p < 0.001)
- Emotional Exhaustion: 18.61 vs 16.38 (p < 0.001)
- Physician Empathy: No significant difference (p = 0.149)

**Interpretation:** Appropriately, students with worse mental health are seeking help.

---

## 6. PREDICTIVE RELATIONSHIPS

### 6.1 Predicting Depression (CES-D)
- **Anxiety (STAI-T):** R² = 0.512 (51% of variance explained) ⭐
- **Emotional Exhaustion:** R² = 0.367 (37% of variance)
- **Affective Empathy:** R² = 0.063 (6% of variance)
- **Study Hours:** R² = 0.030 (3% of variance)

### 6.2 Predicting Emotional Exhaustion (MBI-EX)
- **Depression (CES-D):** R² = 0.367 (37% of variance) ⭐
- **Anxiety (STAI-T):** R² = 0.281 (28% of variance)
- **Affective Empathy:** R² = 0.047 (5% of variance)
- **Study Hours:** R² = 0.035 (3% of variance)

---

## 7. DISTRIBUTION ANALYSIS

### 7.1 Normality Tests (Shapiro-Wilk)
**All variables rejected normality (p < 0.05)**, indicating need for non-parametric tests or transformations for certain analyses.

**Notable Skewness:**
- Age: 2.074 (highly right-skewed, due to older students)
- Depression (CES-D): 0.682 (moderately right-skewed)
- Emotional Exhaustion: 0.102 (fairly symmetric)
- Physician Empathy: -0.664 (moderately left-skewed, ceiling effect)

### 7.2 Outlier Detection (IQR Method)

**Clinical Scores (retained as valid):**
- Depression: 8 outliers (0.9%) - severe cases
- Anxiety: 2 outliers (0.2%) - extreme anxiety
- Emotional Exhaustion: 0 outliers

**Empathy Scores:**
- JSPE: 13 outliers (1.5%) - unusually low empathy
- QCAE-COG: 7 outliers (0.8%) - low cognitive empathy
- QCAE-AFF: 2 outliers (0.2%) - low affective empathy

---

## 8. ASSESSMENT OF YOUR PREPROCESSING

1. **Excellent Rescaling Approach:**
   - Linear transformation to 0-100 scale is appropriate
   - Preserves relative differences and distributions
   - Makes comparisons across instruments intuitive
   - Documented theoretical ranges clearly

2. **Smart Clinical Cutoff Preservation:**
   - Correctly kept CES-D, STAI-T, and MBI in original scales
   - Allows use of established clinical thresholds
   - Added categorical variables for interpretability

3. **Appropriate Outlier Handling:**
   - Languages > 7 → NaN (correct decision)
   - Age > 30 retained (verified with year of study)
   - Clinical scores retained (genuine severity)

4. **Good Documentation:**
   - Clear variable renaming for interpretability
   - Rescaling formulas documented
   - Categorization thresholds specified

### 8.2 Recommendations for Improvement 💡

1. **Consider Log Transformation:**
   - For highly skewed variables (age, study hours)
   - May improve model performance in ML phase

2. **Additional Feature Engineering:**
   ```python
   # Composite mental health risk score
   df['mental_health_risk_score'] = (
       (df['cesd'] >= 16).astype(int) +
       (df['stai_t'] >= 40).astype(int) +
       (df['mbi_ex'] >= 27).astype(int) +
       (df['mbi_ea'] < 32).astype(int)
   )
   
   # Empathy composite
   df['total_empathy'] = (
       df['JSPE_scaled'] + 
       df['QCAE_COG_scaled'] + 
       df['QCAE_AFF_scaled']
   ) / 3
   ```

3. **Interaction Terms for ML:**
   ```python
   # Gender × Empathy interactions (given strong gender effects)
   df['gender_x_affective_empathy'] = df['sex'] * df['qcae_aff']
   
   # Year × Mental health (given improvement over time)
   df['year_x_depression'] = df['year'] * df['cesd']
   ```

4. **Missing Value Imputation Strategy:**
   - For Languages_Spoken NaN values, consider:
     - Mode imputation (most common = 1)
     - Separate "Unknown" category
     - Predictive imputation based on other demographics

5. **Standardization for ML:**
   ```python
   from sklearn.preprocessing import StandardScaler
   
   # For ML models, standardize continuous variables
   scaler = StandardScaler()
   df_scaled = df.copy()
   continuous_vars = ['age', 'stud_h', 'jspe', 'qcae_cog', ...]
   df_scaled[continuous_vars] = scaler.fit_transform(df[continuous_vars])
   ```

### 8.3 Data Validation Checks to Add ✅

```python
# 1. Check for logical inconsistencies
assert (df['year'] >= 1) & (df['year'] <= 6).all()
assert (df['age'] >= 17).all()
assert (df['health'] >= 1) & (df['health'] <= 5).all()

# 2. Verify rescaling
assert df['JSPE_scaled'].between(0, 100).all()
assert df['QCAE_COG_scaled'].between(0, 100).all()

# 3. Check categories match scores
high_jspe = df[df['JSPE_Category'] == 'Élevé']
assert (high_jspe['JSPE_scaled'] >= 67).all()
```

---

## 9. IMPLICATIONS FOR ML/DL MODELING

### 9.1 Recommended Target Variables
1. **Depression Risk (Binary):** CES-D ≥ 16 (52% prevalence - balanced)
2. **High Anxiety (Binary):** STAI-T ≥ 40 (60% prevalence - slightly imbalanced)
3. **Mental Health Risk Score (Ordinal):** 0-4 risk factors
4. **Emotional Exhaustion (Continuous):** MBI-EX score

### 9.2 Feature Selection Priorities

**High Predictive Power (based on correlations):**
1. Anxiety ↔ Depression (r = 0.72) - strongest predictor
2. Emotional Exhaustion ↔ Depression (r = 0.61)
3. Affective Empathy ↔ Anxiety (r = 0.33)
4. Study Hours ↔ Mental Health (moderate correlations)

**Demographic Moderators:**
- Gender (large effects on empathy and mental health)
- Academic Year (significant improvement over time)
- Psychotherapy use (marker of severity)

### 9.3 Potential ML Approaches

**Classification Tasks:**
- Random Forest / Gradient Boosting (handles non-linear relationships)
- Logistic Regression (interpretable baseline)
- Neural Networks (for complex interactions)

**Regression Tasks:**
- Multiple Linear Regression (interpretable)
- XGBoost (high performance)
- Deep Learning (LSTM for temporal patterns if year is key)

**Clustering:**
- K-Means or Hierarchical clustering for student profiles
- Identify subgroups with distinct mental health patterns

### 9.4 Class Imbalance Considerations
- Depression (52/48 split) - **relatively balanced**
- Anxiety (60/40 split) - **slight imbalance**, consider SMOTE
- High Burnout (4/96 split) - **severe imbalance**, use weighted classes

### 9.5 Cross-Validation Strategy
```python
from sklearn.model_selection import StratifiedKFold

# Stratify by target and academic year
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

---

## 10. KEY RECOMMENDATIONS

### 10.1 For Mental Health Interventions
1. **Prioritize Early Years:** Highest depression/burnout in Year 1
2. **Gender-Specific Support:** Females show significantly worse outcomes
3. **Address Affective Empathy Burden:** May lead to compassion fatigue
4. **Increase Access to Psychotherapy:** Only 22.5% currently using services

### 10.2 For Further Analysis
1. **Longitudinal Analysis:** Track same students over years
2. **Mediation Analysis:** Does empathy mediate study hours → mental health?
3. **Qualitative Follow-up:** Interview high-risk students
4. **Intervention Studies:** Test stress-reduction programs

### 10.3 For ML Modeling
1. **Feature Engineering:** Create composite scores, interaction terms
2. **Handle Imbalance:** Use SMOTE, class weights, or stratified sampling
3. **Interpretability:** Use SHAP values to explain predictions
4. **Validation:** Use stratified K-fold, test on holdout set
5. **Fairness:** Check for gender/year biases in predictions

---

## 11. CONCLUSIONS

This comprehensive EDA reveals a **severe mental health crisis** among medical students, with:

- Over **half experiencing depression risk**
- **60% with high anxiety**
- **Nearly half accumulating 3+ risk factors**
- Significant **gender disparities** (females worse)
- **Improvement with academic progression** (adaptation or survivor bias)
- **Paradoxical empathy findings** (higher affective empathy → worse mental health)

### Dataset Strengths:
Complete data (no missing values)  
Large sample size (N=886)  
Validated psychometric instruments  
Rich variable set (empathy, mental health, demographics)  

### Next Steps for ML/DL:
1. Feature engineering (composites, interactions)
2. Handle class imbalance (SMOTE, weights)
3. Model selection (tree-based, neural networks)
4. Interpretability analysis (SHAP, feature importance)
5. Fairness auditing (gender, year biases)

---

**Report Generated:** February 13, 2026  
**Analysis Tools:** Python (pandas, numpy, scipy, seaborn, matplotlib)  
**Visualization Outputs:** 9 comprehensive figures  
**Statistical Outputs:** 4 CSV reports
