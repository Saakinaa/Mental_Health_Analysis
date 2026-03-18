import pandas as pd
import numpy as np
from preprocess_improved import MentalHealthPreprocessor
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import shapiro, kurtosis, skew

# 1. Preprocess

preprocessor = MentalHealthPreprocessor()
preprocessor.run_full_pipeline(
    data_path="/Users/user/Downloads/Stud_Mental_Health/Data/Data 2022 MedTeach.csv",
    output_path="/Users/user/Downloads/Stud_Mental_Health/Data/MentalHealthData_Cleaned.csv"
)

data = pd.read_csv("/Users/user/Downloads/Stud_Mental_Health/Data/MentalHealthData_Cleaned.csv")
data.head()
data.info()