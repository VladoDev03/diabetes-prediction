# Conclusion

## Methodology Deviations from the Baseline Pipeline

For the `BRFSS` dataset, the original public methodology (Teboul et al.) was reproduced with two deliberate, validated deviations: `_BMI5` was kept at its original decimal precision rather than rounded to the nearest integer, and `_AGE80` (single-year age) was used instead of `_AGEG5YR` (5-year age bins), with rows lacking a reported age (`_AGEG5YR == 14`) still excluded to avoid using CDC-imputed rather than reported values. These two changes were empirically validated: the rate of full duplicate rows dropped from 9.42% to 0.47%, and conflicting duplicates (identical features, different diabetes label) dropped from 10.16% to 0.49% - a roughly 20 times reduction confirming that coarse feature resolution in the original methodology was a primary driver of label ambiguity.

The target variable itself was also reconstructed differently from the official methodology. Rather than merging prediabetes with the non-diabetic class (as the public `Diabetes_binary` dataset does), prediabetes was merged with the diabetic class, based on three independent lines of evidence: a feature-mean comparison (15 of 18 features placed prediabetes closer to diabetes than to no-diabetes), Mann-Whitney effect sizes (consistently 2-4x larger against no-diabetes than against diabetes), and centroid distance in standardized feature space (0.916 vs. 0.407). This is a case where the data contradicted the established public methodology, and the deviation is explicitly justified rather than assumed.

Near-constant features identified during EDA (`has_healthcare_coverage`, `chol_checked_recently`, `had_stroke`) were not removed automatically based on prevalence alone. A crosstab against the target showed `had_stroke` and `chol_checked_recently` carry meaningful predictive signal despite low or near-universal prevalence, and only `has_healthcare_coverage` was removed. `chol_checked_recently` was flagged as likely reflecting a detection/healthcare-engagement effect rather than a genuine risk factor, and is not interpreted causally despite its predictive value.

## Data Quality Findings

Both datasets showed evidence of data quality limitations that shaped the analysis. In the `iammustafatz` dataset, `bmi` showed an artificial concentration around a single value (27.32, ~22.5% of all rows) alongside extreme outliers (max = 97.65), and `HbA1c_level`/`blood_glucose_level` were found to take only 18 discrete values each, indicating quantized or synthetically generated data rather than raw clinical measurements.

Most significantly, `HbA1c_level` and `blood_glucose_level` were identified as the clinical diagnostic criteria for diabetes itself (HbA1c $\geq$ 6.5%, fasting glucose $\geq$ 126 mg/dL), not independent risk factors. Their inclusion means models trained on the `iammustafatz` dataset partly reproduce a known clinical threshold rather than discovering genuine lifestyle-based risk patterns - an important distinction from the `BRFSS` dataset, where no comparably direct diagnostic feature exists.

## Modeling Approach

**Logistic Regression** (interpretable baseline) and **Random Forest** (captures non-linear threshold effects) were trained on both datasets. For the larger `BRFSS` dataset, **Stacking** and **Voting** ensembles combining **Logistic Regression**, **Random Forest**, and **HistGradientBoosting** were additionally tested, given the larger sample size better supports the added model complexity. **SVM** was considered but rejected due to poor scalability at this sample size. All models used `class_weight="balanced"` to address class imbalance (`BRFSS`: ~14% positive; `iammustafatz`: ~8.8% positive), rather than oversampling/undersampling, keeping the training data distribution unmodified. Stratified 80/20 train/test splits and `StratifiedKFold` cross-validation were used throughout to ensure stable, representative evaluation given the class imbalance.

## Results Summary

| Dataset | Best Model | ROC-AUC | F1 | PR-AUC |
|---|---|---|---|---|
| `BRFSS` | Stacking Ensemble | 0.8252 | 0.4734 | 0.4565 |
| `iammustafatz` | Random Forest | 0.9746 | 0.6129 | 0.8757 |

The substantial performance gap between the two datasets is expected and directly connects to the data quality finding above: `HbA1c_level` and `blood_glucose_level` give the `iammustafatz` models a much stronger, more direct signal than the purely lifestyle/demographic `BRFSS` features. This gap should be read as a reflection of feature set composition, not as evidence that one dataset or model is inherently "better."

For `BRFSS`, all four models (**Logistic Regression**, **Random Forest**, **Stacking**, **Voting**) performed similarly (ROC-AUC 0.818–0.825), suggesting most of the available predictive signal is captured even by the simplest model. The **Stacking** ensemble's marginal edge over **Voting** (0.0009 ROC-AUC) suggests its meta-learner adds only limited value beyond a simple averaged combination. `general_health`, `high_blood_pressure`, `bmi`, `high_cholesterol`, and `age` consistently emerged as the strongest predictors across both **Logistic Regression** and **Random Forest**, reinforcing confidence that these reflect genuine clinical signal.

Overfitting checks (train vs. test ROC-AUC gap) were small across all models in both datasets (`BRFSS`: 0.010–0.016; `iammustafatz`: comparably small), indicating that hyperparameter tuning successfully controlled model complexity without memorizing the training data.

## Limitations

- **Correlational, not causal**: all reported relationships (e.g. `chol_checked_recently`, income, education) describe statistical association within this data, not causal mechanisms.
- **Selection bias in `BRFSS`**: the original data preparation removes respondents who declined to answer any of ~20 survey questions, systematically excluding people less willing to disclose sensitive information (income, weight, health status).
- **Missing established risk factors**: `_RACE`, an established diabetes risk factor, is absent from the original `BRFSS` feature selection and was not added in this analysis; kidney disease and depression history were identified as other plausible omissions.
- **Production generalization**: neither **RobustScaler** nor **StandardScaler** can guard against future input values outside the observed training range; this would require explicit input validation in a deployed setting, out of scope here.
- **Heterogeneous merged target class**: the merged "at-risk" class in `BRFSS` (prediabetes + diabetes) is not a clinically uniform group, though the evidence supports this grouping over the alternative.

## Future Work

Possible extensions include: adding `_RACE` and other omitted risk factors to the `BRFSS` feature set; training an `iammustafatz` model restricted to lifestyle/demographic features only (excluding HbA1c/glucose) to obtain a more realistic early-screening estimate, isolated from the diagnostic circularity discussed above;