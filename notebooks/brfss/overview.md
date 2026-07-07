# Dataset Overview - Diabetes Health Indicators Dataset (BRFSS Survey)

This dataset is derived from the CDC's 2015 Behavioral Risk Factor Surveillance System (BRFSS) survey. Unlike the smaller diabetes prediction dataset, it contains no lab measurements - every feature is either self-reported or derived from a survey question, so domain knowledge is needed to interpret several of them correctly.

**general_health**
Self-reported overall health on a 5-point ordinal scale (1 = Excellent to 5 = Poor). It is a subjective measure, but consistently one of the strongest predictors of diabetes status across BRFSS-based studies, likely because it implicitly captures a wide range of unmeasured health conditions.

**high_blood_pressure** and **high_cholesterol**
Binary indicators (0 = No, 1 = Yes) for a prior diagnosis of hypertension or high cholesterol, respectively. Both are established comorbidities of type 2 diabetes, frequently co-occurring due to shared risk factors such as obesity and metabolic syndrome.

**chol_checked_recently**
Binary indicator of whether the respondent had their cholesterol checked within the last 5 years. This is not a risk factor in the clinical sense - it is a healthcare-engagement proxy. People who are never screened are also less likely to be screened and diagnosed for diabetes, so this feature can pick up a detection-bias signal rather than a genuine physiological one. This should be flagged explicitly, since a model may lean on it for reasons unrelated to real diabetes risk.

**bmi**
Body Mass Index, calculated as weight (kg) / height (m)$^2$. Same World Health Organization classification as in the other dataset:
- Underweight: < 18.5
- Normal weight: 18.5 – 24.9
- Overweight: 25.0 – 29.9
- Obese: 30.0+

**physical_health_bad_days** and **mental_health_bad_days**
Self-reported number of days (0–30) in the past month during which the respondent's physical or mental health was "not good." These are continuous proxies for general health burden rather than diabetes-specific indicators.

**difficulty_walking**
Binary indicator (0 = No, 1 = Yes) for serious difficulty walking or climbing stairs - a proxy for mobility limitations, which can be both a cause (reduced physical activity) and a consequence (neuropathy, obesity) of diabetes.

**had_stroke** and **heart_disease_or_attack**
Binary indicators for a prior diagnosis of stroke or coronary heart disease/myocardial infarction. Like hypertension and high cholesterol, these are established diabetes comorbidities rather than direct predictors.

**physically_active**, **consumes_fruit_daily**, **consumes_veggies_daily**, **heavy_alcohol_consumption**, **smoked_at_least_100_cigarettes**
Binary lifestyle indicators self-reported by the respondent (e.g. "ever smoked at least 100 cigarettes" is the standard BRFSS proxy for "ever a smoker"). These carry real signal but are individually weak, indirect predictors compared to the comorbidity and general-health features above.

**skipped_doctor_due_to_cost**
Binary indicator of whether cost prevented the respondent from seeing a doctor when needed in the past year - a healthcare-access proxy that, similarly to `chol_checked_recently`, can reflect socioeconomic and detection-bias effects rather than physiological risk.

**income_level** and **education_level**
Ordinal categorical variables (grouped income brackets and education levels). Both are socioeconomic proxies, correlated with diet, healthcare access, and diagnosis rates rather than direct physiological risk factors.

**age** and **sex**
`age` is reported in BRFSS as a grouped ordinal category (13 age brackets) rather than an exact value, which should be kept in mind when interpreting model coefficients or feature importances. `sex` is binary (0/1).

**diabetes** (target variable)
Binary label (0 = No diabetes, 1 = Prediabetes, 2 = Diabetes), with a substantial class imbalance (~8.8% positive). Because none of the features here are direct lab measurements, no single feature is expected to be near-deterministic the way `HbA1c_level` or `blood_glucose_level` are in the other dataset - predictive performance instead comes from combining many weak, indirect signals, which is the main reason overall metrics (ROC-AUC, PR-AUC) are noticeably lower here than on the lab-based dataset.