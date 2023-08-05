#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : MLStudio                                                          #
# Version : 0.1.0                                                             #
# File    : regression.py                                                     #
# Python  : 3.8.2                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Wednesday, March 18th 2020, 4:34:57 am                      #
# Last Modified : Monday, March 23rd 2020, 10:31:37 am                        #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Regression algorithms.

This class encapsulates the core behaviors for regression classes. Currently,
the following regression classes are supported.
    
    * Linear Regression
    * Lasso Regression
    * Ridge Regression
    * ElasticNet Regression

The core behaviors exposed for each class include:

    * predict : Predicts outputs as linear combination of inputs and weights.
    * compute_cost : Computes cost associated with predictions
    * compute_gradient : Computes the derivative of loss w.r.t. to weights

"""
from abc import ABC, abstractmethod
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array

# --------------------------------------------------------------------------- #
#                          REGRESSION ALGORITHM                               #
# --------------------------------------------------------------------------- #
class Regression(ABC):
    """Base class for regression subclasses."""

    def __init__(self):      
        raise Exception("Instantiation of the Regression base class is prohibited.")  
        
    def _validate_hyperparam(self, p):
        assert isinstance(p, (int,float)), "Regularization hyperparameter must be numeric."
        assert p >= 0 and p <= 1, "Regularization parameter must be between zero and 1."

    def hypothesis(self, X, theta):
        """Computes the hypothesis using an input design matrix with bias term.

        Parameter
        ---------
        X : array of shape (m_observations, n_features+1)
            Input data

        theta : array of shape (n_features+1,)  
            The model parameters

        Returns
        -------
        hypothesis : Linear combination of inputs.

        """
        return X.dot(theta)


    def predict(self, X, theta):
        """Computes the prediction as linear combination of inputes and parameters.

        Parameter
        ---------
        X : array of shape (m_observations, n_features)
            Input data

        theta : array of shape (n_features+1,)  
            The model parameters

        Returns
        -------
        prediction : Linear combination of inputs.

        Raises
        ------
        Value error if X and theta have incompatible shapes.
        """
        X = np.array(X)
        check_array(X)        
                
        if X.shape[1] == len(theta):
            y_pred = X.dot(theta)
        elif X.shape[1] == len(theta) - 1:
            y_pred = theta[0] + X.dot(theta[1:])
        else:
            raise ValueError("X.shape[1] not compatible with parameters theta.")
        return y_pred

    @abstractmethod
    def compute_cost(self, y, y_pred, theta):
        """Computes the mean squared error cost.

        Parameters
        ----------
        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters            

        Returns
        -------
        cost : The quadratic cost 

        """
        pass

    @abstractmethod
    def compute_gradient(self, X, y, y_pred, theta):
        """Computes quadratic costs gradient with respect to weights.
        
        Parameters
        ----------
        X : array of shape (m_observations, n_features)
            Input data

        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters                        

        Returns
        -------
        gradient of the cost function w.r.t. the parameters.

        """
        pass
   

# --------------------------------------------------------------------------- #
#                        LINEAR REGRESSION (OLS)                              #
# --------------------------------------------------------------------------- # 
class LinearRegressionOLS(Regression):
    """Ordinary least squares closed form linear regression."""

    def __init__(self):
        self.name = "Linear Regression (OLS)"

    def fit(self, X, y):
        """Fits the linear regression ordinary least squares solution.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data

        y : numpy array, shape (n_samples,)
            Target values 

        Returns
        -------
        self : returns instance of self._
        """
        train_log = {'X': X, 'y': y}
        self._begin_training(train_log)
        
        # Calculate weights by least squares (using Moore-Penrose pseudoinverse)
        U, S, V = np.linalg.svd(self.X_design_.T.dot(self.X_design_))
        S = np.diag(S)
        X_ols = V.dot(np.linalg.pinv(S)).dot(U.T)
        self._theta = X_ols.dot(self.X_design.T).dot(self.y_)

        self._end_training()

        return self



# --------------------------------------------------------------------------- #
#                          LINEAR REGRESSION                                  #
# --------------------------------------------------------------------------- #    
class LinearRegression(Regression):
    """Linear Regression algorithm."""
    
    def __init__(self):
        self.name = "Linear Regression"

    def compute_cost(self, y, y_pred, theta):
        """Computes the mean squared error cost.

        Parameters
        ----------
        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters            

        Returns
        -------
        cost : The quadratic cost 

        """
        J = np.mean(0.5 * (y-y_pred)**2)
        return J

    def compute_gradient(self, X, y, y_pred, theta):
        """Computes quadratic costs gradient with respect to weights.
        
        Parameters
        ----------
        X : array of shape (m_observations, n_features)
            Input data

        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters                        

        Returns
        -------
        gradient of the cost function w.r.t. the parameters.

        """
        n_samples = X.shape[0]
        dZ = y_pred-y
        dW = float(1./n_samples) * X.T.dot(dZ) 
        return(dW)           

# --------------------------------------------------------------------------- #
#                          LASSO REGRESSION                                   #
# --------------------------------------------------------------------------- #    
class LassoRegression(Regression):
    """Lasso Regression algorithm."""
    
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.name = "Lasso Regression"

    def compute_cost(self, y, y_pred, theta):
        """Computes the mean squared error cost.

        Parameters
        ----------
        y : array of shape (n_samples,)
            Ground truth target values

        y_pred : array of shape (n_samples,)
            Predictions 

        theta : array of shape (n_features+1,)  
            The model parameters            

        Returns
        -------
        cost : The quadratic cost 

        """
        self._validate_hyperparam(self.alpha)
        n_samples = y.shape[0]
        J_reg = (self.alpha / n_samples) * np.linalg.norm(theta, ord=1)
        J = np.mean(0.5 * (y-y_pred)**2) + J_reg
        return J

    def compute_gradient(self, X, y, y_pred, theta):
        """Computes quadratic costs gradient with respect to weights.
        
        Parameters
        ----------
        X : array of shape (n_samples, n_features+1)
            Input data

        y : array of shape (n_samples,)
            Ground truth target values

        y_pred : array of shape (n_samples,)
            Predictions 

        theta : array of shape (n_features+1,)  
            The model parameters                        

        Returns
        -------
        gradient of the cost function w.r.t. the parameters.

        """
        n_samples = X.shape[0]
        dZ = y_pred-y
        dW = 1/n_samples  * (X.T.dot(dZ) + self.alpha * np.sign(theta))
        return(dW)           

# --------------------------------------------------------------------------- #
#                          RIDGE REGRESSION                                   #
# --------------------------------------------------------------------------- #            
class RidgeRegression(Regression):
    """Ridge Regression algorithm."""
    
    def __init__(self, alpha=1):
        self.alpha=alpha
        self.name = "Ridge Regression"    

    def compute_cost(self, y, y_pred, theta):
        """Computes the mean squared error cost.

        Parameters
        ----------
        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters            

        Returns
        -------
        cost : The quadratic cost 

        """
        self._validate_hyperparam(self.alpha)
        n_samples = y.shape[0]
        J_reg = (self.alpha / (2*n_samples)) * np.linalg.norm(theta)**2
        J = np.mean(0.5 * (y-y_pred)**2) + J_reg
        return J

    def compute_gradient(self, X, y, y_pred, theta):
        """Computes quadratic costs gradient with respect to weights.
        
        Parameters
        ----------
        X : array of shape (m_observations, n_features)
            Input data

        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters                        

        Returns
        -------
        gradient of the cost function w.r.t. the parameters.

        """
        n_samples = X.shape[0]
        dZ = y_pred-y
        dW = 1/n_samples  * (X.T.dot(dZ) + self.alpha * theta)
        return(dW)                         

# --------------------------------------------------------------------------- #
#                        ELASTIC NET REGRESSION                               #
# --------------------------------------------------------------------------- #            
class ElasticNetRegression(Regression):
    """Elastic Net Regression algorithm."""
    
    def __init__(self, alpha=1, ratio=0.5):
        self.alpha=alpha
        self.ratio=ratio
        self.name = "ElasticNet Regression"           

    def compute_cost(self, y, y_pred, theta):
        """Computes the mean squared error cost.

        Parameters
        ----------
        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters            

        Returns
        -------
        cost : The quadratic cost 

        """
        n_samples = y.shape[0]
        self._validate_hyperparam(self.alpha)
        self._validate_hyperparam(self.ratio)
        l1_contr = self.ratio * np.linalg.norm(theta, ord=1)
        l2_contr = (1 - self.ratio) * 0.5 * np.linalg.norm(theta)**2        
        J_reg = float(1./n_samples) * self.alpha * (l1_contr + l2_contr)
        J = np.mean(0.5 * (y-y_pred)**2) + J_reg
        return J

    def compute_gradient(self, X, y, y_pred, theta):
        """Computes quadratic costs gradient with respect to weights.
        
        Parameters
        ----------
        X : array of shape (m_observations, n_features)
            Input data

        y : array of shape (n_features,)
            Ground truth target values

        y_pred : array of shape (n_features,)
            Predictions 

        theta : array of shape (n_features,)  
            The model parameters                        

        Returns
        -------
        gradient of the cost function w.r.t. the parameters.

        """
        n_samples = X.shape[0]
        l1_contr = self.ratio * np.sign(theta)
        l2_contr = (1 - self.ratio) * theta
        alpha = np.asarray(self.alpha, dtype='float64')         
        dZ = y_pred-y
        dW = 1/n_samples  * (X.T.dot(dZ) + np.multiply(alpha, np.add(l1_contr, l2_contr)))
        return(dW)               