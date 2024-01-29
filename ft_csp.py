import numpy as np
from scipy import linalg
from sklearn.base import TransformerMixin, BaseEstimator

class ft_CSP(TransformerMixin, BaseEstimator):
    def __init__(self, n_components=4, log=None):
            if not isinstance(n_components, int):
                raise ValueError("n_components must be an integer.")
            self.n_components = n_components
            self.log = log
            self.filters_ = None

    def _check_Xy(self, X, y=None):
        if not isinstance(X, np.ndarray):
            raise ValueError("X should be of type ndarray (got %s)." % type(X))
        if y is not None:
            if len(X) != len(y) or len(y) < 1:
                raise ValueError("X and y must have the same length.")
        if X.ndim < 3:
            raise ValueError("X must have at least 3 dimensions.")

    def _compute_covariance_matrices(self, X, y):
        covs = []
        for label in self._classes:
            x_class = X[y==label]
            _, n_channels, _ = x_class.shape
            x_class = np.transpose(x_class, [1, 0, 2])
            x_class = x_class.reshape(n_channels, -1)
            cov = np.cov(x_class, ddof=1)
            covs.append(cov)
        return np.stack(covs)

    def fit(self, X, y):
        self._check_Xy(X, y)

        self._classes = np.unique(y)
        n_classes = len(self._classes)
        if n_classes < 2:
            raise ValueError("n_classes must be >= 2.")

        covs = self._compute_covariance_matrices(X, y)
        eigen_values, eigen_vectors = linalg.eigh(covs[0], covs.sum(0))

        ix = np.argsort(np.abs(eigen_values - 0.5))[::-1]
        eigen_vectors = eigen_vectors[:, ix]

        self.filters_ = eigen_vectors.T
        self.patterns_ = linalg.pinv(eigen_vectors)

        pick_filters = self.filters_[: self.n_components]
        X = np.asarray([np.dot(pick_filters, epoch) for epoch in X])

        X = (X**2).mean(axis=2)
        self.mean_ = X.mean(axis=0)
        self.std_ = X.std(axis=0)
        return self

    def transform(self, X):
        if not isinstance(X, np.ndarray):
            raise ValueError("X should be of type ndarray (got %s)." % type(X))
        if self.filters_ is None:
            raise RuntimeError("No filters available. Please first fit CSP")

        pick_filters = self.filters_[: self.n_components]
        X = np.asarray([np.dot(pick_filters, epoch) for epoch in X])

        X = (X**2).mean(axis=2)
        log = True if self.log is None else self.log
        if log:
            X = np.log(X)
        else:
            X -= self.mean_
            X /= self.std_
        return X

    def fit_transform(self, X, y, **fit_params):
        return super().fit_transform(X, y=y, **fit_params)
