from sklearn.datasets import make_moons
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from sklearn. linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
X, y = make_moons(noise=0.30, random_state=42)
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