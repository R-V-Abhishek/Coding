# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 11:32:51 2023

@author: Manoj
"""
import numpy as np
from sklearn import neighbors 

# Generate random data
predictors = np.random.random(1000).reshape(500,2)
target = np.around(predictors.dot(np.array([0.4, 0.6])) + np.random.random(500))

# Create and train KNN classifier
clf = neighbors.KNeighborsClassifier(n_neighbors=10)
knn = clf.fit(predictors, target)

# Calculate and print the score
score = knn.score(predictors, target)
print(f"Model accuracy score: {score}")

# Print sample predictions
print("\nSample predictions:")
print(knn.predict(predictors[:5]))