import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score

class ft_KNN():
    def __init__(self, K=5):
        self.k = K

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        return [self._nearest_neighbors(x) for x in X]

    def _nearest_neighbors(self, x):
        distances = [self._dist(x, x_train) for x_train in self.X_train]
        indices = np.argsort(distances)[:self.k]
        nearests_labels = [self.y_train[i] for i in indices]

        return Counter(nearests_labels).most_common()[0][0]

    def _dist(self, a, b):
        return np.sqrt(np.sum((a-b)**2))

    def score(self, X, y, sample_weight=None):
        return accuracy_score(y, self.predict(X), sample_weight=sample_weight)
