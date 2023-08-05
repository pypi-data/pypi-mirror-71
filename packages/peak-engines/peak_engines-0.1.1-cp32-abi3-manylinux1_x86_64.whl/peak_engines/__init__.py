from builtins import object
from . import peak_engines_impl
import numpy as np

class Warper(object):
    """Warping functor for a dataset's target space."""

    def __init__(self, impl):
        self.impl_ = impl

    def __call__(self, y):
        return self.compute_latent(y)

    def compute_latent(self, y):
        """Compute the warped latent values for a given target vector."""
        return self.impl_.compute_latent(np.array(y))

    def compute_latent_with_derivative(self, y):
        """Compute the warped latent values and derivatives for a given target vector."""
        return self.impl_.compute_latent_with_derivative(np.array(y))

    def invert(self, z):
        """Invert the warping transformation."""
        return self.impl_.invert(np.array(z))

class WarpedLinearRegressionModel(object):
    """Warped linear regression model fit so as to maximize likelihood.

    Parameters
    ----------
    init0 : object, default=None
        Functor that can be used to change the starting parameters of the optimizer.

    fit_intercept : bool, default=True
        Whether to center the target values and feature matrix columns.

    normalize : bool, default=True
        Whether to rescale the target vector and feature matrix columns.

    num_steps : int, default=1
        The number of components to use in the warping function. More components allows for the 
        model to fit more complex warping functions but increases the chance of overfitting.

    tolerance : float, default=0.0001
        The tolerance for the optimizer to use when deciding to stop the objective. With a lower
        value, the optimizer will be more stringent when deciding whether to stop searching.

    Examples
    --------
    """
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=True,
            num_steps=1,
            tolerance=0.0001):
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                num_steps=num_steps,
                tolerance=tolerance
        )

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value
        self.impl_ = peak_engines_impl.WarpedLinearRegressionModel(**self.params_)

    def fit(self, X, y):
        """Fit the warped linear regression model."""
        self.impl_.fit(np.array(X), np.array(y))
        return self

    def predict(self, X_test):
        """Predict target values."""
        return self.impl_.predict(np.array(X_test))

    def predict_latent_with_stddev(self, X_test):
        """Predict latent values along with the standard deviation of the error distribution."""
        return self.impl_.predict_latent_with_stddev(np.array(X_test))

    def predict_logpdf(self, X_test):
        """Predict target values with a functor that returns the log-likelihood of given target
        values under the model's error distribution."""
        z_pred, z_err = self.predict_latent_with_stddev(X_test)

        def logpdf(y):
            assert len(y) == len(z_pred)
            z, z_der = self.warper.compute_latent_with_derivative(y)
            result = 0
            for i, zi in enumerate(z):
                mean = z_pred[i]
                stddev = z_err[i]
                result += 0.5*(-np.log(2*np.pi*stddev**2) - ((zi - mean) / stddev)**2)
                result += np.log(z_der[i])
            return result
        return logpdf


    @property
    def warper(self):
        """Return the warper associated with the model."""
        return Warper(self.impl_.warper)

    @property
    def noise_variance(self):
        """Return the fitted noise variance."""
        return self.impl_.noise_variance

    @property
    def noise_stddev(self):
        """Return the fitted noise standard deviation."""
        return np.sqrt(self.impl_.noise_variance)

    @property
    def regressors(self):
        """Return the regressors of the latent linear regression model."""
        return self.impl_.regressors

    @property
    def within_tolerance(self):
        """Return True if the optimizer found parameters within the provided tolerance."""
        return self.impl_.within_tolerance
