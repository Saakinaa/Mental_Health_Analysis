# Documentation: Score Rescaling and Categorization

The purpose of this step is to harmonize the different psychometric scales in the dataset to facilitate:
- Comparison across different instruments
- Data visualization
- Use in machine learning models

This approach preserves the original meaning of the scores while standardizing them onto a common scale.

## 1. Rescaled Scores

### 1.1 JSPE (Jefferson Scale of Physician Empathy)

- Theoretical range: 20–140
- Rescaling: linear transformation to 0–100:
JSPE_scaled = (JSPE − 20) / (140 − 20) × 100
- Interpretation: higher scores indicate higher self-reported empathy.
- Use: comparisons, statistical analyses, and preparation for predictive modeling.

### 1.2 QCAE_COG and QCAE_AFF (Questionnaire of Cognitive and Affective Empathy)

- Theoretical range: 1–4 per item
- Total score calculation:
	- Cognitive: min = number of items × 1, max = number of items × 4
	- Affective: min = number of items × 1, max = number of items × 4
- Rescaling: linear transformation to 0–100:
QCAE_scaled = (raw_score − min) / (max − min) × 100
- Interpretation: 0 = low empathy, 100 = high empathy
- Use: inter-score comparison, exploratory analyses, visualizations.

### 1.3 AMSP (Academic Motivation / Self-Presentation)

- Theoretical range: 0 to maximum value depending on questionnaire version
- Rescaling: linear transformation to 0–100:
AMSP_scaled = (raw_score − 0) / (max) × 100
- Interpretation: 0 = low motivation/ability, 100 = high motivation/ability
- Use: statistical analyses, predictive modeling.

### 1.4 EREC_MEAN (GERT – Emotion Recognition)

- Theoretical range: 0–1 (proportion of correct responses)
- Rescaling: multiply by 100 to obtain a percentage:
EREC_scaled=EREC_mean×100
- Interpretation: 0 = minimal performance, 100 = maximal performance
- Use: visualization, comparison with other scores.

## 2. Score Categorization

Each rescaled score is categorized into three levels to facilitate interpretation:

Level	Interval (%)
Low	    0–33
Medium	34–66
High	67–100

- This categorization allows segmentation of participants based on performance or psychometric characteristics.
- Thresholds are arbitrary but consistent for comparative analysis and visualization.

## 3. Key Considerations

- Clinical scores (CES-D, STAI-T, MBI) are not rescaled to preserve the validity of official clinical cut-offs.
- The rescaling is linear and does not alter the proportional relationship among raw scores.
- The rescaling method should be documented in any publication or report to ensure traceability and reproducibility.


#### QCAE, ASMP, EREC 

| Terme             | Signification                            |
| ----------------- | ---------------------------------------- |
| Item              | Une question du questionnaire            |
| Nombre d’items    | Nombre total de questions                |
| Échelle de Likert | Plage de réponses numériques (1–4, 1–7…) |
| Score total       | Somme des réponses aux items             |
| Min théorique     | items × valeur minimale                  |
| Max théorique     | items × valeur maximale                  |
