# Dataset Overview - Diabetes prediction dataset (Clinical)

Some attributes like age and gender are self-explanatory. However, attributes like HbA1c_level, blood_glucose_level, and even bmi require domain knowledge, which is why we go through some explanations below.

**BMI (Body Mass Index)**

bmi: Body Mass Index. A generally useful metric, calculated as weight (kg) / height (m)$^2$. However, it does not account for age, sex, muscle mass, or body fat percentage.

Standard World Health Organization classification:
- Underweight: < 18.5
- Normal weight: 18.5 – 24.9
- Overweight: 25.0 – 29.9
- Obese: 30.0+

**HbA1c_level (Glycated Hemoglobin)**

Reflects the average blood sugar level over the past 2–3 months, measured as a percentage. Unlike a single glucose reading, it is not affected by short-term fluctuations (e.g. what the person ate that morning), which makes it a more stable diagnostic indicator.

Clinical thresholds:
- Normal: < 5.7%
- Prediabetes: 5.7% – 6.4%
- Diabetes: $\geq$ 6.5%

**blood_glucose_level**

A single snapshot measurement of sugar concentration in the blood at the time of testing, expressed in mg/dL (milligrams of glucose per deciliter of blood) - unlike HbA1c which reflects a longer-term average. Depending on whether the reading was fasting or random, the diagnostic thresholds differ:

Fasting glucose:
- Normal: < 100 mg/dL
- Prediabetes: 100 – 125 mg/dL
- Diabetes: $\geq$ 126 mg/dL

Random (non-fasting) glucose:
- Diabetes: $ \geq $ 200 mg/dL

> Note: this dataset does not specify whether readings are fasting or random, which is a limitation worth mentioning in the analysis.

**smoking_history**

Categorical variable with 6 possible values: `never`, `former`, `current`, 
`not current`, `ever`, and `No Info`.

The `No Info` category is not a smoking status - it indicates missing data (the respondent's smoking history was not recorded). Treating it as its own category, rather than dropping it, avoids losing rows, but it should not be interpreted as "never smoked."

The overlap between `former`, `not current`, and `ever` is somewhat ambiguous in the source data and worth noting as a limitation - these may need to be consolidated during preprocessing.

**hypertension** and **heart_disease**

Both are binary indicators (0 = No, 1 = Yes) representing whether the respondent has been previously diagnosed with high blood pressure or heart disease, respectively. These are included as established comorbidity risk factors for type 2 diabetes - hypertension and cardiovascular disease frequently co-occur with diabetes due to shared risk factors such as obesity and metabolic syndrome.

**diabetes** (target variable)

Binary label (0 = No diabetes, 1 = Diabetes). Note the overlap with the clinical thresholds discussed above - since HbA1c $ \geq $ 6.5% and fasting glucose $ \geq $ 126 mg/dL are themselves diagnostic criteria for diabetes, these two features are likely to be extremely strong (possibly near-deterministic) predictors of the target. This should be flagged explicitly, as models may achieve very high accuracy simply by learning the clinical cutoff rather than genuine risk patterns from lifestyle/demographic features.