# Diabetes Prediction

A machine learning project comparing diabetes prediction across two independent datasets: the CDC BRFSS 2015 behavioral health survey and a clinical-style dataset with direct biomarker measurements.

## Project Structure

```
diabetes-analysis/
|-- data/
|   |-- raw/               # original, unmodified source datasets
|   +-- processed/         # cleaned and preprocessed datasets
|-- notebooks/
|   |-- diabetes/          # clinical dataset: EDA, preprocessing, training
|   +-- brfss/             # BRFSS dataset: EDA, preprocessing, training
|-- src/
|   |-- data_prep.py       # data cleaning and statistical comparison utilities
|   |-- visualization.py   # plotting functions used throughout the notebooks
|   +-- evaluation.py      # model evaluation and overfitting-check utilities
|-- models/                # trained model files (.pkl)
|-- final_project.ipynb    # single consolidated notebook containing the full pipeline
|-- notebooks_merge.py     # one-off script used to build final_project.ipynb from the individual notebooks (not needed to run the analysis)
|-- requirements.txt
|-- .gitignore
|-- LICENSE
+-- README.md
```

## Why the project is organized this way

**notebooks/diabetes/ and notebooks/brfss/** hold the project in its natural development form - separate EDA, preprocessing, and training notebooks per dataset. This mirrors how the analysis was actually built and is easiest to navigate stage by stage.

**final_project.ipynb** consolidates every notebook above into a single file, in execution order, with all src/ helper functions available via standard imports. It exists alongside the modular notebooks - not instead of them - specifically for reproducibility: a single file that can be run top to bottom (Kernel -> Restart & Run All) to regenerate every result in the project from raw data to final model evaluation, without needing to track execution order across multiple separate notebooks.

**data/raw/** contains the original source files (zipped) rather than just the cleaned outputs. This is included for reproducibility - anyone cloning this repository can rerun the entire pipeline from the original raw data and verify that the cleaning, EDA, and preprocessing steps produce the same results, without needing to separately track down and re-download the original Kaggle/CDC sources.

**models/** contains the trained model files (.pkl), also for reproducibility. Training the full set of models (including hyperparameter search and the BRFSS ensembles) takes non-trivial time; having the trained artifacts available means the final evaluation results can be verified or reused directly, without requiring a full retraining run.

## Datasets

- Diabetes Health Indicators Dataset (BRFSS 2015) - derived from the CDC's Behavioral Risk Factor Surveillance System survey. Lifestyle, demographic, and comorbidity indicators only, no lab measurements.
- Diabetes Prediction Dataset - a clinical-style dataset including HbA1c_level and blood_glucose_level, both part of the official diagnostic criteria for diabetes.

Both are cited in full under References in the project notebooks, including known limitations identified during EDA (e.g. deviations from the original public preparation methodology, all explicitly justified in the relevant notebooks).

## How to Run

1. Clone the repository.
2. Install dependencies:
   pip install -r requirements.txt
3. Run either:
   - the individual notebooks in notebooks/diabetes/ and notebooks/brfss/ in numerical order, or
   - final_project.ipynb directly, which reproduces the entire pipeline end to end.

Raw data is already included under data/raw/; no external download is required.

## Key Findings

- Prediabetes is statistically closer to diagnosed diabetes than to the non-diabetic population across most features (effect size, centroid distance), motivating a different target-merging strategy than the official public methodology.
- `HbA1c_level` and `blood_glucose_level` function as near-diagnostic criteria, explaining the large performance gap between the two datasets (ROC-AUC 0.97 vs. 0.82)
- Across both datasets, `general_health`, `blood_pressure`, `bmi`, and `age` consistently emerge as the strongest predictors.

## Summary of Results

| Dataset | Best Model | ROC-AUC | F1 | PR-AUC |
|---|---|---|---|---|
| BRFSS | Stacking Ensemble | 0.8252 | 0.4734 | 0.4565 |
| Diabetes Prediction Dataset | Random Forest | 0.9746 | 0.6129 | 0.8757 |

The performance gap between the two datasets reflects the presence of direct diagnostic biomarkers in the second dataset (HbA1c_level, blood_glucose_level), not a difference in model quality - this is discussed in detail in the Conclusion section of the notebooks.