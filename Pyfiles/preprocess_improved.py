# ============================================================================
# PREPROCESSING FILE ASSESSMENT
# ============================================================================

"""
OVERALL ASSESSMENT: Your preprocessing file is GOOD with room for improvement!

STRENGTHS:
1. Correct rescaling approach with clear documentation
2. Proper clinical cutoff preservation
3. Good outlier handling decisions
4. Clear variable renaming
5. Comprehensive exploratory analysis
6. Good use of visualizations

AREAS FOR IMPROVEMENT:
1. Hard-coded file paths (not portable)
2. Mix of exploration and preprocessing (should be separated)
3. Some unused/commented code
4. Could benefit from functions/modularization
5. No explicit train/test split preparation
6. Missing some feature engineering for ML

RECOMMENDED STRUCTURE:
- preprocess.py → Clean preprocessing ONLY
- eda_analysis.ipynb → Exploratory analysis
- ml_analysis.ipynb → Traditional ML models
- dl_analysis.ipynb → Deep learning models
"""

# ============================================================================
# IMPROVED PREPROCESSING FILE
# ============================================================================

import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class MentalHealthPreprocessor:
    """
    Preprocessing pipeline for medical student mental health data.
    Handles rescaling, categorization, outlier treatment, and feature engineering.
    """
    
    def __init__(self, data_path=None):
        """
        Initialize preprocessor.
        
        Args:
            data_path (str): Path to raw data file
        """
        self.data_path = data_path
        self.data = None
        self.processed_data = None
        
        # Clinical cutoffs
        self.clinical_cutoffs = {
            'cesd_depression': 16,
            'cesd_severe': 22,
            'stai_high': 40,
            'stai_very_high': 50,
            'mbi_ex_high': 27,
            'mbi_cy_high': 13,
            'mbi_ea_low': 32
        }
        
        # Rescaling parameters
        self.rescale_params = {
            'jspe': {'min': 20, 'max': 140},
            'qcae_cog': {'min': 19, 'max': 76},  # 19 items × 4 points
            'qcae_aff': {'min': 12, 'max': 48},  # 12 items × 4 points
            'amsp': {'min': 7, 'max': 35},       # 7 items × 5 points
            'erec_mean': {'min': 0, 'max': 1}
        }
    
    def load_data(self, data_path=None):
        """Load data from CSV file."""
        if data_path:
            self.data_path = data_path
        
        self.data = pd.read_csv(self.data_path)
        print(f"✓ Loaded data: {self.data.shape}")
        return self
    
    def handle_outliers(self):
        """Handle outliers according to validated rules."""
        print("\nHandling outliers...")
        
        # Languages > 7 → NaN (implausible)
        outlier_mask = self.data['glang'] > 7
        n_outliers = outlier_mask.sum()
        self.data.loc[outlier_mask, 'glang'] = np.nan
        print(f"  - Set {n_outliers} implausible language values to NaN")
        
        # Keep age > 30 (validated with year of study)
        print(f"  - Retained {(self.data['age'] > 30).sum()} older students (valid cases)")
        
        # Keep extreme clinical scores (genuine severity)
        print(f"  - Retained extreme mental health scores (clinical significance)")
        
        return self
    
    def rescale_scores(self):
        """Rescale empathy and related scores to 0-100 scale."""
        print("\nRescaling scores to 0-100...")
        
        # Rescaling function
        def rescale(x, min_val, max_val):
            return (x - min_val) / (max_val - min_val) * 100
        
        # Apply rescaling
        for var, params in self.rescale_params.items():
            if var in self.data.columns:
                scaled_name = f"{var}_scaled"
                self.data[scaled_name] = self.data[var].apply(
                    lambda x: rescale(x, params['min'], params['max'])
                )
                print(f"  ✓ {var} → {scaled_name}")
        
        return self
    
    def categorize_scores(self):
        """Create categorical versions of scores (Low/Medium/High)."""
        print("\nCategorizing scores...")
        
        def categorize(x):
            if x <= 33:
                return "Low"
            elif x <= 66:
                return "Medium"
            else:
                return "High"
        
        # Categorize rescaled scores
        scaled_vars = [col for col in self.data.columns if '_scaled' in col]
        for var in scaled_vars:
            cat_name = f"{var}_cat"
            self.data[cat_name] = self.data[var].apply(categorize)
        
        # Categorize clinical scores using established cutoffs
        if 'cesd' in self.data.columns:
            self.data['cesd_cat'] = pd.cut(
                self.data['cesd'],
                bins=[-np.inf, 15, 21, np.inf],
                labels=['Low', 'Medium', 'High']
            )
        
        if 'stai_t' in self.data.columns:
            self.data['stai_t_cat'] = pd.cut(
                self.data['stai_t'],
                bins=[-np.inf, 35, 45, np.inf],
                labels=['Low', 'Medium', 'High']
            )
        
        if 'mbi_ex' in self.data.columns:
            self.data['mbi_ex_cat'] = pd.cut(
                self.data['mbi_ex'],
                bins=[-np.inf, 16, 26, np.inf],
                labels=['Low', 'Medium', 'High']
            )
        
        print(f"  ✓ Created {len([c for c in self.data.columns if '_cat' in c])} categorical variables")
        
        return self
    
    def rename_columns(self):
        """Rename columns for better interpretability."""
        print("\nRenaming columns...")
        
        rename_map = {
            # Demographics
            'age': 'Age',
            'year': 'Academic_Year',
            'sex': 'Gender',
            'glang': 'Languages_Spoken',
            'part': 'Has_Partner',
            'job': 'Has_Job',
            'stud_h': 'Study_Hours_Per_Week',
            'health': 'Health_Satisfaction',
            'psyt': 'Psychotherapy_Last_12_Months',
            
            # Empathy
            'jspe': 'Physician_Empathy_Raw',
            'qcae_cog': 'Cognitive_Empathy_Raw',
            'qcae_aff': 'Affective_Empathy_Raw',
            
            # Other measures
            'amsp': 'Attitudes_Mental_Health_Raw',
            'erec_mean': 'Emotion_Recognition_Raw',
            
            # Mental health
            'cesd': 'Depression_Score',
            'stai_t': 'Anxiety_Score',
            'mbi_ex': 'Burnout_Exhaustion',
            'mbi_cy': 'Burnout_Cynicism',
            'mbi_ea': 'Academic_Efficacy'
        }
        
        self.data.rename(columns=rename_map, inplace=True)
        print(f"  ✓ Renamed {len(rename_map)} columns")
        
        return self
    
    def create_binary_targets(self):
        """Create binary target variables for ML classification."""
        print("\nCreating binary targets...")
        
        # Depression risk (main target)
        self.data['Depression_Risk'] = (
            self.data['Depression_Score'] >= self.clinical_cutoffs['cesd_depression']
        ).astype(int)
        
        # Anxiety risk
        self.data['Anxiety_Risk'] = (
            self.data['Anxiety_Score'] >= self.clinical_cutoffs['stai_high']
        ).astype(int)
        
        # Burnout risk
        self.data['Burnout_Risk'] = (
            self.data['Burnout_Exhaustion'] >= self.clinical_cutoffs['mbi_ex_high']
        ).astype(int)
        
        # Low efficacy
        self.data['Low_Efficacy'] = (
            self.data['Academic_Efficacy'] < self.clinical_cutoffs['mbi_ea_low']
        ).astype(int)
        
        # Composite mental health risk
        self.data['Mental_Health_Risk_Score'] = (
            self.data['Depression_Risk'] +
            self.data['Anxiety_Risk'] +
            self.data['Burnout_Risk'] +
            self.data['Low_Efficacy']
        )
        
        print(f"  ✓ Created 5 target variables")
        print(f"    - Depression_Risk: {self.data['Depression_Risk'].sum()} cases ({self.data['Depression_Risk'].mean()*100:.1f}%)")
        print(f"    - Anxiety_Risk: {self.data['Anxiety_Risk'].sum()} cases ({self.data['Anxiety_Risk'].mean()*100:.1f}%)")
        print(f"    - Mental_Health_Risk_Score: Mean = {self.data['Mental_Health_Risk_Score'].mean():.2f}")
        
        return self
    
    def feature_engineering(self):
        """Create additional features for ML models."""
        print("\nFeature engineering...")
        
        # Composite empathy score
        empathy_cols = [c for c in self.data.columns if 'Empathy' in c and 'scaled' in c]
        if empathy_cols:
            self.data['Total_Empathy'] = self.data[empathy_cols].mean(axis=1)
            print(f"  ✓ Created Total_Empathy")
        
        # Mental health burden (continuous)
        if all(col in self.data.columns for col in ['Depression_Score', 'Anxiety_Score', 'Burnout_Exhaustion']):
            self.data['Mental_Health_Burden'] = (
                self.data['Depression_Score'] / 60 +  # Normalize to 0-1 range
                self.data['Anxiety_Score'] / 80 +
                self.data['Burnout_Exhaustion'] / 30
            ) / 3
            print(f"  ✓ Created Mental_Health_Burden")
        
        # Interaction terms (gender × empathy)
        if 'Gender' in self.data.columns and 'Affective_Empathy_Raw' in self.data.columns:
            self.data['Gender_x_Affective_Empathy'] = (
                self.data['Gender'] * self.data['Affective_Empathy_Raw']
            )
            print(f"  ✓ Created Gender_x_Affective_Empathy")
        
        # Year × Mental Health (progression effect)
        if 'Academic_Year' in self.data.columns and 'Depression_Score' in self.data.columns:
            self.data['Year_x_Depression'] = (
                self.data['Academic_Year'] * self.data['Depression_Score']
            )
            print(f"  ✓ Created Year_x_Depression")
        
        # Study load indicator
        if 'Study_Hours_Per_Week' in self.data.columns:
            self.data['High_Study_Load'] = (
                self.data['Study_Hours_Per_Week'] > 
                self.data['Study_Hours_Per_Week'].quantile(0.75)
            ).astype(int)
            print(f"  ✓ Created High_Study_Load")
        
        return self
    
    def prepare_for_ml(self):
        """Prepare final dataset for ML with proper data types."""
        print("\nPreparing for ML...")
        
        # Ensure binary variables are int
        binary_cols = [c for c in self.data.columns if 
                      'Risk' in c or 'Has_' in c or 'High_' in c or 'Low_' in c]
        for col in binary_cols:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(int)
        
        # Ensure categorical are strings
        cat_cols = [c for c in self.data.columns if '_cat' in c]
        for col in cat_cols:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(str)
        
        print(f"  ✓ Data types prepared for ML")
        
        return self
    
    def get_feature_groups(self):
        """Return organized groups of features for modeling."""
        feature_groups = {
            'demographic': [
                'Age', 'Academic_Year', 'Gender', 'Languages_Spoken',
                'Has_Partner', 'Has_Job', 'Study_Hours_Per_Week', 
                'Health_Satisfaction'
            ],
            'empathy_raw': [
                'Physician_Empathy_Raw', 'Cognitive_Empathy_Raw', 
                'Affective_Empathy_Raw'
            ],
            'empathy_scaled': [
                c for c in self.data.columns if 'Empathy' in c and 'scaled' in c
            ],
            'mental_health': [
                'Depression_Score', 'Anxiety_Score', 'Burnout_Exhaustion',
                'Burnout_Cynicism', 'Academic_Efficacy'
            ],
            'targets': [
                'Depression_Risk', 'Anxiety_Risk', 'Burnout_Risk',
                'Low_Efficacy', 'Mental_Health_Risk_Score'
            ],
            'engineered': [
                c for c in self.data.columns if 
                'Total_' in c or '_x_' in c or 'Burden' in c or 'High_' in c
            ]
        }
        
        # Filter only existing columns
        feature_groups = {
            k: [c for c in v if c in self.data.columns]
            for k, v in feature_groups.items()
        }
        
        return feature_groups
    
    def save_processed_data(self, output_path):
        """Save processed data to CSV."""
        self.data.to_csv(output_path, index=False)
        print(f"\n✓ Saved processed data to: {output_path}")
        return self
    
    def run_full_pipeline(self, data_path=None, output_path=None):
        """Run complete preprocessing pipeline."""
        print("="*80)
        print("RUNNING FULL PREPROCESSING PIPELINE")
        print("="*80)
        
        # Execute pipeline
        self.load_data(data_path)
        self.handle_outliers()
        self.rescale_scores()
        self.categorize_scores()
        self.rename_columns()
        self.create_binary_targets()
        self.feature_engineering()
        self.prepare_for_ml()
        
        # Summary
        print("\n" + "="*80)
        print("PREPROCESSING COMPLETE")
        print("="*80)
        print(f"Final shape: {self.data.shape}")
        print(f"Columns: {len(self.data.columns)}")
        print(f"Missing values: {self.data.isnull().sum().sum()}")
        
        # Feature groups
        groups = self.get_feature_groups()
        print("\nFeature Groups:")
        for group_name, features in groups.items():
            print(f"  {group_name}: {len(features)} features")
        
        # Save if path provided
        if output_path:
            self.save_processed_data(output_path)
        
        self.processed_data = self.data.copy()
        return self
    
    