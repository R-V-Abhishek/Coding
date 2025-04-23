import pandas as pd
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor, VotingRegressor, BaggingRegressor, ExtraTreesRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import StackingRegressor

# Generate a regression dataset
X, y = make_regression(n_samples=1000, n_features=2, noise=0.3, random_state=42)
feature_names = ['Feature 1', 'Feature 2']  # Assign feature names
X = pd.DataFrame(X, columns=feature_names)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Voting Regressor
voting_reg = VotingRegressor(
    estimators=[
        ('rf', RandomForestRegressor(random_state=42)),
        ('svr', SVR()),
        ('lr', LinearRegression())
    ]
)
voting_reg.fit(X_train, y_train)
for name, reg in voting_reg.named_estimators_.items():
    print(name, reg.score(X_test, y_test))

print("Voting Regressor Score:", voting_reg.score(X_test, y_test))

# Bagging Regressor
bagging_reg = BaggingRegressor(
    DecisionTreeRegressor(random_state=42),
    n_estimators=100,
    bootstrap=True,
    random_state=42
)

bagging_reg.fit(X_train, y_train)
print("Bagging Regressor Score:", bagging_reg.score(X_test, y_test))

# Random Forest Regressor
rf_reg = RandomForestRegressor(random_state=42)
rf_reg.fit(X_train, y_train)
print("Random Forest Regressor Score:", rf_reg.score(X_test, y_test))
for name, score in zip(rf_reg.feature_names_in_, rf_reg.feature_importances_):
    print(name, score)

# Extra-Trees Regressor
extra_trees_reg = ExtraTreesRegressor(random_state=42)
extra_trees_reg.fit(X_train, y_train)
print("Extra-Trees Regressor Score:", extra_trees_reg.score(X_test, y_test))

# AdaBoost Regressor
adaboost_reg = AdaBoostRegressor(
    DecisionTreeRegressor(random_state=42),
    n_estimators=50,
    random_state=42,
    learning_rate=0.5
)

adaboost_reg.fit(X_train, y_train)
print("AdaBoost Regressor Score:", adaboost_reg.score(X_test, y_test))

# Gradient Boosting Regressor
gradient_boost_reg = GradientBoostingRegressor(
    random_state=42,
    max_depth=3,  # Decision tree depth
    learning_rate=0.1,
    n_estimators=100
)
gradient_boost_reg.fit(X_train, y_train)
print("Gradient Boosting Regressor Score:", gradient_boost_reg.score(X_test, y_test))

# Stacking Regressor
stacking_reg = StackingRegressor(
    estimators=[
        ('rf', RandomForestRegressor(random_state=42)),
        ('svr', SVR()),
        ('lr', LinearRegression())
    ],
    final_estimator=LinearRegression()
)

stacking_reg.fit(X_train, y_train)
print("Stacking Regressor Score:", stacking_reg.score(X_test, y_test))