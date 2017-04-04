#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example of Linear Regression

This program demonstrates the use of statsmodel linear regression.
The actual example processes data from spring-mass and refraction
experiments.
"""

import os.path
import math
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from statsmodels.sandbox.regression.predstd \
    import wls_prediction_std

def read_data(fname):
    """Read data from tidy CSV data frame.
    
    Arguments:
        fname    -- Name of file where data resides
    """
    data = pd.read_csv(fname)
    return data

springs    = read_data(os.path.join("..", "data", "experiment-springs.csv"))
refraction = read_data(os.path.join("..", "data", "experiment-refraction.csv"))

def visualize_data(data, response_name, predictor_name):
    """Create a scatter plot of the predictor vs. the response variable.
    
    Arguments:
        data           -- a tidy DataFrame, with response in column 1 and response in column 2
        response_name  -- name of the response variable
        predictor_name -- name of the predictor variable
    """
    ax = data.plot(kind='scatter', x=1, y=0,
                   title=('Relationship of %s vs. %s' % (response_name, predictor_name)),
                   #xlim=(axis_low, axis_high), ylim=(axis_low, axis_high)
                   )
    ax.set_xlabel(predictor_name)
    ax.set_ylabel(response_name)
    #ax.set_aspect(1)

visualize_data(springs, 'Spring Displacement', 'Mass')
plt.savefig(os.path.join("..", 'img', 'scatter-plot-springs.png'))
visualize_data(refraction, 'Refraction Angle', 'Incidence Angle')
plt.savefig(os.path.join("..", 'img', 'scatter-plot-refraction.png'))

def do_linear_regression(data):
    """Perform a linear regression for column 1 based on column 2 of the DataFrame.
    
    Arguments:
        data      -- a tidy DataFrame, with response in column 1, predictor in column 2, and constant in column 3
    """
    model = sm.OLS(data.iloc[:, 0], 
                   data.iloc[:, [1, 2]],
                   missing='drop')
    fit = model.fit()
    return fit

springs_fit = do_linear_regression(springs)
print (springs_fit.summary ())

refraction_fit = do_linear_regression(refraction)
print (refraction_fit.summary ())

def transform_refraction(data):
    """Transform the data by taking sines of the first and second column.
    
    Arguments:
        data      -- a tidy DataFrame, with response in column 1, predictor in column 2, and constant in column 3
    """

    data = data.copy()
    data.iloc[:,0] = data.iloc[:,0].apply(math.sin)
    data.iloc[:,1] = data.iloc[:,1].apply(math.sin)
    
    return data

transformed_refraction = transform_refraction(refraction)
transformed_refraction_fit = do_linear_regression(transformed_refraction)
print (transformed_refraction_fit.summary ())

def visualize_linear_regression(data, fit, response_name, predictor_name, show_std=False):
    """Create a scatter plot and linear model of the response variable (column 1) vs. predictor variable (column 2).
    
    Arguments:
        data           -- a tidy DataFrame, with response in column 1, predictor in column 2, and constant in column 3
        fit            -- a linear regression result
        response_name  -- name of the response variable
        predictor_name -- name of the predictor variable
        show_std       -- whether to show upper and lower bands around answer (default False)
    """
    ax = data.plot(kind='scatter', x=1, y=0,
                   title=('Relationship of %s vs. %s' % (response_name, predictor_name)),
                   #xlim=(axis_low, axis_high), ylim=(axis_low, axis_high)
                   )
    X_new = pd.DataFrame({'predictor': ax.get_xlim()})
    X_new['const'] = 1
    preds = fit.predict(X_new)
    plt.plot(X_new['predictor'], preds, 'r-')
    if show_std:
        _, lower, upper = wls_prediction_std(fit, X_new)
        plt.plot(X_new['predictor'], lower, 'r--', 
                 X_new['predictor'], upper, 'r--')
    ax.set_xlabel(predictor_name)
    ax.set_ylabel(response_name)
    # ax.set_aspect(1)


visualize_linear_regression(springs, springs_fit, 'Spring Displacement', 'Mass')
plt.savefig(os.path.join("..", 'img', 'springs-lr-plot-without-errors.png'))

visualize_linear_regression(springs, springs_fit, 'Spring Displacement', 'Mass', True)
plt.savefig(os.path.join("..", 'img', 'springs-lr-plot-with-errors.png'))

visualize_linear_regression(refraction, refraction_fit, 'Refraction Angle', 'Incidence Angle')
plt.savefig(os.path.join("..", 'img', 'refraction-lr-plot-without-errors.png'))

visualize_linear_regression(refraction, refraction_fit, 'Refraction Angle', 'Incidence Angle', True)
plt.savefig(os.path.join("..", 'img', 'refraction-lr-plot-with-errors.png'))

visualize_linear_regression(transformed_refraction, transformed_refraction_fit, 'Sine Refraction Angle', 'Sine Incidence Angle')
plt.savefig(os.path.join("..", 'img', 'refraction-xlr-plot-without-errors.png'))

visualize_linear_regression(transformed_refraction, transformed_refraction_fit, 'Sine Refraction Angle', 'Sine Incidence Angle', True)
plt.savefig(os.path.join("..", 'img', 'refraction-xlr-plot-with-errors.png'))

def visualize_linear_regression_with_transformation(orig_data, fit, response_name, predictor_name, response_inverse, predictor_transform, show_std=False):
    """Create a scatter plot and linear model of the response variable (column 1) vs. predictor variable (column 2).
    
    Arguments:
        orig_data           -- a tidy DataFrame, with response in column 1, predictor in column 2, and constant in column 3
        fit                 -- a linear regression result
        response_name       -- name of the response variable
        predictor_name      -- name of the predictor variable
        response_inverse    -- inverse transformation to apply to response variable
        predictor_transform -- transformation to apply to predictor variable
        show_std            -- whether to show upper and lower bands around answer (default False)
    """
    ax = orig_data.plot(kind='scatter', x=1, y=0,
                        title=('Relationship of %s vs. %s' % (response_name, predictor_name)))
    X_orig = pd.np.linspace(min(orig_data.iloc[:,1]), max(orig_data.iloc[:,1]))
    X_new = pd.DataFrame({'predictor': X_orig})
    X_new['predictor'] = X_new['predictor'].apply(predictor_transform)
    X_new['const'] = 1
    preds = fit.predict(X_new)
    vrespinv = pd.np.vectorize(response_inverse)
    preds = vrespinv(preds)
    plt.plot(X_orig, preds, 'r-')

    if show_std:
        _, lower, upper = wls_prediction_std(fit, X_new)
        lower = vrespinv(lower)
        upper = vrespinv(upper)
        plt.plot(X_orig, lower, 'r--', 
                 X_orig, upper, 'r--')
    ax.set_xlabel(predictor_name)
    ax.set_ylabel(response_name)
    # ax.set_aspect(1)

visualize_linear_regression_with_transformation(refraction, transformed_refraction_fit, 'Refraction Angle', 'Incidence Angle', math.asin, math.sin)
plt.savefig(os.path.join("..", 'img', 'refraction-nonlinear-plot-without-errors.png'))

visualize_linear_regression_with_transformation(refraction, transformed_refraction_fit, 'Refraction Angle', 'Incidence Angle', math.asin, math.sin, True)
plt.savefig(os.path.join("..", 'img', 'refraction-nonlinear-plot-with-errors.png'))

