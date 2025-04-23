import pandas as pd 
from sklearn.datasets import make_moons
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn. linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import StackingClassifier

X, y = make_moons(noise=0.30, random_state=42)
feature_names = ['Feature 1', 'Feature 2']  # Assign feature names
X = pd.DataFrame(X, columns=feature_names)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)



voting_clf = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(random_state=42)),
        ('svc', SVC(probability=True, random_state=42)),
        ('lr', LogisticRegression(random_state=42))
    ],
    voting='soft'
)

voting_clf.fit(X_train, y_train)
for name, clf in voting_clf.named_estimators_.items():
	print(name, clf.score(X_test, y_test))

print("Voting Classifier Score:", voting_clf.score(X_test, y_test))

bagging_clf = BaggingClassifier(
    DecisionTreeClassifier(random_state=42),
    n_estimators=100,
    bootstrap=True,
    oob_score=True,
    random_state=42
)

bagging_clf.fit(X_train, y_train)
print("Bagging Classifier OOB Score:", bagging_clf.oob_score_)
print(bagging_clf.oob_decision_function_)


rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
print("Random Forest Classifier Score:", rf_clf.score(X_test, y_test))
for name, score in zip(rf_clf.feature_names_in_, rf_clf.feature_importances_):
    print(name, score)

extra_trees_clf = ExtraTreesClassifier(random_state=42)
extra_trees_clf.fit(X_train, y_train)
print("Extra-Trees Classifier Score:", extra_trees_clf.score(X_test, y_test))

adaboost_clf = AdaBoostClassifier(
    DecisionTreeClassifier(random_state=42),
    n_estimators=50,
    random_state=42,
    learning_rate=0.5
)

adaboost_clf.fit(X_train, y_train)
print("AdaBoost Classifier Score:", adaboost_clf.score(X_test, y_test))

gradient_boost_clf = GradientBoostingClassifier(
    random_state=42,
    max_depth=3,  # Decision tree depth
    learning_rate=0.1,
    n_estimators=100
)
gradient_boost_clf.fit(X_train, y_train)
print("Gradient Boosting Classifier Score:", gradient_boost_clf.score(X_test, y_test))

stacking_clf = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(random_state=42)),
        ('svc', SVC(probability=True, random_state=42)),
        ('lr', LogisticRegression(random_state=42))
    ],
    final_estimator=LogisticRegression(random_state=42)
)

stacking_clf.fit(X_train, y_train)
print("Stacking Classifier Score:", stacking_clf.score(X_test, y_test))