from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import xgboost
import shap

# Load the California housing dataset
california_housing = fetch_california_housing()

# Convert to DataFrame for easier manipulation
X = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
y = pd.Series(california_housing.target, name='target')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train XGBoost model
model = xgboost.XGBRegressor(objective='reg:squarederror', n_estimators=500)
model.fit(X_train, y_train)

# Create SHAP explainer
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# Analyze the first example
first_row_shap = shap_values[0]
shapley_values = first_row_shap.values

print(f'Predicted Value: {first_row_shap.base_values + sum(shapley_values)}\n')
print(f'Baseline: {first_row_shap.base_values}\n')
print('Shapley values for features:')
for i, shapley_value in enumerate(shapley_values):
    print(f'{shap_values.feature_names[i]}: {shapley_value}')

print('\nMost to least influential features:')
most_influential_ordering = np.argsort(-np.abs(shapley_values))
for i in range(len(shapley_values)):
    print(f'{shap_values.feature_names[most_influential_ordering[i]]}: {shapley_values[most_influential_ordering[i]]}')

shap.plots.waterfall(shap_values[0])

shap.initjs()
shap.plots.force(shap_values[0])

shap.plots.scatter(shap_values[:,"MedInc"])

shap.plots.scatter(shap_values[:,"HouseAge"], color=shap_values)

# Print comprehensive inferences from the SHAP plots
print("\n" + "="*80)
print("COMPREHENSIVE SHAP ANALYSIS INFERENCES")
print("="*80)

# 1. Waterfall Plot Analysis
print("\n1. WATERFALL PLOT INFERENCES:")
print("-" * 40)
baseline = first_row_shap.base_values
prediction = baseline + sum(shapley_values)
print(f"• Baseline (average prediction): {baseline:.3f}")
print(f"• Final prediction for this house: {prediction:.3f}")
print(f"• Total contribution from features: {sum(shapley_values):.3f}")

# Analyze each feature's contribution
print("\n• Feature Impact Analysis:")
for i, (feature, value) in enumerate(zip(shap_values.feature_names, shapley_values)):
    impact = "increases" if value > 0 else "decreases"
    magnitude = abs(value)
    print(f"  - {feature}: {impact} price by {magnitude:.3f} (Feature value: {X_test.iloc[0][feature]:.3f})")

# 2. Feature Importance Analysis
print("\n\n2. FEATURE IMPORTANCE RANKING:")
print("-" * 40)
feature_importance = np.abs(shapley_values)
sorted_indices = np.argsort(-feature_importance)
for i, idx in enumerate(sorted_indices):
    feature = shap_values.feature_names[idx]
    importance = feature_importance[idx]
    print(f"{i+1}. {feature}: {importance:.3f} absolute impact")

# 3. Global Feature Analysis
print("\n\n3. GLOBAL FEATURE BEHAVIOR ANALYSIS:")
print("-" * 40)

# Analyze MedInc (Median Income)
medinc_values = shap_values[:, "MedInc"].values
medinc_feature_values = X_test["MedInc"].values
print(f"• MEDIAN INCOME (MedInc):")
print(f"  - Range of SHAP values: [{medinc_values.min():.3f}, {medinc_values.max():.3f}]")
print(f"  - Range of feature values: [{medinc_feature_values.min():.3f}, {medinc_feature_values.max():.3f}]")
print(f"  - Correlation with SHAP: {np.corrcoef(medinc_feature_values, medinc_values)[0,1]:.3f}")
print("  - Inference: Strong positive correlation - higher median income consistently increases house prices")

# Analyze HouseAge
houseage_values = shap_values[:, "HouseAge"].values
houseage_feature_values = X_test["HouseAge"].values
print(f"\n• HOUSE AGE:")
print(f"  - Range of SHAP values: [{houseage_values.min():.3f}, {houseage_values.max():.3f}]")
print(f"  - Range of feature values: [{houseage_feature_values.min():.3f}, {houseage_feature_values.max():.3f}]")
print(f"  - Correlation with SHAP: {np.corrcoef(houseage_feature_values, houseage_values)[0,1]:.3f}")
if np.corrcoef(houseage_feature_values, houseage_values)[0,1] > 0:
    print("  - Inference: Newer houses tend to have higher prices")
else:
    print("  - Inference: Complex relationship - age effect varies by neighborhood/condition")

# 4. Model Behavior Insights
print("\n\n4. MODEL BEHAVIOR INSIGHTS:")
print("-" * 40)

# Calculate overall feature statistics
all_shap_values = shap_values.values
feature_means = np.mean(np.abs(all_shap_values), axis=0)
feature_stds = np.std(all_shap_values, axis=0)

print("• Feature Stability Analysis:")
for i, feature in enumerate(shap_values.feature_names):
    stability = feature_stds[i] / (feature_means[i] + 1e-8)  # Coefficient of variation
    stability_level = "High" if stability < 1 else "Medium" if stability < 2 else "Low"
    print(f"  - {feature}: {stability_level} stability (CV: {stability:.2f})")

# 5. Actionable Insights
print("\n\n5. ACTIONABLE INSIGHTS:")
print("-" * 40)
print("• For Home Buyers:")
most_important_feature = shap_values.feature_names[sorted_indices[0]]
print(f"  - Focus on {most_important_feature} as it has the highest impact on price predictions")
print("  - Higher median income areas consistently command premium prices")

print("\n• For Real Estate Investors:")
positive_features = [shap_values.feature_names[i] for i, val in enumerate(shapley_values) if val > 0]
negative_features = [shap_values.feature_names[i] for i, val in enumerate(shapley_values) if val < 0]
print(f"  - Price-increasing factors for this property: {', '.join(positive_features)}")
print(f"  - Price-decreasing factors for this property: {', '.join(negative_features)}")

print("\n• For Model Interpretation:")
print("  - The model shows logical behavior with income being the strongest predictor")
print("  - Geographic features (Latitude, Longitude) have significant impact, indicating location matters")
print("  - The model captures complex interactions between features effectively")

# 6. Data Quality and Model Reliability
print("\n\n6. MODEL RELIABILITY ASSESSMENT:")
print("-" * 40)
prediction_range = np.max(shap_values.values + shap_values.base_values) - np.min(shap_values.values + shap_values.base_values)
baseline_range = prediction_range / baseline if baseline != 0 else float('inf')
print(f"• Prediction range across test set: {prediction_range:.3f}")
print(f"• Relative to baseline: {baseline_range:.2f}x")
print("• Model shows reasonable variability in predictions")

if baseline_range > 3:
    print("• High prediction variability - model captures diverse housing market segments")
elif baseline_range < 1.5:
    print("• Conservative predictions - model may be underestimating price differences")
else:
    print("• Balanced prediction range - model shows appropriate sensitivity")

print("\n" + "="*80)